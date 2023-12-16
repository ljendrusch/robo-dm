import gradio as gr
from huggingface_hub import login
from torch import bfloat16
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, GenerationConfig


class Llama7b:
    def __init__(self):
        self.model_name = 'meta-llama/Llama-2-7b-chat-hf'
        hf_secret = 'enter huggingface token here'
        login(hf_secret)

        self.llm = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map='auto',
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type='nf4',
                bnb_4bit_compute_dtype=bfloat16,
            ))
        self.tkr = AutoTokenizer.from_pretrained(self.model_name)
        self.gen_cf = GenerationConfig(
                max_length=4096,
                do_sample=True,
                temperature=.8,
                top_p=.9,
            )

    def generate(self, prompt: str) -> str:
        ins = self.tkr(prompt, return_tensors='pt').to('cuda:0')
        outs = self.llm.generate(**ins, generation_config=self.gen_cf)[0]
        resp = self.tkr.decode(outs, skip_special_tokens=True)
        resp = resp[len(prompt):]
        resp = resp.strip()
        return resp



D_BLURB = '''[INST] <<SYS>>
(assistant description, tendencies, taboos)
<</SYS>>

(prompt and background information) [/INST]
'''

def bare_metal():
    model = Llama7b()

    with gr.Blocks() as gr_app:
        gr.Markdown('<h1><center><em>Robo DM -- Bare Metal Edition</em></center></h1>')
        with gr.Group():
            gr.Markdown('<h2>Full Llama Prompt</h2>')
            blurb = gr.Textbox(value=D_BLURB, lines=24, show_label=False, container=False, autofocus=True)
            gen_btn = gr.Button(value='generate')
            resp_box = gr.Textbox(lines=24, show_label=False, container=False)
        gen_btn.click(model.generate, inputs=[blurb], outputs=resp_box)

    gr_app.launch()


if __name__ == '__main__':
    bare_metal()
