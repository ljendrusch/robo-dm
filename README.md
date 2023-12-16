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
- forgot their d20
- runs a version of the open-source LLM Llama2 either locally on one's computer, or remotely on a simple and low-cost cloud computing service
- uses said LLM to expound on minimal-to-no user input to generate well-fleshed-out story content
- generates story content in interactive steps; one can edit the generated content and such edits will be reflected in later steps


## Usage

Robo-DM can be ran locally or remotely. Running locally requires a high-end Nvidia GPU, while running remotely requires an account with the cloud
computing service Modal, and perhaps a few bucks off your bank card.

#### Running Locally

If you have a modern Nvidia GPU with 6 GB or more VRAM, you can run Robo-DM locally with the base Llama2 7b model.
If you have a modern Nvidia GPU with 10 GB or more VRAM, you can run Robo-DM locally with Llama2 7b, 13b, or my modified Novellama 13b model.
The following instructions are for a WSL2 development environment; details may vary for other environments.

**Check GPU VRAM**

- Nvidia Control Panel
    Open Nvidia Control Panel
    Click on 'Help' and 'System Information'
    Scroll down in 'Details' to find 'Dedicated video memory'
    'Dedicated video memory' divided by 1000 is your GPU's VRAM in GB
- Windows
    Ctrl + R to open Run
    enter 'dxdiag'
    click 'Display' tab
    'Display Memory (VRAM)' divided by 1000 is your GPU's VRAM in GB

**Dependencies**

- Nvidia toolkit and CUDA
    [Install WSL2 on Windows 11 with NVIDIA CUDA 11.8](https://www.youtube.com/watch?v=1HzYU2_t3yc)
- Install Python dependencies

    ```pip install -r requirements.txt```

**Run**

```python3 main.py```

    or

```python main.py```

Open the IP address and port that appears in the terminal, example:

```Running on local URL:  http://127.0.0.1:7860```

**Close**

Ctrl + C in the terminal


