import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

def get_env_vars(name, default):
    env = os.environ.get(name)
    if env is None:
        if default is None:
            raise ValueError("Ne peut être vide.")
        return default
    return env
