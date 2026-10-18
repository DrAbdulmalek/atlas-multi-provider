# Atlas Multi-Provider

A modular Python client for explicitly selecting an AI provider. Initial adapters target DeepSeek and Z.ai/GLM through an OpenAI-compatible chat-completions interface.

## Principles

- **No silent fallback:** requests use only the configured provider; failures are surfaced as provider errors.
- **Secrets stay out of Git:** credentials come from environment variables. Never commit real API keys or local .env files.
- **Offline-first tests:** tests inject fake transports and must not make network calls or consume API credits.
- **Provider-specific controls:** reasoning parameters are not assumed portable between providers.
- **Honest verification:** mock tests do not prove live API compatibility.

## Quick start

Requires Python 3.10+.

~~~bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
cp .env.example .env
~~~

Set your own credentials and a model ID in your local environment before making a live request. The Z.ai model is intentionally blank in .env.example so you can select a model available to your account. Do not commit .env.

## Example

~~~python
from atlas_multi_provider import AtlasClient, load_config

config = load_config()  # ATLAS_PROVIDER selects exactly one provider
client = AtlasClient(config)
response = client.chat([{"role": "user", "content": "Explain a simple concept."}])
print(response.text)
~~~

The example makes a live API request and may incur charges. Unit tests do not.

## Reasoning controls

- **DeepSeek:** when explicitly requested, the adapter sends `reasoning_effort` as a top-level Chat Completions parameter and `thinking.type=enabled` through the OpenAI SDK's `extra_body`, following the official API guide. Supported values in this wrapper are `low`, `high`, and `max`.
- **Z.ai/GLM:** generic reasoning control is rejected until model-specific behavior is implemented and verified. GLM reasoning controls vary by model family and version; ordinary chat calls omit reasoning-specific fields.

Reasoning is optional. This wrapper does not expose or log private reasoning content; callers should use the model's user-facing response content and follow provider policies.

## Tests

~~~bash
python -m pytest
~~~

The tests use fake transports and are designed to run without network access or API credentials. A passing local run is required before describing the implementation as tested.

## Current scope and limitations

- Synchronous chat-completions interface only.
- No automatic retry, provider fallback, streaming, tool calls, or model-name guessing.
- No live API verification is claimed by the unit tests.
- Provider API/model features can change; check official documentation before enabling advanced controls.
