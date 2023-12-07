import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '4'

from pathlib import Path
from typing import List, Optional, Tuple
from fastapi import FastAPI
from modal import (
    Image,
    Mount,
    NetworkFileSystem,
    Stub,
    gpu,
    asgi_app,
)

from lib.app import app
from lib.gen_funcs import GenQueries
from lib.models import model_switch#Llama7b, Llama13b, Novellama13b


# def parse_cli() -> None:
#     parser = ArgumentParser()
#     run_location = parser.add_mutually_exclusive_group(required=True)
#     run_location.add_argument('-l', '--local', action='store_true', help='run RoboDM on local GPU')
#     run_location.add_argument('-r', '--remote', action='store_true', help='run RoboDM on modal.com')
#     args = parser.parse_args()

#     if args.local:
#         app()
#     elif args.remote:
#         modal_app()

# from modal import Image, Mount, Stub, gpu
# stub = Stub('robodm')
# dockerfile_image = Image.from_dockerfile('Dockerfile')
# @stub.function(gpu=gpu.T4(count=1), image=dockerfile_image)
# def main():
#     app()

# if __name__ == '__main__':
#     main()







stub = Stub(name='robodm')
image = Image.from_dockerfile('Dockerfile')
volume = NetworkFileSystem.persisted('robodm-vol')
MODEL_PATHS: List[ Path ] = [
    Path('/home/lj/.cache/huggingface/hub/models--meta-llama--Llama-2-7b-chat-hf'),
    Path('/home/lj/.cache/huggingface/hub/models--meta-llama--Llama-2-13b-chat-hf'),
    Path('/home/lj/.cache/huggingface/hub/models--LJ--Llama-2-13b-fantasy-finetune')]

@stub.function(
    image=image,
    network_file_systems={m._str: volume for m in MODEL_PATHS},
    mounts=[Mount.from_local_dir(m, remote_path="/assets") for m in MODEL_PATHS],
)
@asgi_app()
def fastapi_app():
    from gradio.routes import mount_gradio_app

    llm = GenQueries(model_switch('llama7b'))
    interface = app(llm)
    return mount_gradio_app(
        app=FastAPI(),
        blocks=interface,
        path="/",
    )
