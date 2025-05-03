import requests
import json
import os
from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq import ApiEnvironmentType


def create_sandbox_user():
    """Creates a new sandbox user and returns token, email, IBAN."""
    url = "https://public-api.sandbox.bunq.com/v1/sandbox-user-person"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "bunq-sdk-python"
    }

    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to create user: {response.text}")

    data = response.json()
    token = data["Response"][1]["Token"]["token"]
    user = data["Response"][2]["UserPerson"]
    aliases = user["alias"]

    email = next((a["value"] for a in aliases if a["type"] == "EMAIL"), None)
    iban = next((a["value"] for a in aliases if a["type"] == "IBAN"), None)

    return token, email, iban


def save_user_context(api_key: str, fake_name: str):
    """Creates and saves the .conf file with fake name."""
    ctx = ApiContext.create(
        ApiEnvironmentType.SANDBOX,
        api_key,
        f"{fake_name}'s Device"
    )

    conf_name = f"bunq_{fake_name.lower().replace(' ', '_')}.conf"
    ctx.save(conf_name)
    return conf_name


def create_fake_users(n=3):
    users = []

    for _ in range(n):
        nume=""
        for ii in range(n):
            nume+="a"
        name = nume
        print(f"👤 Creating user: {name}")
        api_key, email, iban = create_sandbox_user()
        conf_file = save_user_context(api_key, name)

        users.append({
            "name": name,
            "email": email,
            "iban": iban,
            "api_key": api_key,
            "conf_file": conf_file
        })

    return users


# Run the generator
if __name__ == "__main__":
    users = create_fake_users(3)

    print("\n🎉 Generated users:")
    for u in users:
        print(json.dumps(u, indent=2))