import gradio as gr
from models.mytho_awq import MythoAWQ


def app():
    model = MythoAWQ()

    with gr.Blocks() as gr_app:
        with gr.Box():
            with gr.Column():
                gr.Markdown('<h1><center>Robo DM</center></h1>')
                prompt = gr.Textbox(placeholder='Story elements...',
                                    lines=8, show_label=False, container=False, autofocus=True)
                checks = gr.CheckboxGroup(['Dune', 'LoTR', 'Star Wars'], show_label=False, container=False),
                genre = gr.Textbox(placeholder='Genre...',
                                lines=3, show_label=False, container=False)
                submit = gr.Button(value='generate')
        outputs = gr.Textbox(max_lines=32, show_label=False)

        submit.click(model.generate, inputs=[genre, prompt], outputs=outputs)

    gr_app.launch()


if __name__ == '__main__':
    app()
