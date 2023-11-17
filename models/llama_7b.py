import re
import timeit
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, GenerationConfig
from typing import List, Literal

# from huggingface_hub import login
from .prompt_templates import Interaction, \
    characters_prompt, species_prompt, places_prompt, acts_prompt, scenes_prompt


class Llama7b:
    def __init__(self):
        self.model_name = 'meta-llama/Llama-2-7b-chat-hf'
        # hf_read_secret = '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'
        # login(hf_read_secret, add_to_git_credential=False)

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
        self.gen_cf_lo = GenerationConfig(
                max_new_tokens=2048,
                do_sample=True,
                temperature=.8,
                top_p=.9,
            )
        self.gen_cf_hi = GenerationConfig(
                max_new_tokens=1024,
                do_sample=True,
                temperature=1.4,
            )
        self.acts_re = re.compile(r'^Act \d{1,2}: .+$\n', re.M)

    def generate(self, prompt: str, cfg_temp: Literal[ 'lo', 'hi' ]='lo') -> str:
        prompt = prompt.strip()

        st = timeit.default_timer()
        ins = self.tkr(prompt, return_tensors='pt').to('cuda:0')
        outs = self.llm.generate(**ins, generation_config=self.gen_cf_lo if cfg_temp=='lo' else self.gen_cf_hi)[0]
        resp = self.tkr.decode(outs, skip_special_tokens=True)
        resp = resp[len(prompt):]
        resp = resp.strip()

        print(resp)

        Interaction(self.__class__.__name__,
                    timeit.default_timer()-st,
                    prompt,
                    resp).to_json()
        return resp

    def generate_acts(self, genre: str, blurb: str) -> str:
        if not genre or not blurb:
            return ''
        genre = genre.strip()
        blurb = blurb.strip()
        if len(genre) < 3 or len(blurb) < 12:
            return ''
        return self.generate(acts_prompt(genre, blurb))

    def generate_scenes(self, genre: str, acts_blob: str) -> str:
        if not genre or not acts_blob:
            return ''
        genre = genre.strip()
        acts_blob = acts_blob.strip()
        if len(genre) < 3 or len(acts_blob) < 12:
            return ''
        acts = [s.strip() for s in self.acts_re.split(acts_blob) if s]
        scenes = []
        for i,act in enumerate(acts):
            scenes.append(f'Act {i+1} {self.generate(scenes_prompt(genre, act))}\n')
            yield '    ----------------------------------------------------------------\\n\n'.join(scenes)

    def generate_characters(self, genre: str, chars_blob: str, num_chars: int) -> str:
        # blurbs = chars_blob.split('\n\n')
        # if len(blurbs) == num_chars:
        return self.generate(characters_prompt(genre, chars_blob, num_chars), cfg_temp='hi')

    def generate_species(self, genre: str, species_blob: str, num_species: int) -> str:
        return self.generate(species_prompt(genre, species_blob, num_species), cfg_temp='hi')

    def generate_places(self, genre: str, places_blob: str, num_places: int) -> str:
        return self.generate(places_prompt(genre, places_blob, num_places), cfg_temp='hi')
