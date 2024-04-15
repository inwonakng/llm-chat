from pathlib import Path
import yaml
from datetime import datetime
import shutil

from .session import Session
from .config import AppConfig


class AppState:
    config: AppConfig
    current_model: str
    current_session: Session
    sessions_by_name: dict[str, str]

    def __init__(self, config: AppConfig):
        self.config = config
        self.current_model = list(self.config.models.keys())[0]
        self.session = Session(
            model_config = self.config.models[self.current_model],
            system_prompt = self.config.system_prompts["default"].content,
            log_dir = self.config.log_dir,
        )
        self.sessions_by_name = {}

    def load_saved_sessions(self):
        for sname in self.config.log_dir.glob("sessions/*/session_name.txt"):
            with open(sname) as f:
                self.sessions_by_name[f.read()] = sname.parent.name

    def save(self):
        self.session.save()
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        log_dir = self.config.log_dir / "app_state" / f"{timestamp}.yaml"
        log_dir.parent.mkdir(exist_ok=True, parents=True)
        with open(log_dir, "w") as f:
            yaml.safe_dump(
                {
                    "config": self.config,
                    "current_model": self.current_model,
                    "current_session": self.session.log_dir,
                    "sessions_by_name": self.sessions_by_name,
                },
                f,
            )

    @staticmethod
    def load_or_create(config: AppConfig):
        state = AppState(config=config)
        if not (config.log_dir / "app_state.yaml").is_file():
            return state

        with open(config.log_dir / "app_state.yaml") as f:
            saved_state = yaml.safe_load(f)

        if saved_state.get("current_model") is None:
            print("No current model found, will use default..")
        else:
            state.current_model = saved_state["current_model"]

        if saved_state.get("current_session") is None:
            print("No current session found, will create new..")
        else:
            state.current_session = Session.load(saved_state["current_session"])

        if saved_state.get("sessions_by_name") is None:
            print("No sessions found, will reload..")
        else:
            state.sessions_by_name = saved_state["sessions_by_name"]

        return state

    def purge(self):
        shutil.rmtree(self.config.log_dir)
