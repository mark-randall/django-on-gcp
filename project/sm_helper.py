import google.auth
from google.cloud import secretmanager_v1beta1 as sm

"""
For a list of secret values, return a dictionary of keys and values from Secret
Manager (if such a service exists in the current context)
"""
def access_secrets(secret_keys):
    secrets = {}
    _, project = google.auth.default()

    if project:
        client = sm.SecretManagerServiceClient()

        for s in secret_keys:
            path = client.secret_version_path(project, s, "latest")
            payload = client.access_secret_version(path).payload.data.decode("UTF-8")
            secrets[s] = payload

    return secrets
