FROM python:3.10-slim as system

RUN apt -qq update -qq && apt -qq upgrade -qq -y
RUN apt -qq install -qq build-essential gcc git ffmpeg -y
RUN pip3 install -qq -U pip setuptools

RUN pip3 install -qq -U torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install -qq -U git+https://github.com/huggingface/transformers.git
RUN pip3 install -qq -U bitsandbytes
RUN pip3 install -qq -U huggingface_hub

RUN pip3 install -qq -U gradio
