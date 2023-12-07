from huggingface_hub import login
import torch
from typing import Any, Literal
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, GenerationConfig


class Llama7b:
    def __init__(self):
        self.model_name = 'meta-llama/Llama-2-7b-chat-hf'
        hf_read_secret = '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'
        login(hf_read_secret, add_to_git_credential=False)

        self.llm = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map='auto',
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type='nf4',
                bnb_4bit_compute_dtype=torch.bfloat16,
            ))
        self.tkr = AutoTokenizer.from_pretrained(self.model_name)
        self.gen_cf = GenerationConfig(
                max_length=4096,
                do_sample=True,
                temperature=.8,
                top_p=.9,
            )
        # self.gen_cf_hi = GenerationConfig(
        #         max_length=4096,
        #         do_sample=True,
        #         temperature=1.4,
        #     )

    def generate(self, prompt: str) -> str: #, cfg_temp: Literal[ 'lo', 'hi' ]='lo') -> str:
        ins = self.tkr(prompt, return_tensors='pt').to('cuda:0')
        outs = self.llm.generate(**ins, generation_config=self.gen_cf)[0]# if cfg_temp=='lo' else self.gen_cf_hi)[0]
        resp = self.tkr.decode(outs, skip_special_tokens=True)
        resp = resp[len(prompt):]
        resp = resp.strip()
        return resp


class Llama13b:
    def __init__(self):
        self.model_name = 'meta-llama/Llama-2-13b-chat-hf'
        hf_read_secret = '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'
        login(hf_read_secret, add_to_git_credential=False)

        self.llm = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map='auto',
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type='nf4',
                bnb_4bit_compute_dtype=torch.bfloat16,
            ))
        self.tkr = AutoTokenizer.from_pretrained(self.model_name)
        self.gen_cf = GenerationConfig(
                max_length=4096,
                do_sample=True,
                temperature=.8,
                top_p=.9,
            )
        # self.gen_cf_hi = GenerationConfig(
        #         max_length=4096,
        #         do_sample=True,
        #         temperature=1.4,
        #     )

    def generate(self, prompt: str) -> str: #, cfg_temp: Literal[ 'lo', 'hi' ]='lo') -> str:
        ins = self.tkr(prompt, return_tensors='pt').to('cuda:0')
        outs = self.llm.generate(**ins, generation_config=self.gen_cf)[0]# if cfg_temp=='lo' else self.gen_cf_hi)[0]
        resp = self.tkr.decode(outs, skip_special_tokens=True)
        resp = resp[len(prompt):]
        resp = resp.strip()
        return resp


class Novellama13b:
    def __init__(self):
        self.model_name = 'logij/Novellama-13b-chat-hf'
        # self.model_name = '/home/lj/.cache/huggingface/hub/models--LJ--Llama-2-13b-fantasy-finetune'
        hf_read_secret = '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'
        login(hf_read_secret, add_to_git_credential=False)

        self.llm = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map='auto',
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type='nf4',
                bnb_4bit_compute_dtype=torch.bfloat16,
            ))
        self.tkr = AutoTokenizer.from_pretrained(self.model_name)
        self.gen_cf = GenerationConfig(
                max_length=4096,
                do_sample=True,
                temperature=.8,
                top_p=.9,
            )
        # self.gen_cf_hi = GenerationConfig(
        #         max_length=4096,
        #         do_sample=True,
        #         temperature=1.4,
        #     )

    def generate(self, prompt: str) -> str: #, cfg_temp: Literal[ 'lo', 'hi' ]='lo') -> str:
        ins = self.tkr(prompt, return_tensors='pt').to('cuda:0')
        outs = self.llm.generate(**ins, generation_config=self.gen_cf)[0]# if cfg_temp=='lo' else self.gen_cf_hi)[0]
        resp = self.tkr.decode(outs, skip_special_tokens=True)
        resp = resp[len(prompt):]
        resp = resp.strip()
        return resp


def model_switch(name: Literal[ 'llama7b', 'llama13b', 'novellama13b']) -> Any:
    if name == 'llama7b':
        return Llama7b()
    elif name == 'llama13b':
        return Llama13b()
    elif name == 'novellama13b':
        return Novellama13b()
    else:
        print(f'** ERROR: Unknown model {name}; now exiting')
        exit()