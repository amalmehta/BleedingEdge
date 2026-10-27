"""GET with a disk cache, polite per-host delays and retries.

Every response is cached under data/cache/ keyed by URL, so a re-run makes no
network calls and gives the same numbers. Delete the folder to refetch.
"""
import hashlib
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"

# Seconds between calls to each host: arXiv asks for 3 s; GitHub search allows 30 a minute.
DELAYS = {"export.arxiv.org": 3.5, "api.github.com": 2.2, "hn.algolia.com": 0.3}
_last_call: dict[str, float] = {}
_github_token: str | None = None


def _load_env() -> dict[str, str]:
    env = {}
    path = ROOT / ".env"
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def secret(name: str) -> str | None:
    """A key from the environment or .env, or None."""
    return os.environ.get(name) or _load_env().get(name) or None


def _headers(host: str) -> dict[str, str]:
    global _github_token
    h = {"User-Agent": "BleedingEdge-backtest (personal research)"}
    if host == "api.github.com":
        if _github_token is None:
            _github_token = subprocess.run(
                ["gh", "auth", "token"], capture_output=True, text=True, check=True
            ).stdout.strip()
        h["Authorization"] = f"Bearer {_github_token}"
        h["Accept"] = "application/vnd.github+json"
    return h


def _cache_path(url: str) -> Path:
    host = urlparse(url).netloc
    return CACHE / host / (hashlib.sha1(url.encode()).hexdigest() + ".txt")


def get_text(url: str, retries: int = 6) -> str:
    path = _cache_path(url)
    if path.exists():
        return path.read_text()
    host = urlparse(url).netloc
    for attempt in range(retries):
        wait = DELAYS.get(host, 1.0) - (time.time() - _last_call.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        _last_call[host] = time.time()
        try:
            req = urllib.request.Request(url, headers=_headers(host))
            with urllib.request.urlopen(req, timeout=90) as resp:
                body = resp.read().decode("utf-8")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body)
            return body
        except urllib.error.HTTPError as e:
            if e.code not in (403, 429, 500, 502, 503, 504) or attempt == retries - 1:
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == retries - 1:
                raise
        time.sleep(min(120, 5 * 2**attempt))
    raise RuntimeError(f"unreachable: {url}")


def get_json(url: str) -> dict:
    return json.loads(get_text(url))
