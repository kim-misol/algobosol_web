from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    root: Path = Path(__file__).resolve().parents[1]
    data_dir: Path = Path(__file__).resolve().parents[1] / "data"
    attachments_dir: Path = Path(__file__).resolve().parents[1] / "data" / "attachments"
    db_path: Path = Path(__file__).resolve().parents[1] / "data" / "analyses.sqlite3"
    price_ttl_seconds: int = 30

    def ensure_dirs(self) -> "Settings":
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.attachments_dir.mkdir(parents=True, exist_ok=True)
        return self

SETTINGS = Settings().ensure_dirs()
