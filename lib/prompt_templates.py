from dataclasses import dataclass, asdict
from datetime import datetime
import json

from lib.globals import ROBODM_PATH
from lib.utils import int2words


def characters_prompt(genre: str, blurb: str, n: int) -> str:
    pr =  f'''[INST] <<SYS>>
You are a {genre} author. Create unique and dynamic characters, be they hero, antihero, villain, or other.

Do not write any first-person commentary or dialogue. Respond only with the contents of the character descriptions.
<</SYS>>

The following is a character description json object:
{{
    "name": String,
    "occupation": String,
    "personality": String,
    "history": String
}}

Create {int2words(n)} character description json {'object' if n == 1 else 'objects'}.'''
    if blurb and len(blurb.split()) > 4:
        pr = pr + f'''

Preliminary character information includes the following:

{blurb}'''
    return pr + f''' [/INST]
Sure! Here {'is' if n == 1 else 'are'} {int2words(n)} character description json {'object' if n == 1 else 'objects'} for {'a unique and dynamic character' if n == 1 else 'unique and dynamic characters'}:

{{
    '''


def species_prompt(genre: str, blurb: str, n: int) -> str:
    pr =  f'''[INST] <<SYS>>
You are a {genre} author. Create unique and dynamic species, be they elegant, monstrous, supernatural, or other.

Do not write any first-person commentary or dialogue. Respond only with the contents of the species descriptions.
<</SYS>>

The following is a species description json object:
{{
    "name": String,
    "appearance": String,
    "traits": String,
    "culture": String
}}

Create {int2words(n)} species description json {'object' if n == 1 else 'objects'}.'''
    if blurb and len(blurb.split()) > 4:
        pr = pr + f'''

Preliminary species information includes the following:

{blurb}'''
    return pr + f''' [/INST]
Sure! Here {'is' if n == 1 else 'are'} {int2words(n)} species description json {'object' if n == 1 else 'objects'} for {'a unique and dynamic species' if n == 1 else 'unique and dynamic species'}:

{{
    '''


def locales_prompt(genre: str, blurb: str, n: int) -> str:
    pr =  f'''[INST] <<SYS>>
You are a {genre} author. Create unique and dynamic locales, be they bustling cities, barren wastelands, verdant forests, hungering voids, or other.

Do not write any first-person commentary or dialogue. Respond only with the contents of the place descriptions.
<</SYS>>

The following is a locale description json object:
{{
    "name": String,
    "geography": String,
    "landmarks": String,
    "history": String
}}

Create {int2words(n)} locale description json {'object' if n == 1 else 'objects'}.'''
    if blurb and len(blurb.split()) > 4:
        pr = pr + f'''

Preliminary locale information includes the following:

{blurb}'''
    return pr + f''' [/INST]
Sure! Here {'is' if n == 1 else 'are'} {int2words(n)} locale description json {'object' if n == 1 else 'objects'} for {'a unique and dynamic locale' if n == 1 else 'unique and dynamic locales'}:

{{
    '''


def plot_prompt(genre: str, blurb: str) -> str:
    pr =  f'''[INST] <<SYS>>
You are a {genre} author. Use story elements given to you and write stories that are descriptive and impactful.

Don't write any first-person commentary or dialogue. Respond only with the contents of the story.
<</SYS>>

Story elements include the following:

{blurb}

Write this story's plot. Don't write a title. [/INST]'''
    return pr


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

Don't write any first-person commentary or dialogue. Respond only with the contents of the story.
<</SYS>>

Write a plot for this story's '{prompt_acts[i]}'.

Story elements include the following:

{blurb} [/INST]'''
    return pr


def acts_prompt(genre: str, blurb: str) -> str:
    pr =  f'''[INST] <<SYS>>
You are a {genre} author. Use story elements given to you and write stories that are descriptive and impactful.

Don't write any first-person commentary or dialogue. Respond only with the contents of the story.
<</SYS>>

Story elements include the following:

{blurb}

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

Write a plot for each act of the monomyth narrative. [/INST]'''
    return pr


def scenes_prompt(genre: str, blurb: str) -> str:
    pr = f'''You are an explorer in a world of {genre}. You write in a staccato, fanciful scrawl. Document observations on scenes that you encounter on your expedition.

Don't write any first-person commentary or dialogue. Respond only with the contents of your observations.
<</SYS>>

On your expedition you recently heard the following story:

"{blurb}"

Observational notes are composed of the following sections:
Flora
Fauna
Environs
Populations
Architecture

Write short and specific observations of scenes that you've encountered on your expedition as bullet points to observational notes. [/INST]'''
    return pr



@dataclass
class Interaction:
    model: str
    runtime: float
    prompt: str
    response: str

    def to_json(this):
        json_path = ROBODM_PATH / 'interactions' / this.model / datetime.now().strftime("%m.%d") / f'i{datetime.now().strftime("%m.%d.%y.%H:%M:%S")}.json'
        json_path.parent.mkdir(parents=True, exist_ok=True)
        out = asdict(this)

        json_str = json.dumps(out, indent=2)
        json_path.write_text(json_str)
