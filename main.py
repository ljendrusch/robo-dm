from os import environ as os_env
os_env['TF_CPP_MIN_LOG_LEVEL'] = '4'
# from argparse import ArgumentParser

from lib.app import app
# from lib.modal_app import modal_app


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

if __name__ == '__main__':
    app('Llama7b')
