from datasets import Dataset
# import json
from math import ceil
from pathlib import Path
from typing import List, Union
import re


def dataset_clean():
    tdr_path = Path(__file__).parents[2] / 'text_data' / 'raw'

    non_asc_reg = re.compile(r'[^\x00-\x7f]')
    page_num_reg = re.compile(r'\r?\n(chapter|part|section|act)?\s*\d+\s*\r?\n', re.I)
    space_reg = re.compile(r'\s{2,}|[^\S ]')

    apos1_reg = re.compile(r'( \')|( ?`)')
    apos2_reg = re.compile(r"''")

    eos_reg = re.compile(r'([\.!?][\'"]?) ')

    for f_path in tdr_path.iterdir():
        cleaned_path = f_path.parents[2] / 'cleaned' / f_path.name

        t = f_path.read_text(errors='ignore')
        t = '\n' + non_asc_reg.sub('', t).strip() + '\n'
        t = page_num_reg.sub(' ', t).strip() + '\n'
        t = space_reg.sub(' ', t).strip() + '\n'

        t = apos1_reg.sub('\'', t)
        t = apos2_reg.sub('"', t)

        t = eos_reg.sub(r'\1\n', t)

        if t[-1] != '\n':
            t = t + '\n'

        cleaned_path.write_text(t)

def dataset_preprocess(max_token_caps = Union[ int, List[int] ]):
    if not isinstance(max_token_caps, list):
        max_token_caps = [max_token_caps]

    tdc_path = Path(__file__).parents[2] / 'text_data' / 'cleaned'

    # B_SEN, E_SEN = "<s>", "\n</s>\n\n"
    # B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
    B_INST, E_INST = "[INST]", "[/INST]"
    genre_dict = {
        '01 -': 'high fantasy, adventure',
        '02 -': 'high fantasy, adventure',
        '03 -': 'high fantasy, adventure',
        'Auel': 'epic historical fiction',
        'Clan': 'technological thriller',
        'Clar': 'science fiction',
        'Doug': 'absurdist science fiction',
        'Fran': 'military science fiction',
        'Geor': 'dystopian political science fiction',
        'Harr': 'fantasy adventure',
        'Jame': 'philosophical dystopian fiction',
        'Lloy': 'high fantasy',
        'Phil': 'dystopian science fiction',
        'Rich': 'cyberpunk',
        'Robe': 'epic high fantasy adventure',
        'Salv': 'epic high fantasy adventure',
        'Star': 'space opera',
        'Will': 'cyberpunk',
    }

    big_prompts_list = []
    for max_num_tokens in max_token_caps:
        for f_path in tdc_path.iterdir():
            title = f_path.stem
            print(title)
            t = [ tx.split() for tx in f_path.read_text().split('\n') ]

            genre = genre_dict[f_path.stem[:4]]
            prompt_tmp = f'{B_INST} Write part of a {genre} story. {E_INST} '
            m = max_num_tokens-len(prompt_tmp.split())

            prompts_list = []
            lp = 0
            while lp < len(t):
                rp = lp + 1
                while sum([len(es) for es in t[lp:rp]]) < m and rp < len(t):
                    rp += 1
                if rp - lp == 1:
                    fac = ceil(len(t[lp]) / m)
                    for i in range(fac):
                        prompts_list.append({'genre': genre, 'title': title, 'text': prompt_tmp + ' '.join(t[lp][i*m:(i+1)*m])})
                else:
                    rp -= 1
                    prompts_list.append({'genre': genre, 'title': title, 'text': prompt_tmp + ' '.join([tx for txt in t[lp:rp] for tx in txt])})
                lp = rp

            # jsp = Path(__file__).parents[1] / 'resources' / f'{f_path.stem}.json'
            # jsp.write_text(json.dumps(prompts_list, indent=2))
            big_prompts_list.extend(prompts_list)
    ds = Dataset.from_list(big_prompts_list)
    print(ds.info)
    ds.to_json(Path(__file__).parents[1] / 'resources' / f'books_{max_num_tokens}.ds.json')


if __name__ == '__main__':
    dataset_clean()
    dataset_preprocess([60, 120, 240, 480, 960])
