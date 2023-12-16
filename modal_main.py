from os import environ as os_env
os_env['TF_CPP_MIN_LOG_LEVEL'] = '4'

from lib.app import app
from lib.globals import MODAL_MODEL
from fastapi import FastAPI
from modal import (
    Image,
    NetworkFileSystem,
    Stub,
    gpu,
    asgi_app,
)


stub = Stub(name='robodm')
volume = NetworkFileSystem.persisted('robodm-vol')
web_app = FastAPI()
image = (
    Image.from_registry('pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime')
    .run_commands(
        'apt -qq update -qq && apt -qq upgrade -qq -y',
        'apt -qq install -qq git -y',
        # 'apt -qq install -qq build-essential gcc git ffmpeg wget software-properties-common -y',
        'pip3 install -qq -U pip setuptools',
        'pip3 install -qq -U git+https://github.com/huggingface/transformers.git',
        'pip3 install -qq -U git+https://github.com/huggingface/accelerate.git',
        'pip3 install -qq -U bitsandbytes huggingface_hub gradio protobuf scipy',
    )
)

@stub.function(
    gpu=gpu.T4(count=1),
    image=image,
    network_file_systems={'/models': volume},
    timeout=86400,
)
@asgi_app()
def fastapi_app():
    from gradio.routes import mount_gradio_app

    interface = app(MODAL_MODEL, True)
    return mount_gradio_app(
        app=web_app,
        blocks=interface,
        path='/',
    )
