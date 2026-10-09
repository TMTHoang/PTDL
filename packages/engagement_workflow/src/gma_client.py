"""
gma_client.py - Reusable MCP client with auto-refresh.

Usage:
    from gma_client import call_mcp, refresh_if_needed

    refresh_if_needed()
    sites = call_mcp("list_sites")
    overview = call_mcp("get_overview", {"site_id": "1games.io", "from": "2026-09-06", "to": "2026-10-04"})

Reference: D:/GR/engagement_workflow/docs/MCP_DATA_COLLECTION_v2.md
"""
import requests
import json
import time
from pathlib import Path

BASE = "https://gma-web.readyplayer1.xyz"
TOKEN_FILE = Path(r"D:\GR\.gma_token.json")
REFRESH_BEFORE_SEC = 60  # Refresh if token expires within 60s


def _load_token() -> dict:
    return json.loads(TOKEN_FILE.read_text())


def _save_token(d: dict):
    TOKEN_FILE.write_text(json.dumps(d, indent=2))


def _refresh(token_data: dict) -> dict:
    """Exchange refresh_token for a new access_token."""
    r = requests.post(f"{BASE}/oauth/token", json={
        "grant_type": "refresh_token",
        "client_id": token_data["client_id"],
        "refresh_token": token_data["refresh_token"],
    }, timeout=10)
    r.raise_for_status()
    new = r.json()
    token_data.update({
        "access_token": new["access_token"],
        "refresh_token": new.get("refresh_token", token_data["refresh_token"]),
        "expires_in": new["expires_in"],
        "saved_at": time.time(),
    })
    _save_token(token_data)
    return token_data


def refresh_if_needed() -> dict:
    """Refresh token if it's about to expire. Returns current token data."""
    d = _load_token()
    expires_at = d["saved_at"] + d.get("expires_in", 900)
    if time.time() > expires_at - REFRESH_BEFORE_SEC:
        return _refresh(d)
    return d


def call_mcp(tool_name: str, arguments: dict = None, auto_retry_on_401: bool = True) -> dict:
    """
    Call an MCP tool. Returns parsed JSON.

    Handles:
    - Auto-refresh if token is expiring
    - SSE response parsing (data: lines)
    - One retry on 401 with forced refresh
    """
    token_data = refresh_if_needed()
    access_token = token_data["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments or {}}
    }

    r = requests.post(f"{BASE}/mcp", headers=headers, json=payload, timeout=60)

    # Retry once on 401 with forced refresh
    if r.status_code == 401 and auto_retry_on_401:
        token_data = _refresh(_load_token())
        headers["Authorization"] = f"Bearer {token_data['access_token']}"
        r = requests.post(f"{BASE}/mcp", headers=headers, json=payload, timeout=60)

    r.raise_for_status()

    # Parse SSE
    text = r.text
    data_str = None
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('data: '):
            data_str = line[6:]
            break
    if not data_str:
        return {"_raw_sse": text}

    parsed = json.loads(data_str)

    # Unwrap MCP content[0].text
    if "result" in parsed and "content" in parsed["result"]:
        content = parsed["result"]["content"]
        if content and content[0].get("type") == "text":
            try:
                return json.loads(content[0]["text"])
            except json.JSONDecodeError:
                return {"_text": content[0]["text"]}

    if "error" in parsed:
        return {"_mcp_error": parsed["error"]}

    return parsed
