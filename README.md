# simple-wgcf

Simple-WGCF: A Wireguard profile generator for Cloudflare WARP

### Commands:
- `(no command)` - Show help message
  - Options:
    - `--help`, `-h`   Also shows help message
- `generate` - Generate WireGuard configuration file from Cloudflare WARP account
  - Options:
    - `-h`, `--help`          Show help message for generate command
    - `--mtu MTU`             Set the MTU value for the generated profile (default: 1280)
    - `--filename FILENAME`   Set the filename for the generated profile (default: cloudflare-warp-profile)
- `register` - Register a new Cloudflare WARP account
  - Options:
    - `-h`, `--help`          Show help message for register command
- `test-speed` - Test the speed of your current network connection (Useful for testing speed when connected to WARP)
  - Options:
    - `-h`, `--help`          Show help message for test-speed command
