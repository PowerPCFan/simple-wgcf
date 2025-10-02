import json
import os
import sys
import requests
import configparser
import modules.color as color
from datetime import datetime
from modules.global_vars import CONFIG_FILE, API_URL, API_VERSION, DEFAULT_HEADERS


def create_yes_or_no_prompt(
    prompt: str,
    default_yes: bool | None = None
) -> bool:
    """
    Returns True for yes, False for no.
    Set default_yes to True for default = yes, or set to False for default = no.
    """

    # colorblue = lambda text: color.blue(text)  # noqa: E731
    colorblue = lambda text: text  # noqa: E731

    yes = colorblue("Y") if default_yes else "y"
    no = colorblue("N") if default_yes is False else "n"
    prompt = f"{color.yellow(prompt)} [{yes}/{no}]: "

    while True:
        response = input(prompt).strip().lower()

        if response in ['yes', 'y']:
            print()
            return True
        elif response in ['no', 'n']:
            print()
            return False
        elif response == '' and default_yes:
            print()
            return default_yes
        print(f"Invalid response '{response}'. Please try again.")


def make_api_request(
    url: str,
    data: dict | None = None,
    headers: dict | None = None,
    auth_token: str | None = None
) -> dict:
    if headers is None:
        headers = DEFAULT_HEADERS.copy()

    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    try:
        if data:
            response = requests.post(url, json=data, headers=headers)
        else:
            response = requests.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            print(f"API Error: HTTP {e.response.status_code}")
        raise Exception(f"HTTP {e.response.status_code}: {e.response.reason}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")


def get_timestamp() -> str:
    return datetime.now().isoformat() + "Z"


def register_device(public_key: str) -> dict:
    url = f"{API_URL}/{API_VERSION}/reg"

    data = {
        "fcm_token": "",
        "install_id": "",
        "key": public_key,
        "locale": "en_US",
        "model": "PC",
        "tos": get_timestamp(),
        "type": "Android"  # not sure why this is android but whatever
    }

    return make_api_request(url, data)


def get_source_device(device_id: str, access_token: str) -> dict:
    url = f"{API_URL}/{API_VERSION}/reg/{device_id}"
    return make_api_request(url, auth_token=access_token)


def save_config(config: dict) -> None:
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Configuration saved to {CONFIG_FILE.resolve()}")


def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        raise Exception(f"Configuration file {CONFIG_FILE.resolve()} not found. Run 'register' first.")

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def check_tos() -> bool:
    print("DISCLAIMER: This project is not affiliated with Cloudflare.")
    print("Please read Cloudflare's ToS before proceeding: https://www.cloudflare.com/application/terms/")

    if create_yes_or_no_prompt("Do you agree to the Cloudflare Terms of Service?", default_yes=True):
        return True
    else:
        print("You must accept the Terms of Service to continue.")
        sys.exit(1)
        return False  # if it somehow gets here idk


class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr


def create_wireguard_config_file(
    private_key: str,
    ipv4_addresses: str,
    ipv6_addresses: str,
    public_key: str,
    endpoint: str
) -> CaseSensitiveConfigParser:
    interface = {
        "PrivateKey": private_key,
        "Address": f"{ipv4_addresses}/32, {ipv6_addresses}/128",
        "DNS": "1.1.1.1, 1.0.0.1, 2606:4700:4700::1111, 2606:4700:4700::1001",
        "MTU": "1280",
    }

    peer = {
        "PublicKey": public_key,
        "AllowedIPs": "0.0.0.0/0, ::/0",
        "Endpoint": endpoint,
    }

    config = CaseSensitiveConfigParser()
    config["Interface"] = interface
    config["Peer"] = peer

    return config
