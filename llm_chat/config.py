import os
import yaml
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ModelConfig:
    model_name: str
    api_kind: str
    model_kind: str
    endpoint: str
    args: dict

    def json(self):
        return {
            "model_name": self.model_name,
            "api_kind": self.api_kind,
            "model_kind": self.model_kind,
            "endpoint": self.endpoint,
            "args": self.args,
        }

@dataclass
class SystemPrompt:
    prompt_name: str
    content: str

    def json(self):
        return {
            "prompt_name": self.prompt_name,
            "content": self.content,
        }


@dataclass
class AppConfig:
    models: dict[str, ModelConfig]
    system_prompts: dict[str, str]
    log_dir: Path

    def __post_init__(self):
        self.log_dir.mkdir(exist_ok=True, parents=True)

    @staticmethod
    def load(conf_dir: Path):
        models = {}
        for file in conf_dir.glob("models/*.yaml"):
            with open(file) as f:
                model_config = ModelConfig(**yaml.safe_load(f))
                models[model_config.model_name] = model_config

        system_prompts = {}
        for file in conf_dir.glob("system_prompts/*.yaml"):
            with open(file) as f:
                system_prompt = SystemPrompt(**yaml.safe_load(f))
                system_prompts[system_prompt.prompt_name] = system_prompt

        log_dir = Path.home() / ".llm-chat"
        if "LLM_CHAT_LOGDIR" in os.environ:
            log_dir = Path(os.environ["LLM_CHAT_LOGDIR"])

        return AppConfig(
            models=models,
            system_prompts = system_prompts,
            log_dir=log_dir,
        )
