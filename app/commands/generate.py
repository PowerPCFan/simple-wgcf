import modules.color as color
from pathlib import Path
from modules.global_vars import WGCF_HOME_DIR
from modules.utils import load_config, get_source_device, create_wireguard_config_file


def generate_command(mtu: int, filename: str) -> None:
    # Validate MTU
    if mtu < 576 or mtu > 1440:
        print(color.yellow("Warning: MTU is outside of the range 576-1440. You may experience issues."))

    # Validate filename by only allowing a-z, A-Z, 0-9, underscores, and hyphens
    if not filename.replace('_', '').replace('-', '').isalnum():
        print(color.yellow("Warning: Filename contains invalid characters. Using default 'cloudflare-warp-profile'."))
        filename = "cloudflare-warp-profile"

    print(color.blue("Generating WireGuard profile..."))

    try:
        PROFILE_FILE: Path = WGCF_HOME_DIR / (filename + ".conf")

        config = load_config()

        device_config = get_source_device(config["device_id"], config["access_token"])

        interface_config = device_config["config"]["interface"]
        peer_config = device_config["config"]["peers"][0]

        profile_content = create_wireguard_config_file(
            private_key=config["private_key"],
            ipv4_addresses=interface_config["addresses"]["v4"],
            ipv6_addresses=interface_config["addresses"]["v6"],
            mtu=str(mtu),
            public_key=peer_config["public_key"],
            endpoint=peer_config["endpoint"]["host"]
        )

        with open(PROFILE_FILE, 'w') as f:
            profile_content.write(f)

        print(color.green(f"WireGuard profile saved to {PROFILE_FILE.resolve()}"))
        print("You can now use this profile with any WireGuard client.")

    except Exception as e:
        print(color.red(f"Profile generation failed: {e}"))
