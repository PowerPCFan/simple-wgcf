import os
import modules.color as color
from modules.global_vars import CONFIG_FILE
from modules.wireguard import WireguardKey
from modules.utils import check_tos, save_config, register_device, create_yes_or_no_prompt


def register_command() -> None:
    print(color.blue("Registering new Cloudflare WARP account...") + "\n")

    if os.path.exists(CONFIG_FILE):
        overwrite = create_yes_or_no_prompt(
            f"Config file {CONFIG_FILE.resolve()} already exists. Overwrite?",
            default_yes=True
        )

        if not overwrite:
            print(color.yellow("Registration cancelled."))
            return

    if not check_tos():
        return

    private_key = WireguardKey.generate()

    print(color.blue("Generating keys and registering Cloudflare WARP account..."))

    try:
        # Register device
        device_response = register_device(private_key.public_key_base64())

        # Save configuration
        config = {
            "private_key": private_key.to_base64(),
            "device_id": device_response["id"],
            "access_token": device_response["token"],
            "license_key": device_response["account"]["license"]
        }

        save_config(config)

        print(color.green("Successfully registered Cloudflare WARP account!"))

    except Exception as e:
        print(color.red(f"Registration failed: {e}"))
