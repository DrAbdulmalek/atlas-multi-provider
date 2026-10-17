import pytest
from atlas_multi_provider.config import ProviderConfig, load_config
from atlas_multi_provider.errors import ConfigurationError

def test_loads_deepseek_from_environment():
    cfg = load_config({"ATLAS_PROVIDER":"deepseek","DEEPSEEK_API_KEY":"test-key","DEEPSEEK_BASE_URL":"https://example.invalid/v1","DEEPSEEK_MODEL":"test-model"})
    assert cfg.provider == "deepseek"
    assert cfg.model == "test-model"

def test_unknown_provider_is_rejected():
    with pytest.raises(ConfigurationError, match="Unsupported provider"):
        load_config({"ATLAS_PROVIDER":"unknown"})

def test_missing_key_fails_closed():
    with pytest.raises(ConfigurationError, match="API key is missing"):
        load_config({"ATLAS_PROVIDER":"zai","ZAI_BASE_URL":"https://example.invalid/v1","ZAI_MODEL":"test-model"})

def test_nonpositive_timeout_is_rejected():
    with pytest.raises(ConfigurationError, match="timeout_seconds"):
        ProviderConfig("deepseek","key","https://example.invalid","model",0)
