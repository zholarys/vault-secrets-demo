# Vault Secrets Demo

Local learning lab: Vault KV v2 stores a secret, a Python client retrieves it using a scoped token, and a policy limits reads to one path. Requires Docker Compose and Python 3 with venv support.

## Start and prepare Python

```bash
docker compose up -d
python3 -m venv .venv
. .venv/bin/activate
pip install -r app/requirements.txt
export VAULT_ADDR=http://127.0.0.1:8200
```

Vault uses dev mode with the public, disposable `dev-root-token` bootstrap token. Data lives in memory and is lost when Vault restarts. The host port is bound only to loopback. Never put real credentials into this demo.

## Store a dummy secret and install the policy

```bash
docker compose exec -T -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-root-token vault vault kv put secret/telegram-bot token=demo-placeholder
docker compose exec -T -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-root-token vault vault policy write app-read - < read-only-policy.hcl
export VAULT_TOKEN="$(docker compose exec -T -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-root-token vault vault token create -policy=app-read -no-default-policy -ttl=15m -field=token)"
python app/read_secret.py
```

Expected: `Secret retrieved successfully; value is not logged.` The client has a request timeout and never prints the secret or HTTP response body.

## Verify restricted access

```bash
# Only print HTTP status codes, not secret values. Expect 200, then 403.
curl -s -o /dev/null -w '%{http_code}\n' -H "X-Vault-Token: $VAULT_TOKEN" "$VAULT_ADDR/v1/secret/data/telegram-bot"
curl -s -o /dev/null -w '%{http_code}\n' -H "X-Vault-Token: $VAULT_TOKEN" "$VAULT_ADDR/v1/secret/data/unrelated"
unset VAULT_TOKEN
docker compose down
```

A production setup additionally needs durable storage, TLS, an appropriate unseal mechanism, audit logs and workload authentication with token lifecycle management. Environment variables are used here to bootstrap client authentication; Vault does not remove that bootstrap problem.
