from typing import Literal
from pathlib import Path
import yaml
from dataclasses import dataclass
from datetime import datetime

from llm_chat.config import ModelConfig


@dataclass
class Message:
    role: Literal["system", "user", "assistant"]
    content: str

    def json(self):
        return {"role": self.role, "content": self.content}


class Session:
    name: str
    system_prompt: str
    model_config: ModelConfig
    messages: list[Message]
    autosave: bool = False
    log_dir: Path

    def __init__(self, model_config: ModelConfig, system_prompt: str, log_dir: Path):
        self.name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.model_config = model_config
        self.system_prompt = system_prompt
        self.messages = [Message(role="system", content=system_prompt)]
        self.log_dir = log_dir / "sessions" / self.name

    @staticmethod
    def load(name: str, log_dir: str | Path):
        log_dir = Path(log_dir)
        messages_dir = log_dir / "messages.yaml"
        model_config_dir = log_dir / "model_config.yaml"
        system_prompt_dir = log_dir / "system_prompt.txt"
        session_name_dir = log_dir / "session_name.txt"
        if not log_dir.is_dir():
            raise ValueError(f"Cannot find session saved at: {log_dir}")
        if not messages_dir.is_file():
            raise ValueError(f"Cannot find messages saved at: {messages_dir}")
        if not model_config_dir.is_file():
            raise ValueError(f"Cannot find model config saved at: {model_config_dir}")
        if not system_prompt_dir.is_file():
            raise ValueError(f"Cannot find system prompt saved at: {system_prompt_dir}")
        if not session_name_dir.is_file():
            raise ValueError(f"Cannot find session name saved at: {session_name_dir}")

        with open(session_name_dir) as f:
            name = f.read()
        with open(system_prompt_dir) as f:
            system_prompt = f.read()
        with open(model_config_dir) as f:
            model_config = ModelConfig(**yaml.safe_load(f))
        with open(messages_dir) as f:
            messages = [Message(**message) for message in yaml.safe_load(f)]

        return Session(
            name=name,
            system_prompt=system_prompt,
            model_config=model_config,
            messages=messages,
        )

    def save(self):
        self.log_dir.mkdir(exist_ok=True, parents=True)
        with open(self.log_dir / "session_name.txt", "w") as f:
            f.write(self.name)
        with open(self.log_dir / "system_prompt.txt", "w") as f:
            f.write(self.system_prompt)
        with open(self.log_dir / "messages.yaml", "w") as f:
            yaml.safe_dump([m.json for m in self.messages], f)
        with open(self.log_dir / "model_config.yaml", "w") as f:
            yaml.safe_dump(self.model_config.json(), f)
