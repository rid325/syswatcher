"""
Network geo-lookup using ip-api.com (free, no API key required).
Results are cached in memory to avoid hammering the API on every refresh.
Private/loopback IPs are skipped automatically.
"""

import ipaddress
import requests

_cache: dict[str, str] = {}  # ip -> "City, Country"
_TIMEOUT = 2  # seconds per request


def _is_private(ip: str) -> bool:
    """Returns True if the IP is private, loopback, or link-local."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return True


def lookup_ip(ip: str) -> str:
    """
    Returns a 'City, Country' string for a public IP.
    Returns 'Private' for local IPs and 'Unknown' on failure.
    """
    if _is_private(ip):
        return "Private"

    if ip in _cache:
        return _cache[ip]

    try:
        resp = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,country,city",
            timeout=_TIMEOUT
        )
        data = resp.json()
        if data.get("status") == "success":
            location = f"{data.get('city', '?')}, {data.get('country', '?')}"
        else:
            location = "Unknown"
    except Exception:
        location = "Unknown"

    _cache[ip] = location
    return location


def enrich_connections(connections: list[dict]) -> list[dict]:
    """
    Adds a 'location' key to each connection dict by looking up the remote IP.
    Skips connections that have an error flag.
    """
    for conn in connections:
        if "_error" in conn:
            continue
        remote_ip = conn["remote"].split(":")[0]
        conn["location"] = lookup_ip(remote_ip)
    return connections
