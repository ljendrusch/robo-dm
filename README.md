## Motivation

This project is designed with two primary motivations in mind:
- Make an assistant to assist and inspire fans of tabletop role-playing games in fulfilling the role of the 'Dungeon Master'
- Make an open-source codebase to serve as a guide for programmers to explore modern techniques of interfacing with AI and Large Language Models

### On Motivation 1: Dungeon Master Inspiration / Assistance

**Background**: Tabletop role-playing games (TTRPG's) have experienced numerous explosive rises in player population and general public interest
over the past few decades. TTRPG's such as Dungeons and Dragons (D&D), Shadowrun, FATE, etc. are played by groups of friends around a table in a
comfortable living room, or perhaps over group video chat. It's easy, wholesome fun, but there are problems; one of these friends has to take on
the role of the *Dungeon Master* (DM), and is held responsible for puppeting the game's world. The DM can either buy an adventure guide book that
has a premade world, plot, characters, locations, factions, faiths, encounters, monsters, bad guys, etc. or they have to create and design all of
that content themselves. The former option (using an adventure guide) is obviously easier but there are limited options and can make for an
'on-rails' experience for the table; players must stay on the defined path of the adventure guide, which often feels confining. The latter option
(the DM making an entire game world themselves) is akin to a part-time job, but if done well it often leads to wonderful experiences for all
friends at the table. Either way, the friend that assumes the role of DM has a huge workload to shoulder. This huge workload gives rise to another
problem: everyone wants to play TTRPG's but noone wants to be the DM. I reckon a spitball statistic splitting the TTRPG player population holds
that about 1 in 20 TTRPG players are willing to take on the role of DM.

**Robo-DM's role**: Robo-DM endeavors to greatly reduce the work required of a DM by helping them create world props (characters, species, notable
places, etc.), adventure plot summary, adventure acts summaries, and scene elements per act. Interactively-generated content from Robo-DM can serve
as a foundation for, or inspiration for, a novel, storyboard, or custom TTRPG adventure. If TTRPG fans know about tools to lessen the burdon of
being a DM - tools like Robo-DM - exist, they will be more likely to volunteer to take up the role of DM, and the TTRPG playerbase should pivot to
a more even ratio.

### On Motivation 2: Democratization of AI and Large Language Models (LLM's)

**Background**: Programmers hear 'AI' and 'LLM' and think 'that's too complex, I'll just pay big brother to query their models.' And this sentiment
of reservedness towards AI has been the proper approach before the advent of recent tools and storage and sharing services targeting the computer
science discipline of AI / ML. Coding AI from scratch is exceptionally difficult, reserved only for the most passionate, dedicated, and capable
programmers, such as members of PhD-level research and development teams of leading tech companies. However, tools and abstractions that have been
developed in the last couple of years have made it easy - even practical - for any programmer to use, modify, perhaps even create their own AI or
LLM models from building-block abstractions. With decent hardware - namely a modern high-end Nvidia GPU - a journeyman programmer can even do this
at home, on their own computer, at zero cost.

**Robo-DM's role**: Robo-DM, as an open-source project and codebase, endeavors to share the good word: *AI is within your reach, just do like I do.*
I hope this code is shared widely to serve as a foundation for or inspiration for people to begin their own journeys exploring the world of AI and
LLM's. Together, we can create the perfect Skynet.

**Note**: Some of the most influential of the tools, abstractions, techniques, services, etc. that have bridged the gap to making AI programming
approachable are shared in [misc/Resources.md](misc/Resources.md).


## Overview

*Robo-DM...*

- is a novel, storyboard, and TTRPG adventure writing assistant

- forgot their d20, do you have a spare?

- runs a version of the open-source LLM Llama2 either locally on one's computer, or remotely on a simple and low-cost cloud computing service

- uses said LLM to expound on minimal-to-no user input to generate well-fleshed-out story content

- generates story content in interactive steps; one can edit the generated content and such edits will be reflected in later steps


## Usage

Robo-DM can be ran locally or remotely. Running locally requires a high-end Nvidia GPU, while running remotely requires an account with the cloud
computing service Modal, and perhaps a few bucks off your bank card. Note: The first time you use a certain model, you may have to download it.
This process is automated, but the download may be 24 GB and thus will take some time and harddrive real estate.


**Add Huggingface Access Token**:

Go to [huggingface.co](https://huggingface.co) and make an account

Go to your email and confirm your registration

Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens); click new token, name it whatever, set it to 'read'

