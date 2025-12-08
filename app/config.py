import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    
    # Project Paths
    # __file__ = app/config.py
    # parent = app/
    # parent.parent = l/ (Project Root)
    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent
    DATA_DIR: ClassVar[Path] = BASE_DIR / "data"
    
    GEMINI_API_KEY: str
    API_SECRET_KEY: str = "default-insecure-key"
    GEMINI_MODEL: str = "gemini-1.5-flash-latest"

    def ensure_dirs(self):
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        (self.DATA_DIR / "logs").mkdir(parents=True, exist_ok=True)
        (self.DATA_DIR / "docs").mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.ensure_dirs()