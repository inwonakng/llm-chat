from pathlib import Path
from datetime import datetime

class Logger:
    log_dir: Path
    sessions_file: Path

    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        log_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_file = log_dir / "sessions.json"
        if not self.sessions_file.is_file():
            ...


