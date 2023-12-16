from os import environ as os_env
os_env['TF_CPP_MIN_LOG_LEVEL'] = '4'

from argparse import ArgumentParser
from lib.app import app
from lib.globals import MODELS_L


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('model_name', type=str, choices=MODELS_L, help="name of LLM to use; one of 'Llama7b' 'Llama13b' 'Novellama13b'")
    args = parser.parse_args()

    app(args.model_name)
