# Vault Secrets Demo

A HashiCorp Vault lab demonstrating centralized secrets management, replacing hardcoded credentials and .env files with a proper secrets store and scoped access.

## Architecture

- Vault running in dev mode (in-memory, auto-unsealed — production would use a persistent storage backend and manual unseal)
- KV v2 secrets engine storing application secrets
- A Python client reading secrets via the Vault HTTP API instead of environment variables or hardcoded values
- A least-privilege policy restricting access to a single secret path

## What it shows

- Storing and retrieving secrets via `vault kv put` / `vault kv get`
- Reading secrets programmatically through the Vault API
- Writing a scoped Vault policy (`read-only-policy.hcl`) instead of using the root token everywhere
- Verifying the policy actually restricts access — a scoped token can read the intended secret but is denied on unrelated operations (`403 permission denied`)

## Motivation

Built after a real incident where a Telegram bot token was accidentally committed to a public GitHub repository and flagged by GitHub's secret scanning. This lab demonstrates the alternative: secrets pulled from a dedicated store at runtime, never stored in code or version control.

## Stack

Docker Compose, HashiCorp Vault, Python

## Usage

\`\`\`bash
docker compose up -d
\`\`\`

Store a secret:
\`\`\`bash
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-root-token <container> vault kv put secret/telegram-bot token="..."
\`\`\`

Read it via the app:
\`\`\`bash
VAULT_TOKEN="<scoped-token>" VAULT_ADDR="http://127.0.0.1:8200" python3 app/read_secret.py
\`\`\`
