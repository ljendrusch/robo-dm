from pathlib import Path
from typing import Literal


ROBODM_PATH = Path(__file__).parents[1]

D_BLURB = 'Gram discovers a looming intergalactic threat while working at a dig site. But noone will believe him.'

D_GENRE = 'science fiction'

MODELS = Literal['Llama7b', 'Llama13b', 'Novellama13b']
MODELS_L = ['Llama7b', 'Llama13b', 'Novellama13b']
MODAL_MODEL = 'Novellama13b'

HF_SECRET = 'huggingface access token here'
