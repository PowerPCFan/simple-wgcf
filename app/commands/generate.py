import modules.color as color
from modules.global_vars import PROFILE_FILE
from modules.utils import load_config, get_source_device, create_wireguard_config_file


def generate_command() -> None:
    print(color.blue("Generating WireGuard profile..."))

    try:
        config = load_config()

        device_config = get_source_device(config["device_id"], config["access_token"])

        interface_config = device_config["config"]["interface"]
        peer_config = device_config["config"]["peers"][0]

        profile_content = create_wireguard_config_file(
            private_key=config["private_key"],
            ipv4_addresses=interface_config["addresses"]["v4"],
            ipv6_addresses=interface_config["addresses"]["v6"],
            public_key=peer_config["public_key"],
            endpoint=peer_config["endpoint"]["host"]
        )

        with open(PROFILE_FILE, 'w') as f:
            profile_content.write(f)

        print(color.green(f"WireGuard profile saved to {PROFILE_FILE.resolve()}"))
        print("You can now use this profile with any WireGuard client.")

    except Exception as e:
        print(color.red(f"Profile generation failed: {e}"))
