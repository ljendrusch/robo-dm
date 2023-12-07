import json
import re
from timeit import default_timer as tt
from typing import Generator

from lib.prompt_templates import Interaction, \
    characters_prompt, species_prompt, locales_prompt, plot_prompt, acts_prompt, scenes_prompt


def gen_json_parse(gen: str, num_fields: int) -> str:
    # print(gen)
    if gen.count('"') % 2 == 1:
        print('uneven quotation marks')
    blob = '{\n    ' + gen
    blob = blob[:blob.rfind('"')+1] + '\n}'
    # print()
    # print(gen)
    # print()
    if gen.count('{') != gen.count('}'):
        print(f'uneven curly braces; {{: {gen.count("{")}, }}: {gen.count("}")}' )

    split = re.findall(r'{.*?}', blob, re.S)

    for i,o in enumerate(split):
        if o.count('",') != num_fields-1:
            print('uneven field commas')
            c = -1
            for _ in range(num_fields-1):
                for _ in range(4):
                    c = o.find('"', c+1)
                if o[c+1] != ',':
                    o = o[:c+1] + ',' + o[c+1:]
                    c += 1
            split[i] = o

    return [{k.strip().lower():v.strip().encode('ascii','ignore').decode() for k,v in json.loads(o).items()} for o in split]


class GenQueries:
    def __init__(self, model):
        self.model = model
        self.acts_re = re.compile(r'^Act \d{1,2}: .+$\n', re.M)

    def generate_characters(self, genre: str, blob: str, n: int) -> str:
        st = tt()
        gen = self.model.generate(characters_prompt(genre, blob, n)).strip()
        jo = gen_json_parse(gen,4)
        resp = '\n\n'.join([f"{e['name']}, {e['occupation']}\n- {e['personality']}\n- {e['history']}" for e in jo])
        Interaction(self.model.__class__.__name__, tt()-st, blob, resp).to_json()
        return resp

    def generate_species(self, genre: str, blob: str, n: int) -> str:
        st = tt()
        gen = self.model.generate(species_prompt(genre, blob, n)).strip()
        jo = gen_json_parse(gen,4)
        resp = '\n\n'.join([f"{e['name']}\n- {e['appearance']}\n- {e['traits']}\n- {e['culture']}" for e in jo])
        Interaction(self.model.__class__.__name__, tt()-st, blob, resp).to_json()
        return resp

    def generate_locales(self, genre: str, blob: str, n: int) -> str:
        st = tt()
        gen = self.model.generate(locales_prompt(genre, blob, n)).strip()
        jo = gen_json_parse(gen,4)
        resp = '\n\n'.join([f"{e['name']}\n- {e['geography']}\n- {e['landmarks']}\n- {e['history']}" for e in jo])
        Interaction(self.model.__class__.__name__, tt()-st, blob, resp).to_json()
        return resp

    def generate_plot(self, genre: str, chars: str, species: str, locales: str, blob: str) -> str:
        st = tt()
        chars = '\n\n'.join(['Character: ' + c.strip() for c in chars.split('\n\n') if c])
        species = '\n\n'.join(['Species: ' + s.strip() for s in species.split('\n\n') if s])
        locales = '\n\n'.join(['Locale: ' + l.strip() for l in locales.split('\n\n') if l])
        if locales:
            blob = locales + '\n\n\n' + blob
        if species:
            blob = species + '\n\n\n' + blob
        if chars:
            blob = chars + '\n\n\n' + blob
        resp = self.model.generate(plot_prompt(genre, blob))
        Interaction(self.model.__class__.__name__, tt()-st, blob, resp).to_json()
        return resp

    def generate_acts(self, genre: str, blob: str) -> str:
        st = tt()
        resp = self.model.generate(acts_prompt(genre, blob))
        Interaction(self.model.__class__.__name__, tt()-st, blob, resp).to_json()
        return resp

    def generate_scenes(self, genre: str, blob: str) -> Generator[ str, None, None ]:
        st = tt()
        blob = blob.strip()
        acts = [s.strip() for s in self.acts_re.split(blob) if s and s.strip()]
        scenes = []
        for i,act in enumerate(acts):
            scenes.append(f'Act {i+1} {self.model.generate(scenes_prompt(genre, act))}\n') ## TODO: put i into the prompt and prefill response with 'Act {n} Observational Notes:\n\n
            resp = '    ----------------------------------------------------------------\n\n'.join(scenes)
            if i == len(acts)-1:
                Interaction(self.model.__class__.__name__, tt()-st, blob, resp).to_json()
            yield resp
