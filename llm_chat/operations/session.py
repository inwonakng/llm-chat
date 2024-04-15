from pathlib import Path
from rich.markdown import Markdown

from llm_chat.state import AppState
from llm_chat.session import Session
from llm_chat.console import console


def new_session(*args, state: AppState):
    new_session = Session(
        model_config=state.config.models[state.current_model],
        system_prompt=state.config.system_prompts["default"],
        log_dir=state.config.log_dir,
    )
    state.session = new_session


def load_session(log_dir: Path, *, state: AppState):
    loaded_session = Session.load(log_dir)
    state.session = loaded_session


def save_session(*args, state: AppState, save_name = None): 
    if save_name is not None:
        state.session.name = save_name
    state.session.save()

def check_session(*args, state: AppState):
    console.print(Markdown(f"Current session: `{state.session.name}`"))

def list_session(*args, state: AppState):
    buffer = "Available sessions:\n" + "\n".join(
        f"\n- {session}"
        for session in state.sessions_by_name
    )
    console.print(Markdown(buffer))
