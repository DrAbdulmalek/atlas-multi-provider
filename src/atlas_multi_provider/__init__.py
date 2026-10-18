"""Atlas Multi-Provider: explicit provider routing with no silent fallback."""

from .config import ProviderConfig, load_config
from .core import AtlasClient, ChatResponse
from .errors import AtlasError, ConfigurationError, ProviderRequestError, UnsupportedFeatureError

__all__ = [
    "AtlasClient",
    "AtlasError",
    "ChatResponse",
    "ConfigurationError",
    "ProviderConfig",
    "ProviderRequestError",
    "UnsupportedFeatureError",
    "load_config",
]
