import gradio as gr
from lib.models import Llama7b

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
