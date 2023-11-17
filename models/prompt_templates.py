from dataclasses import dataclass, asdict
from datetime import datetime
import json
from os import makedirs
from pathlib import Path



def characters_prompt(genre: str, blurb: str, n: int) -> str:
    pr =  f'''[INST] <<SYS>>
You are a {genre} author. Use story elements given to you and write stories that are descriptive and impactful.

Don't write dialogue. Respond only with contents of the story.
<</SYS>>

Name and create {n} characters and write short backstories for each, including history, occupation, personality, etc.'''
    if blurb and len(blurb.split()) > 4:
        pr = pr + f'''

Preliminary character information includes the following:

{blurb}'''
    return pr + ' [/INST]'


def species_prompt(genre: str, blurb: str, n: int) -> str:
    pr =  f'''[INST] <<SYS>>
You are a {genre} author. Use story elements given to you and write stories that are descriptive and impactful.

Don't write dialogue. Respond only with contents of the story.
<</SYS>>

Name and create {n} distinct species and write short backstories for each, including appearance, culture, tendencies, etc.'''
    if blurb and len(blurb.split()) > 4:
        pr = pr + f'''

Preliminary species information includes the following:

{blurb}'''
    return pr + ' [/INST]'


def places_prompt(genre: str, blurb: str, n: int) -> str:
    pr =  f'''[INST] <<SYS>>
You are a {genre} author. Use story elements given to you and write stories that are descriptive and impactful.

Don't write dialogue. Respond only with contents of the story.
<</SYS>>

Create and name {n} places and write short backstories for each, including notable geographic features, history, landmarks, etc.'''
    if blurb and len(blurb.split()) > 4:
        pr = pr + f'''

Preliminary place information includes the following:

{blurb}'''
    return pr + ' [/INST]'


prompt_acts = [
    'Act 1: Ordinary world',
    'Act 2: Call to adventure',
    'Act 3: Refusal of the call',
    'Act 4: Meeting with the mentor',
    'Act 5: Crossing the first threshold',
    'Act 6: Tests, allies, and enemies',
    'Act 7: Approach to the inmost cave',
    'Act 8: The ordeal',
    'Act 9: Reward',
    'Act 10: The road back',
    'Act 11: The resurrection',
    'Act 12: Return with the elixir',
]

def iter_acts_prompt(genre: str, blurb: str, i: int) -> str:
    pr =  f'''[INST] <<SYS>>
You are a {genre} author. Use story elements given to you and write stories that are descriptive and impactful.

Don't write dialogue. Respond only with contents of the story.
<</SYS>>

Write a plot for this story's '{prompt_acts[i]}'.

Story elements include the following:

{blurb} [/INST]'''
    return pr


def acts_prompt(genre: str, blurb: str) -> str:
    pr =  f'''[INST] <<SYS>>
You are a {genre} author. Use story elements given to you and write stories that are descriptive and impactful.

Don't write dialogue. Respond only with contents of the story.
<</SYS>>

The monomyth narrative is composed of the following acts:
Act 1: Ordinary world
Act 2: Call to adventure
Act 3: Refusal of the call
Act 4: Meeting with the mentor
Act 5: Crossing the first threshold
Act 6: Tests, allies, and enemies
Act 7: Approach to the inmost cave
Act 8: The ordeal
Act 9: Reward
Act 10: The road back
Act 11: The resurrection
Act 12: Return with the elixir

Write a plot for each act of the monomyth narrative using the following story elements:

{blurb}

Plots of each act should be at least two sentences long. [/INST]'''
    return pr


def scenes_prompt(genre: str, blurb: str) -> str:
    pr = f'''You are an explorer in a world of {genre}. You write in a staccato, fanciful scrawl. Document your observations on the scenes that you encounter on your expedition.

Don't write any first-person commentary. Respond only with the contents of your observations.
<</SYS>>

Observational notes are composed of the following headings:
Flora
Fauna
Environs
Populations
Architecture

On your expedition you recently heard the following story:

"{blurb}"

Write short and specific observations of scenes that you've encountered on your expedition as bullet points to observational notes headings. [/INST]'''
    return pr



@dataclass
class Interaction:
    model_name: str
    runtime: float
    prompt: str
    response: str

    def to_json(this):
        json_path = Path(__file__).parents[1] / 'interactions' / this.model_name / f'i{datetime.now().strftime("%m.%d.%y.%H:%M:%S")}.json'
        makedirs(json_path.parent, exist_ok=True)
        out = asdict(this)

        json_str = json.dumps(out, indent=2)
        json_path.write_text(json_str)
