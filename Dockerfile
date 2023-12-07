FROM python:3.10-slim as system

RUN apt update && apt upgrade -y
RUN apt install build-essential gcc git ffmpeg -y
RUN pip3 install --upgrade pip setuptools

RUN pip3 install -U torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install -q -U git+https://github.com/huggingface/transformers.git
RUN pip3 install -q -U bitsandbytes
RUN pip3 install -q -U huggingface_hub==0.16.4
RUN pip3 install -q -U gradio

WORKDIR /home
COPY . .
