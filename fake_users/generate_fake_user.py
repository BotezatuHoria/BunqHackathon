from bunq.sdk.context.api_context import ApiContext
from bunq import ApiEnvironmentType

import requests
import json

def create_sandbox_user():
    url = "https://public-api.sandbox.bunq.com/v1/sandbox-user-person"
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "User-Agent": "bunq-sdk-python"
    }

    response = requests.post(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"❌ Failed to create sandbox user: {response.text}")

    res = response.json()
    token = res['Response'][1]['Token']['token']
    user_info = res['Response'][2]['UserPerson']
    aliases = user_info['alias']
    iban = next((a['value'] for a in aliases if a['type'] == 'IBAN'), None)
    email = next((a['value'] for a in aliases if a['type'] == 'EMAIL'), None)

    return {
        "api_key": token,
        "iban": iban,
        "email": email
    }

# Example usage
user = create_sandbox_user()
print("🎉 New sandbox user created:")
print(json.dumps(user, indent=2))

def generate_fake_user(name:str):
    api_context = ApiContext.create(
        ApiEnvironmentType.SANDBOX,
        "sandbox_d199e92eb4646fce5b3ced92b2d8fc0c062fa389084c988a0bd7fdb0",
        name+" device"
    )
    api_context.save(name+"_bunq.conf")
    print(name+" generated")

#generate_fake_user("Gigel Ionut")