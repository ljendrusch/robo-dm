from vllm import LLM, SamplingParams
from .prompt_templates import *


class MythoAWQ:
    def __init__(self):
        self.llm = LLM(model="TheBloke/MythoMax-L2-13B-AWQ", quantization="awq")
        self.sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=4096)

    def generate(self, genre, prompt):
        prompt_tp = prompt_templates[0]
        system_message = prompt_tp[0] + genre + prompt_tp[1]
        prompt_template=f"{system_message}\n\n### Instruction:\n{prompt}\n\n### Response:"

        outs = self.llm.generate(prompt_template, self.sampling_params)
        return '\n'.join([ o.outputs[0].text for o in outs ])

    # def print_outputs(self, outputs):
    #     for output in outputs:
    #         p = output.prompt
    #         generated_text = output.outputs[0].text
    #         print(f"Prompt:\n{p}\n\nGenerated text:\n{generated_text}")


if __name__ == '__main__':
    model = MythoAWQ()
    genre = "sci-fi"
    prompt = "Johnny is attacked by wolves. His sister, Clara, is abducted by aliens."
    outs = model.generate(genre, prompt)
    print(outs)
