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

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--generate",
        action="store_true",
        help="Generate a WireGuard profile from existing account"
    )
    group.add_argument(
        "--register",
        action="store_true",
        help="Register a new Cloudflare WARP account"
    )

    args = parser.parse_args()

    # Handle commands
    if args.generate:
        run_cmd(generate_command)
    elif args.register:
        run_cmd(register_command)
    else:
        print("No command specified. Use --help / -h for usage information.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\n" + color.yellow("Ctrl+C pressed, exiting..."))
        sys.exit(0)
    except Exception as e:
        print(f"An unhandled exception occurred: {e}")
        sys.exit(1)
