"""
gma_oauth.py — One-time OAuth 2.0 + PKCE auth for GMA Web.

Run ONCE to get a token saved next to this script (or next to the .exe
when frozen via PyInstaller). After that, gma_client.py auto-refreshes it.

Reference: D:/GR/engagement_workflow/docs/MCP_DATA_COLLECTION_v2.md
"""
import base64, hashlib, json, secrets, sys, time, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import requests

BASE = "https://gma-web.readyplayer1.xyz"
REDIRECT_URI = "http://127.0.0.1:8765/callback"

# Module-level paths (overridden by workflow.py when called from the .exe)
TOKEN_FILE = Path(r".gma_token.json")
STATE_FILE = Path(r".gma_oauth_state.json")


# ── PKCE helpers ──────────────────────────────────────────────────────────────

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def pkce_pair():
    verifier = b64url(secrets.token_bytes(48))
    challenge = b64url(hashlib.sha256(verifier.encode()).digest())
    return verifier, challenge


# ── Step 1: Register client ───────────────────────────────────────────────────

def register_client() -> str:
    r = requests.post(f"{BASE}/oauth/register", json={
        "client_name": "Engagement Workflow",
        "redirect_uris": [REDIRECT_URI],
        "grant_types": ["authorization_code", "refresh_token"],
        "token_endpoint_auth_method": "none",
    }, timeout=10)
    r.raise_for_status()
    return r.json()["client_id"]


# ── Step 2: Browser auth ─────────────────────────────────────────────────────

def start_callback_server():
    """Returns (server, handler_class) when the browser hits the callback."""
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args): pass  # silent

        def do_GET(self):
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(self.path)
            qs = parse_qs(parsed.query)
            if "code" in qs and "state" in qs:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>Authenticated! You can close this tab.</h1>")
                Handler._code = qs["code"][0]
                Handler._state = qs["state"][0]
                self.server.should_stop = True
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Bad callback")

    server = HTTPServer(("127.0.0.1", 8765), Handler)
    server.should_stop = False
    Handler._code = None
    Handler._state = None
    return server, Handler


def exchange_code(client_id: str, code: str, verifier: str) -> dict:
    r = requests.post(f"{BASE}/oauth/token", json={
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": verifier,
    }, timeout=10)
    r.raise_for_status()
    return r.json()


def test_token(access_token: str):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
               "params": {"name": "list_sites", "arguments": {}}}
    r = requests.post(f"{BASE}/mcp", headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    text = r.text
    for line in text.split('\n'):
        if line.strip().startswith('data: '):
            data = json.loads(line[6:])
            if "error" in data:
                raise RuntimeError(f"Token test failed: {data['error']}")
            print("  Token test OK \u2014 list_sites returned:",
                  data["result"]["content"][0]["text"][:80])
            return


# ── Main flow ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("GMA Web OAuth 2.0 + PKCE \u2014 One-time setup")
    print("=" * 60)

    # 1. Register (or reuse client_id) and generate PKCE pair
    if STATE_FILE.exists():
        saved = json.loads(STATE_FILE.read_text())
        client_id   = saved["client_id"]
        verifier    = saved["verifier"]
        saved_state = saved["state"]
        print(f"Reusing client_id from state file: {client_id}")
    else:
        client_id   = register_client()
        verifier, _ = pkce_pair()
        saved_state = b64url(secrets.token_bytes(16))
        STATE_FILE.write_text(json.dumps({
            "client_id": client_id,
            "verifier": verifier,
            "state": saved_state,
        }))
        print(f"Registered client: {client_id}")

    # 2. Build auth URL (challenge = base64url(SHA256(verifier)))
    challenge = b64url(hashlib.sha256(verifier.encode()).digest())
    auth_url = (
        f"{BASE}/oauth/authorize"
        f"?client_id={client_id}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&code_challenge={challenge}"
        f"&code_challenge_method=S256"
        f"&state={saved_state}"
    )

    print(f"\nOpening browser for sign-in...")
    print(f"  (or manually visit: {auth_url})\n")
    webbrowser.open(auth_url)

    # 3. Start local server to catch callback
    server, Handler = start_callback_server()
    print("Waiting for callback on http://127.0.0.1:8765 ...")
    while not server.should_stop:
        server.handle_request()
    server.server_close()
    code = Handler._code
    returned_state = Handler._state
    print(f"  Got code, state={returned_state[:8]}...")

    if returned_state != saved_state:
        print("ERROR: state mismatch! Possible CSRF. Run again.")
        sys.exit(1)

    # 4. Exchange code for tokens
    print("Exchanging code for tokens...")
    tokens = exchange_code(client_id, code, verifier)
    print(f"  access_token: {tokens['access_token'][:20]}...")
    print(f"  expires_in:   {tokens.get('expires_in')}s")

    # 5. Save token
    token_data = {
        "access_token":  tokens["access_token"],
        "refresh_token": tokens.get("refresh_token", ""),
        "expires_in":    tokens.get("expires_in", 900),
        "client_id":     client_id,
        "saved_at":      time.time(),
    }
    TOKEN_FILE.write_text(json.dumps(token_data, indent=2))
    print(f"\nToken saved to: {TOKEN_FILE}")

    # 6. Clean up state file
    STATE_FILE.unlink(missing_ok=True)

    # 7. Test
    print("\nTesting token...")
    test_token(token_data["access_token"])
    print("\n\u2705 OAuth setup complete! gma_client.py is ready.")


if __name__ == "__main__":
    main()
