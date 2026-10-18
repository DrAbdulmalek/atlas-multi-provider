import pytest
from atlas_multi_provider.config import ProviderConfig, load_config
from atlas_multi_provider.errors import ConfigurationError


def test_loads_deepseek_from_environment():
    cfg = load_config({"ATLAS_PROVIDER": "deepseek", "DEEPSEEK_API_KEY": "test-key", "DEEPSEEK_BASE_URL": "https://example.invalid/v1", "DEEPSEEK_MODEL": "test-model"})
    assert cfg.provider == "deepseek"
    assert cfg.model == "test-model"


def test_explicit_provider_overrides_environment_selection():
    cfg = load_config(
        {
            "ATLAS_PROVIDER": "deepseek",
            "DEEPSEEK_API_KEY": "deepseek-test-key",
            "DEEPSEEK_BASE_URL": "https://example.invalid/v1",
            "DEEPSEEK_MODEL": "deepseek-test-model",
            "ZAI_API_KEY": "zai-test-key",
            "ZAI_BASE_URL": "https://example.invalid/api/paas/v4",
            "ZAI_MODEL": "zai-test-model",
        },
        provider="zai",
    )
    assert cfg.provider == "zai"
    assert cfg.model == "zai-test-model"


def test_explicit_empty_provider_is_rejected_instead_of_falling_back():
    with pytest.raises(ConfigurationError, match="Unsupported provider"):
        load_config({"ATLAS_PROVIDER": "deepseek"}, provider="")


def test_unknown_provider_is_rejected():
    with pytest.raises(ConfigurationError, match="Unsupported provider"):
        load_config({"ATLAS_PROVIDER": "unknown"})


def test_missing_key_fails_closed():
    with pytest.raises(ConfigurationError, match="API key is missing"):
        load_config({"ATLAS_PROVIDER": "zai", "ZAI_BASE_URL": "https://example.invalid/v1", "ZAI_MODEL": "test-model"})


def test_non_numeric_timeout_is_rejected():
    with pytest.raises(ConfigurationError, match="must be a number"):
        load_config({"ATLAS_TIMEOUT_SECONDS": "not-a-number", "DEEPSEEK_API_KEY": "key", "DEEPSEEK_BASE_URL": "https://example.invalid/v1", "DEEPSEEK_MODEL": "model"})


def test_nonpositive_timeout_is_rejected():
    with pytest.raises(ConfigurationError, match="timeout_seconds"):
        ProviderConfig("deepseek", "key", "https://example.invalid", "model", 0)
