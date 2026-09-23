import os
import requests

VAULT_ADDR = os.environ.get("VAULT_ADDR", "http://vault:8200")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN")

if not VAULT_TOKEN:
    raise SystemExit("VAULT_TOKEN environment variable is required")

url = f"{VAULT_ADDR}/v1/secret/data/telegram-bot"
headers = {"X-Vault-Token": VAULT_TOKEN}

response = requests.get(url, headers=headers)
if not response.ok:
    print("ERROR BODY:", response.text)
response.raise_for_status()

token = response.json()["data"]["data"]["token"]
print(f"Retrieved secret from Vault (not logging full value): {token[:6]}...")
