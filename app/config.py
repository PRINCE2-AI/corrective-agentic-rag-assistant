from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # Allows tests and local demo to run before installing extras.
    def load_dotenv() -> None:
        return None


load_dotenv()


@dataclass(frozen=True)
class Settings:
    project_root: Path = Path(__file__).resolve().parents[1]
    chroma_path: Path = Path(os.getenv("CHROMA_PATH", "data/index/chroma"))
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "mistral")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    default_top_k: int = int(os.getenv("DEFAULT_TOP_K", "5"))
    crag_upper_threshold: float = float(os.getenv("CRAG_UPPER_THRESHOLD", "0.5"))
    crag_lower_threshold: float = float(os.getenv("CRAG_LOWER_THRESHOLD", "-0.8"))

    @property
    def resolved_chroma_path(self) -> Path:
        if self.chroma_path.is_absolute():
            return self.chroma_path
        return self.project_root / self.chroma_path


settings = Settings()
