from rich.markdown import Markdown
from rich.prompt import Prompt
import yaml

from llm_chat.config import ModelConfig
from llm_chat.console import console
from llm_chat.state import AppState
from llm_chat.paths import CONFIG_DIR


def is_model_name_valid(model_name: str, available_models: list[str]) -> bool:
    return model_name not in available_models and not " " in model_name


def add_model(*args, state: AppState) -> None:
    model_name = " "
    while not is_model_name_valid(model_name, list(state.config.models.keys())):
        model_name = console.input("> Please enter a name: ")
    if model_name == "":
        print("cancelled")
        return
    print(f"Adding model: {model_name}")
    config_api_kinds = list(set(m.api_kind for m in state.config.models.values()))
    config_model_kinds = list(set(m.model_kind for m in state.config.models.values()))
    config_endpoints = list(set(m.endpoint for m in state.config.models.values()))

    api_kind = Prompt.ask(
        "Type of API", choices=config_api_kinds + ["other"], default=config_api_kinds[0]
    )
    if api_kind == "other":
        api_kind = Prompt.ask("Please type the API type")
    model_kind = Prompt.ask(
        "Type of Model",
        choices=config_model_kinds + ["other"],
        default=config_model_kinds[0],
    )
    if model_kind == "other":
        model_kind = Prompt.ask("Please type the Model type")
    if model_kind.lower() == "openai":
        endpoint = "https://api.openai.com/v1/chat/completions"
    else:
        endpoint = Prompt.ask("endpoint")

    args = {}
    if model_kind.lower() == "openai":
        args["model"] = Prompt.ask("Name of Model", default=model_name)

    add_args = Prompt.ask(
        "Add additional arguments? (y/n) or Enter for n. You can finish by pressing enter"
    )
    if add_args.lower() == "y":
        while True:
            arg_key = Prompt.ask("Add additional arguments? (y/n) or Enter for n")
            if arg_key == "":
                break
            arg_value = Prompt.ask("Add additional arguments? (y/n) or Enter for n")
            args[arg_key] = arg_value

    new_config = ModelConfig(
        api_kind=api_kind,
        model_kind=model_kind,
        endpoint=endpoint,
        args=args,
    )

    yaml.safe_dump(new_config.json(), open(CONFIG_DIR / f"models/{model_name}.yaml", "w"))

    state.config.models.append(new_config)
    print(state.config)
    console.print(f"Model [{model_name}] added successfully")


def list_model(*args, state: AppState) -> None:
    buffer = "Available models:\n" + "\n\n".join(
        (
            f"- **{model_config.model_name}**"
            if model_config.model_name == state.current_model
            else f"- {model_config.model_name}"
        )
        for model_config in state.config.models.values()
    )
    console.print(Markdown(buffer))


def select_model(*args, state: AppState) -> str:
    list_model(state=state)
    selected_model = Prompt.ask(
        "> Please select a model",
        choices=[m.model_name for m in state.config.models.values()],
    )
    state.current_model = selected_model
