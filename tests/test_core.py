from types import SimpleNamespace

import pytest

from atlas_multi_provider.config import ProviderConfig
from atlas_multi_provider.core import AtlasClient
from atlas_multi_provider.errors import ProviderRequestError
from atlas_multi_provider.providers import OpenAICompatibleAdapter


class FakeTransport:
    def __init__(self, result=None, error=None):
        self.kwargs = None
        self.result = result or SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="mock answer"))]
        )
        self.error = error

    def create(self, **kwargs):
        self.kwargs = kwargs
        if self.error:
            raise self.error
        return self.result


def config(provider="deepseek"):
    return ProviderConfig(provider, "not-a-real-key", "https://example.invalid/v1", "mock-model")


def test_chat_returns_normalized_response_without_network():
    cfg, transport = config(), FakeTransport()
    client = AtlasClient(cfg, adapter=OpenAICompatibleAdapter(cfg, transport=transport))
    response = client.chat([{"role": "user", "content": "hello"}])
    assert response.text == "mock answer"
    assert response.provider == "deepseek"
    assert transport.kwargs["model"] == "mock-model"


def test_deepseek_reasoning_options_follow_documented_request_shape():
    transport = FakeTransport()
    OpenAICompatibleAdapter(config(), transport=transport).chat(
        [{"role": "user", "content": "x"}], reasoning="high"
    )
    assert transport.kwargs["reasoning_effort"] == "high"
    assert transport.kwargs["extra_body"] == {"thinking": {"type": "enabled"}}
    assert "reasoning_effort" not in transport.kwargs["extra_body"]


def test_invalid_reasoning_is_rejected_before_request():
    transport = FakeTransport()
    with pytest.raises(ValueError, match="reasoning must be"):
        OpenAICompatibleAdapter(config(), transport=transport).chat(
            [{"role": "user", "content": "x"}], reasoning="medium"
        )
    assert transport.kwargs is None


def test_zai_reasoning_is_not_silently_forwarded():
    transport = FakeTransport()
    with pytest.raises(ValueError, match="not implemented"):
        OpenAICompatibleAdapter(config("zai"), transport=transport).chat(
            [{"role": "user", "content": "x"}], reasoning="high"
        )
    assert transport.kwargs is None


def test_provider_failure_does_not_fallback():
    transport = FakeTransport(error=RuntimeError("simulated failure"))
    with pytest.raises(ProviderRequestError, match="selected provider"):
        OpenAICompatibleAdapter(config(), transport=transport).chat(
            [{"role": "user", "content": "x"}]
        )
