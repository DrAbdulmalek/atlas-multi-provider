# Security Policy

## Reporting a vulnerability

Do not post API keys, tokens, private medical data, or exploitable details in public issues. For sensitive reports, use GitHub's private vulnerability reporting feature if enabled for this repository.

## Credential handling

- Keep credentials in environment variables or a local ignored .env file.
- Never commit keys, tokens, or real request/response dumps containing sensitive data.
- If a credential is exposed, revoke it at the provider and rotate it; deleting the commit alone is not sufficient.

## Provider behavior

- The selected provider is never changed automatically after an error.
- Tests must use fake transports and must not require a real key or network access.
- Live provider smoke tests must be explicit, opt-in, and separate from normal CI.
