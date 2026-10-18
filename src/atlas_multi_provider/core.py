"""Shared public client and normalized chat response."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .config import ProviderConfig
from .errors import ConfigurationError
from .providers import OpenAICompatibleAdapter

@dataclass(frozen=True)
class ChatResponse:
    text: str
    model: str
    provider: str
    raw: Any

class AtlasClient:
    """A client bound to one provider; automatic fallback is never performed."""
    def __init__(self, config: ProviderConfig, *, adapter: Any | None = None):
        self.config = config
        if adapter is not None:
            self._adapter = adapter
        elif config.provider in {"deepseek", "zai"}:
            self._adapter = OpenAICompatibleAdapter(config)
        else:
            raise ConfigurationError(f"No adapter registered for {config.provider!r}.")

    def chat(self, messages: list[dict[str, str]], *, temperature: float | None = None,
             max_tokens: int | None = None, reasoning: str | None = None) -> ChatResponse:
        result = self._adapter.chat(messages, temperature=temperature, max_tokens=max_tokens, reasoning=reasoning)
        try:
            text = result.choices[0].message.content or ""
        except (AttributeError, IndexError, TypeError) as exc:
            raise ValueError("Provider returned an unexpected chat-completions response.") from exc
        return ChatResponse(text=text, model=self.config.model, provider=self.config.provider, raw=result)
