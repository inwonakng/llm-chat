from rich.markdown import Markdown
from rich.console import Console

from .state import AppState
from .operations.model import add_model, list_model, select_model
from .operations.session import new_session, load_session, save_session
from .operations.operation import Operation

TAB = " " * 2


def build_help_message(key: str, cursor: dict[str, any] | Operation, depth=0):
    if isinstance(cursor, Operation):
        return TAB * depth + f"- *{key}*: {cursor.help_text}"
    else:
        return (
            TAB * depth
            + f"- {key}\n\n"
            + "\n\n".join(
                build_help_message(k, v, depth + 1) for k, v in cursor.items()
            )
        )


class Parser:
    state: AppState
    parse_tree: dict[str, any]
    console: Console
    help_message: Markdown

    def __init__(self, state: AppState):
        self.state = state
        self.parse_tree = {}
        self.console = Console()

    def register(self, path, func, help_text):
        cursor = self.parse_tree
        for i, key in enumerate(path):
            if i == len(path) - 1:
                cursor[key] = Operation(" ".join(path), func, help_text)
                continue
            if cursor.get(key) is None:
                cursor[key] = {}
            cursor = cursor[key]

    def prepare_help_message(self):
        self.help_message = Markdown(
            "### LLM Chat Help\n\n"
            + "*press `q` or type `quit` to exit application*\n\n"
            + build_help_message("**Commands**", self.parse_tree)
        )

    def handle(self, user_input):
        commands = user_input.split()
        cursor = self.parse_tree
        for i, key in enumerate(commands):
            if isinstance(cursor.get(key), Operation):
                cursor[key](*commands[i + 1 :], state=self.state)
            else:
                cursor = cursor.get(key)
                if cursor is None:
                    self.console.print(Markdown("Invalid command: `user_input`"))
                    break

    def input(self):
        user_input = self.console.input("> ").strip()
        return user_input

    def show_help_message(self):
        self.console.print(self.help_message)

    def run(self):
        exit_loop = False
        while not exit_loop:
            user_input = self.input()
            if not user_input: continue
            commands = user_input.split()
            if commands[0] in ["q", "quit"]:
                exit_loop = True
            elif commands[0] in ["h", "help"]:
                self.show_help_message()
            else:
                self.handle(user_input)


def initialize_parser(
    state: AppState,
) -> tuple[Parser]:
    parser = Parser(state=state)

    parser.register(["model", "list"], list_model, "Add a new model")
    parser.register(["model", "add"], add_model, "List models")
    parser.register(["model", "select"], select_model, "Select model")

    parser.prepare_help_message()

    return parser
