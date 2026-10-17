# Atlas Multi-Provider

A modular Python gateway for multiple AI providers, beginning with DeepSeek and GLM/Z.ai, with a testable shared core and explicit provider selection.

## Safety and development principles

- Provider selection is explicit; no silent fallback between providers.
- API credentials are read from environment variables and must never be committed.
- Unit tests use mocks and must not require network access or paid API calls.
- Provider-specific reasoning options are translated only where supported by that provider.
- Live API verification is reported separately from mock/unit test results.
- Changes are developed on feature branches; merges into `main` require explicit approval.

## Status

Initial repository setup. Implementation and verification status will be documented as work progresses.
