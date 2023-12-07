import gradio as gr
from models.llama import Llama7b

D_BLURB = '''[INST] <<SYS>>
(assistant description, tendencies, taboos)
<</SYS>>

(prompt and background information) [/INST]
'''

def app():
    model = Llama7b()

    with gr.Blocks() as gr_app:
        gr.Markdown('<h1><center><em>Robo DM -- Bare Metal Edition</em></center></h1>')
        with gr.Box():
            with gr.Column():
                gr.Markdown('<h2>Full Llama Prompt</h2>')
                blurb = gr.Textbox(placeholder='Story elements...', value=D_BLURB,
                                    lines=8, show_label=False, container=False, autofocus=True)
                gen_btn = gr.Button(value='generate')
                resp_box = gr.Textbox(lines=4, max_lines=32, show_label=False)#, container=False)
        gen_btn.click(model.generate, inputs=[blurb], outputs=resp_box)

    # gr_app.queue() # needed if any 'click' event functions return generators
    gr_app.launch()


if __name__ == '__main__':
    app()
