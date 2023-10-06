from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from .prompt_templates import *


class MythoGPTQ:
    def __init__(self):
        model_name_or_path = "TheBloke/MythoMax-L2-13B-GPTQ"
        self.model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                                    device_map="auto",
                                                    revision="gptq-4bit-32g-actorder_True")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

        self.gen_config = GenerationConfig.from_model_config(self.model.config)
        self.gen_config.max_new_tokens = 4096
        self.gen_config.min_length = 1
        self.gen_config.do_sample=True

    def generate(self, genre, prompt):
        prompt_tp = prompt_templates[0]
        system_message = prompt_tp[0] + genre + prompt_tp[1]
        prompt_template=f"{system_message}\n\n### Instruction:\n{prompt}\n\n### Response:"

        input_ids = self.tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
        outs = self.model.generate(inputs=input_ids, generation_config=self.gen_config)
        return '\n'.join([ self.tokenizer.decode(o) for o in outs ])


if __name__ == '__main__':
    model = MythoGPTQ()
    genre = "sci-fi"
    prompt = "Johnny is attacked by wolves. His sister, Clara, is abducted by aliens."
    outs = model.generate(genre, prompt)
    print(outs)
