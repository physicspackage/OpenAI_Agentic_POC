from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    practice_name: str = os.getenv("PRACTICE_NAME", "BrightSmile Dental")
    backend_base_url: str = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
    model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


settings = Settings()