Copy the token to clipboard (should be a string like 'hf_QkfV................')

Paste the token in [lib/globals.py](lib/globals.py) HF_SECRET, example:

```
HF_SECRET = 'hf_QkfV.......'
```


**Access Llama Models**:

To use Llama2 7b or 13b you need to get access from the model creator, meta. To do so, complete the following steps.

Fill out the meta form first; the email you use must match your huggingface account email

[ai.meta.com/resources/models-and-libraries/llama-downloads/](https://ai.meta.com/resources/models-and-libraries/llama-downloads/)

Next go to this site. There's a card up top with the title 'Access Llama 2 on Hugging Face;' check the box and press submit

[huggingface.co/meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)

Note: Can take over a day to go through, but usually takes only a couple hours


## Running Locally

If you have a modern Nvidia GPU with 6 GB or more VRAM, you can run Robo-DM locally with the base Llama2 7b model.

If you have a modern Nvidia GPU with 10 GB or more VRAM, you can run Robo-DM locally with Llama2 7b, 13b, or my modified Novellama 13b model.

Note: Generated content is saved in a rudimentary for in [robo-dm/interactions](robo-dm/interactions); it may be pertinent to instead save content you like by copying
it with Ctrl + A, Ctrl + C, then pasting it into a text document or similar, and saving it there.

The following instructions are for a WSL2 development environment; details may vary for other environments.


**Check GPU VRAM**:

- Nvidia Control Panel

    ```
    Open Nvidia Control Panel
    Click on 'Help' and 'System Information'
    Scroll down in 'Details' to find 'Dedicated video memory'
    'Dedicated video memory' divided by 1000 is your GPU's VRAM in GB
    ```

- Windows

    ```
    Ctrl + R to open Run
    enter 'dxdiag'
    click 'Display' tab
    'Display Memory (VRAM)' divided by 1000 is your GPU's VRAM in GB
    ```


**Dependencies**:

- Nvidia toolkit and CUDA

    [Install WSL2 on Windows 11 with NVIDIA CUDA 11.8](https://www.youtube.com/watch?v=1HzYU2_t3yc)

- Install Python dependencies

    ```pip install -r requirements.txt```


**Run**:

```
python3 main.py Llama7b
    or
python3 main.py Llama13b
    or
python3 main.py Novellama13b
```

Open the IP address and port that appears in the terminal, example:

```Running on local URL:  http://127.0.0.1:7860```


**Close**:

Ctrl + C in the terminal


## Running Remote via Modal

Anyone and everyone can run Robo-DM using modal. Modal is exceptionally easy to use with Python projects, and is much lower cost than big-name
competitors. You get a $30 credit per month, and you'd have to do a lot of Robo-DM'ing to overtake that mark. You do have to cough up your card
number to make an account though, and you need a github account to make a modal account. Also, it may take around 30 minutes to get Robo-DM
running the first time you run it on modal, and around 15 minutes the first time you use any alternate model. Modal needs to construct and
compile a container and download the model you wish to use to modal servers. Note: The actual Robo-DM website will automatically close after
24 hours, and doesn't currently save its content anywhere. If you want to keep a story you've generated, copy the text with Ctrl + A, Ctrl + C,
paste it into a text document or similar, and save it there.


**Make a Modal Account**:

Login or register on (github.com)[https://github.com/]

Create an account on (modal.com)[https://modal.com/]

Go to your email and confirm your registration


**Make a Modal Token**:

In a terminal, enter

```
modal token new
```


**Deploy Robo-DM to Modal**:

This step readies a container on modal. There may be a roughly 15 minute compile timer. In a terminal, enter

```
modal serve modal_main.py
```

This step runs the container. There may be a roughly 15 minute model download time. Open the website that appears in the terminal, example:

```
Created fastapi_app => https://ljendrusch--robodm-fastapi-app-dev.modal.run
```

This step will finally open Robo-DM in your browser. Open the website that appears in the terminal, example:

```
Running on public URL: https://99527e444cca905a81.gradio.live
```

Modal is set to use model 'Novellama13b.' If you want to use a different model, change [lib/globals.py](lib/globals.py) MODAL_MODEL, example:

```
MODAL_MODEL = 'Llama7b'
    or
MODAL_MODEL = 'Llama13b'
```


**Close Modal-deployed Robo-DM**:

Ctrl + C in the terminal
