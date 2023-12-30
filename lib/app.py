import gradio as gr
from lib.globals import MODELS
from lib.models import model_switch

# from lib.globals import D_BLURB, D_GENRE
TEXTBOX_LINES = 32

 
def app(model_name: MODELS, share: bool=False):
    model = model_switch(model_name)
    gr_state = gr.State({'characters': None, 'species': None, 'locales': None, 'plot': None, 'acts': None, 'scenes': None})

    with gr.Blocks() as gr_app:
        gr.Markdown('<h1><center><em>Robo DM</em></center></h1>')
        gr.Markdown('<p><em>Robo DM</em> is here to help!</p><p>Freedom of play isn\'t mandatory, but <b>FUN IS</b></p>')

        outs_box = gr.Markdown('')

        with gr.Column():
            with gr.Row(variant='panel'):
                gr.Textbox('Genre:', scale=1, lines=1, container=False, interactive=False)
                genre_box = gr.Textbox(scale=3, lines=1, placeholder='Genre...', container=False, show_label=False, interactive=True, autofocus=True)#, value=D_GENRE
                # genre_btn = gr.Button('select')
                # def gbc(t):
                #     return gr.Textbox(interactive=False), gr.Button(interactive=False)#scale=3, lines=1, value=t, container=False, show_label=False, interactive=False, autofocus=True), \
                # genre_btn.click(gbc, [genre_box], [genre_box, genre_btn], show_progress='hidden')


            with gr.Tabs():
                with gr.Tab('Elements'):
                    with gr.Tab('Characters'):
                        with gr.Group():
                            chars_box = gr.Textbox(placeholder='Base character info...', lines=TEXTBOX_LINES, show_label=False, container=False)
                            with gr.Row():
                                chars_generate_bt = gr.Button('generate', scale=4)
                                chars_generate_num = gr.Number(1, precision=0, minimum=1, maximum=5, interactive=True, show_label=False, container=False)
                                chars_generate_bt.click(model.generate_characters, inputs=[genre_box, chars_box, chars_generate_num, gr_state], outputs=[chars_box, gr_state, outs_box])

                    with gr.Tab('Species'):
                        with gr.Group():
                            species_box = gr.Textbox(placeholder='Base species info...', lines=TEXTBOX_LINES, show_label=False, container=False)
                            with gr.Row():
                                species_generate_bt = gr.Button('generate', scale=4)
                                species_generate_num = gr.Number(1, precision=0, minimum=1, maximum=5, interactive=True, show_label=False, container=False)
                                species_generate_bt.click(model.generate_species, inputs=[genre_box, species_box, species_generate_num, gr_state], outputs=[species_box, gr_state, outs_box])

                    with gr.Tab('Locales'):
                        with gr.Group():
                            locales_box = gr.Textbox(placeholder='Base locale info...', lines=TEXTBOX_LINES, show_label=False, container=False)
                            with gr.Row():
                                locales_generate_bt = gr.Button('generate', scale=4)
                                locales_generate_num = gr.Number(1, precision=0, minimum=1, maximum=5, interactive=True, show_label=False, container=False)
                                locales_generate_bt.click(model.generate_locales, inputs=[genre_box, locales_box, locales_generate_num, gr_state], outputs=[locales_box, gr_state, outs_box])


                with gr.Tab('Plot'):
                    with gr.Group():
                        gr.Markdown('<h3><center>Story Overview</center></h3>')
                        plot_box = gr.Textbox(placeholder='Plot blurb...', lines=TEXTBOX_LINES, show_label=False, container=False)
                        plot_generate_bt = gr.Button('generate')
                        plot_generate_bt.click(model.generate_plot, inputs=[genre_box, chars_box, species_box, locales_box, plot_box, gr_state], outputs=[plot_box, gr_state, outs_box])


                with gr.Tab('Story'):
                    with gr.Group():
                        gr.Markdown('<h3><center>Plot by Act</center></h3>')
                        acts_box = gr.Textbox(lines=TEXTBOX_LINES, show_label=False, container=False)
                        acts_generate_bt = gr.Button('generate')
                        acts_generate_bt.click(model.generate_acts, inputs=[genre_box, plot_box, gr_state], outputs=[acts_box, gr_state, outs_box])


                with gr.Tab('Scenes'):
                    with gr.Group():
                        gr.Markdown('<h3><center>Scenes by Act</center></h3>')
                        scenes_box = gr.Textbox(lines=TEXTBOX_LINES, show_label=False, container=False)
                        scenes_generate_bt = gr.Button('generate')
                        scenes_generate_bt.click(model.generate_scenes, inputs=[genre_box, acts_box, gr_state], outputs=[scenes_box, gr_state, outs_box])




    gr_app.queue() # needed if any 'click' event functions return generators
    gr_app.launch(share=share, show_api=False)



    # checks = gr.CheckboxGroup(['Dune', 'LoTR', 'Star Wars'], show_label=False, container=False),
