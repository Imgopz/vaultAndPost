import requests

class VaultClient:
    def __init__(self, vault_url, auth_token=None):
        self.vault_url = vault_url
        self.auth_token = auth_token
        self.session = requests.Session()

    def login(self, username, password):
        """Login to Vault using a username and password."""
        login_url = f"{self.vault_url}/v1/auth/userpass/login/{username}"
        data = {"password": password}
        response = self.session.post(login_url, json=data)
        if response.status_code != 200:
            raise Exception(f"Failed to login to Vault: {response.text}")
        self.auth_token = response.json()["auth"]["client_token"]

    def get_secret(self, secret_path):
        """Get a secret from Vault."""
        if not self.auth_token:
            raise Exception("No authentication token found. Please login first.")
        secret_url = f"{self.vault_url}/v1/{secret_path}"
        headers = {"X-Vault-Token": self.auth_token}
        response = self.session.get(secret_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get secret from Vault: {response.text}")
        return response.json()["data"]

# Example usage
vault_client = VaultClient("https://vault.example.com")
vault_client.login("user1", "secret_password")
secret = vault_client.get_secret("secret/data/example")
print(f"Retrieved secret: {secret}")
