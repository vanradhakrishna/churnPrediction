import requests
import yaml
import sys
import os

DATABRICKS_HOST = os.environ["DATABRICKS_HOST"]
TOKEN = os.environ["DATABRICKS_TOKEN"]

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

env = sys.argv[1]

with open("infra/config.yaml", "r") as f:
    config = yaml.safe_load(f)

env_config = config[env]

endpoint_name = env_config["endpoint_name"]
model_name = env_config["model_name"]
alias = env_config["alias"]

url = f"{DATABRICKS_HOST}/api/2.0/serving-endpoints/{endpoint_name}"

payload = {
    "name": endpoint_name,
    "config": {
        "served_models": [
            {
                "model_name": model_name,
                "model_version": alias,
                "workload_size": "Small",
                "scale_to_zero_enabled": True
            }
        ]
    }
}

response = requests.post(
    f"{DATABRICKS_HOST}/api/2.0/serving-endpoints",
    headers=headers,
    json=payload
)

if response.status_code in [400, 409]:
    print("Updating existing endpoint...")
    response = requests.put(
        f"{url}/config",
        headers=headers,
        json=payload["config"]
    )

print(response.status_code)
print(response.text)