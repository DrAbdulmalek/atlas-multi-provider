"""Domain exceptions exposed by the Atlas API."""

class AtlasError(Exception):
    """Base class for expected Atlas failures."""

class ConfigurationError(AtlasError):
    """Raised when provider configuration is missing or invalid."""

class ProviderRequestError(AtlasError):
    """Raised when the selected provider request fails."""

class UnsupportedFeatureError(AtlasError):
    """Raised when a requested feature is not supported by a provider."""
