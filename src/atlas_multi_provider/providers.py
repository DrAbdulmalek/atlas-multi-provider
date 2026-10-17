"""Provider adapters for OpenAI-compatible chat-completions endpoints."""
from __future__ import annotations
from typing import Any, Protocol
from .config import ProviderConfig
from .errors import ProviderRequestError

class ChatTransport(Protocol):
    def create(self, **kwargs: Any) -> Any: ...

class OpenAICompatibleAdapter:
    """Thin adapter; creates an SDK transport only when a request is made."""
    def __init__(self, config: ProviderConfig, *, transport: ChatTransport | None = None):
        self.config = config
        self._transport = transport

    def _get_transport(self) -> ChatTransport:
        if self._transport is None:
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise ProviderRequestError("The openai package is required; install atlas-multi-provider.") from exc
            client = OpenAI(api_key=self.config.api_key, base_url=self.config.base_url, timeout=self.config.timeout_seconds)
            self._transport = client.chat.completions
        return self._transport

    def chat(self, messages: list[dict[str, str]], *, temperature: float | None = None,
             max_tokens: int | None = None, reasoning: str | None = None) -> Any:
        if not messages:
            raise ValueError("messages must contain at least one message.")
        payload: dict[str, Any] = {"model": self.config.model, "messages": messages}
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        # Do not assume advanced controls are portable across providers.
        if reasoning is not None:
            if self.config.provider == "deepseek":
                if reasoning not in {"low", "high", "max"}:
                    raise ValueError("DeepSeek reasoning must be one of: low, high, max.")
                payload["extra_body"] = {"thinking": {"type": "enabled"}, "reasoning_effort": reasoning}
            elif self.config.provider == "zai":
                raise ValueError("Generic reasoning control for Z.ai is not implemented; omit it rather than sending an unverified parameter.")
        try:
            return self._get_transport().create(**payload)
        except (ValueError, ProviderRequestError):
            raise
        except Exception as exc:
            raise ProviderRequestError(f"Request to selected provider {self.config.provider!r} failed.") from exc
