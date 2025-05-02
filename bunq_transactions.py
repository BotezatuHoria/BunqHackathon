import os
import time
import json
import base64
import requests
from pprint import pprint
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

API_KEY = "sandbox_d199e92eb4646fce5b3ced92b2d8fc0c062fa389084c988a0bd7fdb0"
BASE_URL = "https://public-api.sandbox.bunq.com/v1"
PRIVATE_KEY_FILE = "private_key.pem"
PUBLIC_KEY_FILE = "public_key.pem"
INSTALLATION_FILE = "installation.json"
SESSION_FILE = "session.json"

def generate_key_pair():
    if os.path.exists(PRIVATE_KEY_FILE) and os.path.exists(PUBLIC_KEY_FILE):
        return
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with open(PRIVATE_KEY_FILE, "wb") as f:
        f.write(private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    with open(PUBLIC_KEY_FILE, "wb") as f:
        f.write(private_key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def sign_request(private_key_file, data: str) -> str:
    with open(private_key_file, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)
    signature = private_key.sign(
        data.encode("utf-8"),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode("utf-8")

def install():
    with open(PUBLIC_KEY_FILE, "r") as f:
        pubkey = f.read()
    payload = json.dumps({ "client_public_key": pubkey })
    signature = sign_request(PRIVATE_KEY_FILE, payload)
    headers = {
        "Content-Type": "application/json",
        "X-Bunq-Language": "en_US",
        "X-Bunq-Region": "nl_NL",
        "X-Bunq-Geolocation": "0 0 0 0 000",
        "X-Bunq-Client-Request-Id": "req-installation",
        "X-Bunq-Client-Signature": signature
    }
    url = f"{BASE_URL}/installation"
    response = requests.post(url, headers=headers, data=payload)
    res_json = response.json()
    pprint(res_json)
    if "Error" in res_json:
        raise Exception("❌ INSTALLATION failed: " + res_json["Error"][0]["error_description"])
    token = res_json["Response"][1]["Token"]["token"]
    with open(INSTALLATION_FILE, "w") as f:
        json.dump({ "token": token }, f)
    print("✅ Installation token saved")
    return token

def load_installation_token():
    if os.path.exists(INSTALLATION_FILE):
        with open(INSTALLATION_FILE, "r") as f:
            return json.load(f)["token"]
    return None

def register_device(installation_token):
    payload = {
        "description": "My Python Client",
        "secret": API_KEY
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "python-client",
        "X-Bunq-Language": "en_US",
        "X-Bunq-Region": "nl_NL",
        "X-Bunq-Geolocation": "0 0 0 0 000",
        "X-Bunq-Client-Request-Id": "req-device",
        "X-Bunq-Client-Authentication": installation_token
    }

    url = f"{BASE_URL}/device-server"
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    res_json = response.json()
    pprint(res_json)

    if "Error" in res_json:
        raise Exception("❌ DEVICE registration failed: " + res_json["Error"][0]["error_description"])

    print("✅ Device registered")

def create_session(installation_token):
    body = json.dumps({ "secret": API_KEY })
    signature = sign_request(PRIVATE_KEY_FILE, body)
    headers = {
        "Content-Type": "application/json",
        "X-Bunq-Language": "en_US",
        "X-Bunq-Region": "nl_NL",
        "X-Bunq-Geolocation": "0 0 0 0 000",
        "X-Bunq-Client-Authentication": installation_token,
        "X-Bunq-Client-Signature": signature
    }
    url = f"{BASE_URL}/session-server"
    response = requests.post(url, headers=headers, data=body)
    res_json = response.json()
    pprint(res_json)
    if "Error" in res_json:
        raise Exception("❌ SESSION creation failed: " + res_json["Error"][0]["error_description"])
    token = res_json["Response"][1]["Token"]["token"]
    user_id = res_json["Response"][2]["UserPerson"]["id"]
    with open(SESSION_FILE, "w") as f:
        json.dump({ "token": token, "user_id": user_id }, f)
    print("✅ Session created and saved")
    return token, user_id

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            session = json.load(f)
            return session["token"], session["user_id"]
    return None, None

def main():
    print("🔍 Checking for existing session...")
    token, user_id = load_session()

    if token and user_id:
        print("✅ Reusing saved session token and user ID")
    else:
        print("🔧 Generating keys...")
        generate_key_pair()

        installation_token = load_installation_token()
        if not installation_token:
            print("📦 Installing client...")
            installation_token = install()
            time.sleep(1)

        print("📱 Registering device...")
        register_device(installation_token)
        time.sleep(1)

        print("🔐 Creating session...")
        token, user_id = create_session(installation_token)

    print("🎉 Ready to make API calls!")
    print("🔐 Session token:", token)
    print("👤 User ID:", user_id)

if __name__ == "__main__":
    main()