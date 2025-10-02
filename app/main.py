import argparse
import sys
import modules.color as color
import modules.global_vars as gv
from typing import Callable

from commands.generate import generate_command
from commands.register import register_command


def run_cmd(
    command: Callable[gv.P, gv.R],
    *args: gv.P.args,
    **kwargs: gv.P.kwargs
) -> gv.R:
    print()
    res = command(*args, **kwargs)
    print()

    return res


def main():
    parser = argparse.ArgumentParser(
        description="Simple-WGCF: A Wireguard profile generator for Cloudflare WARP",
        add_help=True
    )

    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate a WireGuard profile from existing account"
    )
    generate_parser.add_argument(
        "--mtu",
        type=int,
        default=1280,
        help="Set the MTU value for the generated profile (default: 1280)"
    )
    generate_parser.add_argument(
        "--filename",
        type=str,
        default="cloudflare-warp-profile",
        help="Set the filename for the generated profile (default: cloudflare-warp-profile)"
    )

    register_parser = subparsers.add_parser(
        "register",
        help="Register a new Cloudflare WARP account"
    )

    args = parser.parse_args()

    if args.command == "generate":
        run_cmd(generate_command, mtu=args.mtu, filename=args.filename)
    elif args.command == "register":
        run_cmd(register_command)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\n" + color.yellow("Ctrl+C pressed, exiting..."))
        sys.exit(0)
    except Exception as e:
        print(f"An unhandled exception occurred: {e}")
        sys.exit(1)
