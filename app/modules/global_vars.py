from pathlib import Path
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

WGCF_HOME_DIR: Path = Path.home() / ".simple-wgcf"
WGCF_HOME_DIR.mkdir(exist_ok=True)

CONFIG_FILE: Path = WGCF_HOME_DIR / ".wgcf-account.json"
PROFILE_FILE: Path = WGCF_HOME_DIR / "cloudflare-warp-profile.conf"

API_URL = "https://api.cloudflareclient.com"
# this shouldn't ever need to change, looking in ViRb3/wgcf's commit history it's been "v0a1922" for a long time
API_VERSION = "v0a1922"

DEFAULT_HEADERS = {
    "User-Agent": "okhttp/3.12.1",
    "CF-Client-Version": "a-6.3-1922",
    "Content-Type": "application/json"
}
