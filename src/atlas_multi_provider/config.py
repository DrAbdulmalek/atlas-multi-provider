"""Environment-based configuration with no implicit provider switching."""
from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Mapping
from .errors import ConfigurationError

SUPPORTED_PROVIDERS = ("deepseek", "zai")

@dataclass(frozen=True)
class ProviderConfig:
    provider: str
    api_key: str
    base_url: str
    model: str
    timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        if self.provider not in SUPPORTED_PROVIDERS:
            raise ConfigurationError(f"Unsupported provider {self.provider!r}; choose one of {SUPPORTED_PROVIDERS}.")
        if not self.api_key.strip():
            raise ConfigurationError(f"API key is missing for provider {self.provider!r}.")
        if not self.base_url.strip():
            raise ConfigurationError(f"Base URL is missing for provider {self.provider!r}.")
        if not self.model.strip():
            raise ConfigurationError(f"Model is missing for provider {self.provider!r}.")
        if self.timeout_seconds <= 0:
            raise ConfigurationError("timeout_seconds must be greater than zero.")

def load_config(environ: Mapping[str, str] | None = None, *, provider: str | None = None) -> ProviderConfig:
    """Load one explicitly selected provider from environment variables."""
    env = os.environ if environ is None else environ
    selected = (provider or env.get("ATLAS_PROVIDER", "deepseek")).strip().lower()
    if selected not in SUPPORTED_PROVIDERS:
        raise ConfigurationError(f"Unsupported provider {selected!r}; choose one of {SUPPORTED_PROVIDERS}.")
    prefix = "DEEPSEEK" if selected == "deepseek" else "ZAI"
    try:
        timeout = float(env.get("ATLAS_TIMEOUT_SECONDS", "30"))
    except (TypeError, ValueError) as exc:
        raise ConfigurationError("ATLAS_TIMEOUT_SECONDS must be a number.") from exc
    return ProviderConfig(
        provider=selected,
        api_key=env.get(f"{prefix}_API_KEY", ""),
        base_url=env.get(f"{prefix}_BASE_URL", "").strip(),
        model=env.get(f"{prefix}_MODEL", "").strip(),
        timeout_seconds=timeout,
    )
