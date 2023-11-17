import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "4"

import gradio as gr
from models.llama_7b import Llama7b

D_BLURB = 'Gram discovers a looming intergalactic threat while working at a dig site. But noone will believe him.'
D_GENRE = 'science fiction'


def app():
    model = Llama7b()

    with gr.Blocks() as gr_app:
        # scenes_var = gr.State([])
        gr.Markdown('<h1><center><em>Robo DM</em></center></h1>')
        gr.Markdown('<p><em>Robo DM</em> is here to help!</p><p>Freedom of play isn\'t mandatory, but FUN is</p>')

        with gr.Row(variant='panel'):
            gr.Textbox('Genre (Required First)', scale=1, lines=1,
                       container=False, interactive=False)
            genre_box = gr.Textbox(scale=3, lines=1, placeholder='Genre...', value=D_GENRE,
                        container=False, interactive=True)


        with gr.Accordion('Characters, Species, Places (Optional)', open=False):
            with gr.Tab('Characters'):
                chars_box = gr.Textbox(placeholder='Character backstories...', show_label=False, container=False)
                with gr.Row(variant='panel'):
                    chars_generate_bt = gr.Button('generate', scale=4)
                    chars_generate_num = gr.Number(1, precision=0, minimum=1, maximum=5, interactive=True, show_label=False, container=False)
                chars_generate_bt.click(model.generate_characters, inputs=[genre_box, chars_box, chars_generate_num], outputs=chars_box)

            with gr.Tab('Species'):
                species_box = gr.Textbox(placeholder='Species traits...', show_label=False, container=False)
                with gr.Row(variant='panel'):
                    species_generate_bt = gr.Button('generate', scale=4)
                    species_generate_num = gr.Number(1, precision=0, minimum=1, maximum=5, interactive=True, show_label=False, container=False)
                species_generate_bt.click(model.generate_species, inputs=[genre_box, species_box, species_generate_num], outputs=species_box)

            with gr.Tab('Places'):
                places_box = gr.Textbox(placeholder='Place descriptions...', show_label=False, container=False)
                with gr.Row(variant='panel'):
                    places_generate_bt = gr.Button('generate', scale=4)
                    places_generate_num = gr.Number(1, precision=0, minimum=1, maximum=5, interactive=True, show_label=False, container=False)
                places_generate_bt.click(model.generate_places, inputs=[genre_box, places_box, places_generate_num], outputs=places_box)


        with gr.Accordion('Plot Overview', open=False):
            blurb_box = gr.Textbox(placeholder='Story elements...', value=D_BLURB, #lines=12,
                                show_label=False, container=False)
            # checks = gr.CheckboxGroup(['Dune', 'LoTR', 'Star Wars'], show_label=False, container=False),
            plot_generate_bt = gr.Button('generate')
            acts_box = gr.Textbox(max_lines=32, show_label=False)
        plot_generate_bt.click(model.generate_acts, inputs=[genre_box, blurb_box], outputs=acts_box)


        with gr.Accordion('Scenes by Act', open=False):
            scenes_generate_bt = gr.Button('generate')
            scenes_box = gr.Textbox(show_label=False)#, max_lines=32
            scenes_box.change()
        scenes_generate_bt.click(model.generate_scenes, inputs=[genre_box, acts_box], outputs=scenes_box)

    gr_app.queue() # needed if any 'click' event functions return generators
    gr_app.launch(share=False, show_api=False)


if __name__ == '__main__':
    app()
