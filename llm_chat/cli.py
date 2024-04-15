import dotenv
import os
from pathlib import Path

from .state import AppState
from .config import AppConfig
from .parser import initialize_parser
from .paths import CONFIG_DIR


dotenv.load_dotenv()

help_message = (
    "Commands:\n"
    "q, quit: exit application\n"
    "h, help: view help message\n"
    "l, load: load session\n"
    "e, edit: edit history\n"
    "m, model: edit model configuration\n"
)


def run() -> None:
    config = AppConfig.load(CONFIG_DIR)
    state = AppState(config=config)
    parser = initialize_parser(state)
    parser.run()

    print("Goodbye!")


if __name__ == "__main__":
    run()
