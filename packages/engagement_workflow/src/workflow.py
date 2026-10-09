"""
Engagement Workflow — single entry point for packaging as a standalone .exe.

Usage (after packaging):
    1. Double-click "EngagementWorkflow.exe" (Windows) or run from terminal.
    2. Follow the on-screen wizard.
    3. Output: <out_dir>/dashboard_batch<N>.html + insights_batch<N>.md + _batch<N>_results_v2.json

Pre-requisites baked into the .exe:
    - gma_client.py  (OAuth + auto-refresh)
    - gma_oauth.py   (one-time OAuth flow)
    - build_dashboard.py (HTML dashboard builder)
    - .gma_token.json (token cache, auto-created on first run)

This script does NOT modify the source files in D:\\GR\\engagement_workflow.
It only reads from them and writes outputs to the user-chosen output folder.
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
import webbrowser
from datetime import date, datetime
from pathlib import Path

# ── PyInstaller-friendly path resolution ──────────────────────────────────────
# When running as a frozen .exe, sys._MEIPASS points to the bundle dir.
# When running as a normal .py, use the script's own directory.
if getattr(sys, "frozen", False):
    BUNDLE_DIR = Path(sys._MEIPASS)
else:
    BUNDLE_DIR = Path(__file__).resolve().parent

# ── Console encoding fix for Windows (cp1252 can't print box-drawing chars) ──
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass  # Python < 3.7 or already wrapped — fall through

# gma_client looks for the token at this exact path. We override by importing
# then setting TOKEN_FILE before any call.
import gma_client  # noqa: E402
from gma_client import call_mcp, refresh_if_needed  # noqa: E402

# All outputs go to user-chosen directory; defaults next to the .exe.
if getattr(sys, "frozen", False):
    EXE_DIR = Path(sys.executable).resolve().parent
else:
    EXE_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = EXE_DIR / "output"
# TOKEN_FILE is used as a default for the bundled token; ensure_auth() will
# redirect to the user-writable path at runtime.
TOKEN_FILE = BUNDLE_DIR / ".gma_token.json"
gma_client.TOKEN_FILE = TOKEN_FILE  # initial value; ensure_auth() will reassign


# ── Console UX helpers ────────────────────────────────────────────────────────

def hr(char="─", width=72):
    print(char * width)

def banner(title, sub=None):
    print()
    hr("═")
    print(f"  {title}")
    if sub:
        print(f"  {sub}")
    hr("═")

def ok(msg):   print(f"  [OK] {msg}")
def warn(msg): print(f"  [!]  {msg}")
def err(msg):  print(f"  [X]  {msg}")
def step(n, total, msg): print(f"\n  [{n}/{total}] {msg}")


def prompt_path(prompt_text, must_exist=True, default=None):
    """Friendly file path prompt — supports drag-and-drop into the console."""
    while True:
        if default:
            raw = input(f"  {prompt_text} [{default}]: ").strip()
        else:
            raw = input(f"  {prompt_text}: ").strip()
        # PowerShell drag-and-drop wraps in quotes
        if raw.startswith('"') and raw.endswith('"'):
            raw = raw[1:-1]
        if not raw and default:
            raw = default
        if not raw:
            print("    (path is required)")
            continue
        p = Path(raw)
        if must_exist and not p.exists():
            print(f"    File not found: {p}")
            continue
        return p


def prompt_yes_no(question, default_yes=True):
    suffix = "[Y/n]" if default_yes else "[y/N]"
    while True:
        ans = input(f"  {question} {suffix}: ").strip().lower()
        if not ans:
            return default_yes
        if ans in ("y", "yes"): return True
        if ans in ("n", "no"):  return False
        print("    (please answer y or n)")


# ── OAuth handling ───────────────────────────────────────────────────────────

def _get_user_token_path():
    """Resolve the writable token cache path.

    When running as a frozen .exe, the bundle lives in a temp dir (read-only).
    We mirror the token to a writable path next to the .exe.
    When running as a .py script, the script's directory is writable.
    """
    if getattr(sys, "frozen", False):
        return EXE_DIR / ".gma_token.json"
    return BUNDLE_DIR / ".gma_token.json"


def ensure_auth():
    """Make sure we have a valid token. If not, run the OAuth flow."""
    banner("Authentication", "OAuth 2.0 + PKCE against gma-web.readyplayer1.xyz")

    user_token = _get_user_token_path()
    # Point gma_client at the user-writable path
    gma_client.TOKEN_FILE = user_token

    if not user_token.exists():
        warn(f"No token cache at {user_token}. Starting one-time OAuth flow.")
        return _run_oauth_flow()

    try:
        d = json.loads(user_token.read_text())
        if d.get("access_token", "PLACEHOLDER") == "PLACEHOLDER":
            warn("Token cache is a placeholder. Re-running OAuth.")
            return _run_oauth_flow()
        # refresh if needed
        tok = refresh_if_needed()
        ok(f"Token valid (client_id={tok.get('client_id','?')[:24]}...)")
        return True
    except Exception as e:
        err(f"Token check failed: {e}")
        return _run_oauth_flow()


def _run_oauth_flow():
    """Run the OAuth flow by importing gma_oauth.main()."""
    print()
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │  A browser window will open for GMA Web sign-in.    │")
    print("  │  1. Sign in to your GMA Web account.                │")
    print("  │  2. Click 'Allow' to grant access.                  │")
    print("  │  3. The browser will redirect to localhost:8765     │")
    print("  │     and the workflow will continue automatically.   │")
    print("  └─────────────────────────────────────────────────────┘")
    print()
    try:
        sys.path.insert(0, str(BUNDLE_DIR))
        import gma_oauth
        # When frozen, write the token next to the .exe (writable) rather
        # than inside the read-only temp bundle.
        if getattr(sys, "frozen", False):
            user_token_path = EXE_DIR / ".gma_token.json"
        else:
            user_token_path = BUNDLE_DIR / ".gma_token.json"
        gma_oauth.TOKEN_FILE = user_token_path
        gma_client.TOKEN_FILE = user_token_path
        gma_oauth.main()
        ok(f"OAuth completed. Token saved -> {user_token_path}")
        return True
    except KeyboardInterrupt:
        err("OAuth cancelled by user.")
        return False
    except Exception as e:
        err(f"OAuth failed: {e}")
        return False


# ── CSV parsing (same logic as _batch_query_v2.py) ───────────────────────────

SITE_MAP = {
    "1games":   "1games.io",
    "1000games": "1000games.io",
    "zapgames": "zapgames.io",
    "Zapgames": "zapgames.io",
    "ZapGames": "zapgames.io",
    "1000Games": "1000games.io",
    "1Games":   "1games.io",
}


def resolve_date(raw):
    raw = (raw or "").strip()
    if not raw:
        return None
    if "/" in raw:
        d, m = raw.split("/", 1)
        return f"2026-{int(m):02d}-{int(d):02d}"
    if re.match(r"\d{4}-\d{2}-\d{2}", raw):
        return raw
    return raw


def parse_csv(csv_path):
    games = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            norm = {k.strip(): (v.strip() if v else v) for k, v in row.items()}
            slug = norm.get("Game_slug") or norm.get("slug")
            if not slug:
                continue
            games.append({
                "slug":           slug,
                "source":         norm.get("Source", ""),
                "site_id":        norm.get("Site", ""),
                "upload_date_raw": norm.get("Upload_date", ""),
            })
    return games


# ── ClickHouse query (same SQL as _batch_query_v2.py) ────────────────────────

def query_game(site_id, slug, start_date, end_date):
    q = f"""
    WITH raw_events AS (
        SELECT
            client_id,
            session_id,
            page_location,
            params_num['page_duration_seconds'] AS page_dur_s
        FROM gm_measurement_events
        WHERE event_name = 'page_exit'
          AND site_id = '{site_id}'
          AND shard_date BETWEEN '{start_date}' AND '{end_date}'
          AND client_id != '' AND session_id != '' AND bot = 0
          AND page_location LIKE '%{slug}%'
    ),
    sess AS (
        SELECT
            client_id,
            session_id,
            page_location,
            sum(page_dur_s) AS sess_dur
        FROM raw_events
        GROUP BY client_id, session_id, page_location
    ),
    per_user AS (
        SELECT
            client_id,
            page_location,
            sum(sess_dur) AS user_dur,
            uniqExact(session_id) AS n_sessions,
            if(sum(sess_dur) > 30, 1, 0) AS engaged
        FROM sess
        GROUP BY client_id, page_location
    )
    SELECT
        (SELECT count() FROM raw_events) AS measurements,
        (SELECT count() FROM sess) AS sessions,
        (SELECT count() FROM per_user) AS users,
        (SELECT sum(engaged) FROM per_user) AS eng_users,
        round((SELECT sum(engaged) FROM per_user) * 100.0 / nullIf((SELECT count() FROM per_user), 0), 2) AS eng_pct,
        round((SELECT avg(sess_dur) FROM sess), 2) AS s_avg_s,
        round((SELECT quantile(0.5)(sess_dur) FROM sess), 2) AS s_p50_s,
        round((SELECT quantile(0.9)(sess_dur) FROM sess), 2) AS s_p90_s
    """
    return call_mcp("run_query", {"sql": q})


# ── Run query for all games (with progress) ──────────────────────────────────

def run_batch(games, today):
    results = []
    total = len(games)
    for i, g in enumerate(games, 1):
        site_short = g["site_id"]
        site = SITE_MAP.get(site_short, site_short + ".io")
        slug = g["slug"]
        start = resolve_date(g["upload_date_raw"])
        if not start:
            warn(f"[{i}/{total}] Skipping {slug}: no upload_date")
            continue

        # If upload_date is after the cutoff, swap them so the range is valid
        if start > today:
            warn(f"[{i}/{total}] {slug}: upload_date {start} > today {today}; swapping range")
            start, today_eff = today, start
        else:
            today_eff = today

        sys.stdout.write(f"  [{i:>{len(str(total))}}/{total}] {slug:<40} ({g['source'] or '?':<6} on {site}, {start} -> {today_eff}) ... ")
        sys.stdout.flush()
        try:
            data = query_game(site, slug, start, today_eff)
            if not data or "rows" not in data or not data["rows"]:
                print("NO DATA")
                results.append({"site": site, "slug": slug, "source": g.get("source", ""),
                                "upload_date": start, "error": "no data"})
                continue
            r = data["rows"][0]
            out = {
                "site": site, "slug": slug, "source": g.get("source", ""), "upload_date": start,
                "measurements": r.get("measurements", "0"),
                "sessions":     r.get("sessions", "0"),
                "users":        r.get("users", "0"),
                "eng_users":    r.get("eng_users", "0"),
                "eng_pct":      r.get("eng_pct", "0"),
                "s_avg":        r.get("s_avg_s", "0"),
                "s_p50":        r.get("s_p50_s", "0"),
                "s_p90":        r.get("s_p90_s", "0"),
            }
            try:
                users_v = int(out['users'])
                pct_v   = float(out['eng_pct'])
                p50_v   = float(out['s_p50'])
            except (TypeError, ValueError):
                users_v, pct_v, p50_v = 0, 0.0, 0.0
            print(f"users={users_v:>5} eng%={pct_v:>6.2f}% s_p50={p50_v:>7.1f}s")
            results.append(out)
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({"site": site, "slug": slug, "source": g.get("source", ""),
                            "upload_date": start, "error": str(e)})
    return results


# ── Auto-generate Section 3 insights (markdown) ──────────────────────────────

def cohort_key(r):
    return (r.get("site", ""), r.get("upload_date", ""))


def best_per_metric(rows):
    """Pick the winner for each metric in a cohort, defensively against missing data."""
    def f(row, key):
        try:
            v = float(row.get(key, 0) or 0)
        except (TypeError, ValueError):
            return 0.0
        return v
    if not rows: return {}
    return {
        "users":   max(rows, key=lambda r: f(r, "users")),
        "eng_pct": max(rows, key=lambda r: f(r, "eng_pct")),
        "s_p50":   max(rows, key=lambda r: f(r, "s_p50")),
        "s_avg":   max(rows, key=lambda r: f(r, "s_avg")),
    }


def render_insights(results, batch_n, today):
    """Auto-generate Section 3 insights + cohort availability matrix."""
    valid = [r for r in results if "error" not in r]
    if not valid:
        return "# Insights\n\nNo valid rows.\n"

    # Group by (site, date)
    cohorts = {}
    for r in valid:
        cohorts.setdefault(cohort_key(r), []).append(r)

    # Sort cohorts: site then date
    site_order = {"1games.io": 0, "1000games.io": 1, "zapgames.io": 2}
    def cohort_sort_key(kv):
        site, dt = kv[0]
        return (site_order.get(site, 99), dt)
    sorted_cohorts = sorted(cohorts.items(), key=cohort_sort_key)

    today_disp = today
    sources = sorted({r.get("source", "") for r in valid})

    lines = []
    lines.append(f"# Batch-{batch_n} — Reading Insights (Section 3 only)")
    lines.append("")
    lines.append(f"> **Phiên bản:** 1.0 — Batch-{batch_n} (auto-generated)")
    lines.append(f"> **Ngày báo cáo:** {today_disp}")
    lines.append("> **Methodology:** v2 — `gm_measurement_events` / `page_exit` / `page_duration_seconds`")
    lines.append(f"> **Date range:** upload_date → {today_disp} inclusive")
    lines.append(f"> **Phạm vi:** {len(valid)} game across {len({r['site'] for r in valid})} sites × {len({r['upload_date'] for r in valid})} dates = **{len(sorted_cohorts)} cohort slots**")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## 3. Best Game per Cohort — Reading Insights")
    lines.append("")

    for idx, ((site, date_str), rows) in enumerate(sorted_cohorts, 1):
        src_counts = {s: sum(1 for r in rows if r.get("source") == s) for s in ["GR", "AZ", "owner"]}
        counts_str = " / ".join(f"{v} {k}" for k, v in src_counts.items() if v > 0)
        site_short = site.replace(".io", "")
        lines.append(f"### 3.{idx} {site_short} × {date_str[5:]} ({len(rows)} games: {counts_str})")

        winners = best_per_metric(rows)

        # Build a single line with all winners + their key metric
        parts = []
        for metric_key, metric_lbl in [("eng_pct", "Engagement"), ("s_p50", "Duration (S_p50)"), ("users", "Traffic")]:
            w = winners.get(metric_key)
            if not w: continue
            val = w.get(metric_key, "0")
            parts.append(f"{w['source'] or '?'} `{w['slug']}` thắng {metric_lbl} ({w.get(metric_key, '0')})")
        lines.append("**" + "; ".join(parts) + ".**")

        # Per-source comment line: pull the row with the highest s_p50 of that source
        for src in ["GR", "AZ", "owner"]:
            src_rows = [r for r in rows if r.get("source") == src]
            if not src_rows: continue
            top = max(src_rows, key=lambda r: float(r.get("s_p50", 0) or 0))
            try:
                users = int(top.get("users", 0))
            except (TypeError, ValueError):
                users = 0
            lines.append(
                f"- {src} `{top['slug']}`: {users:,} users, "
                f"Eng% {top.get('eng_pct', '0')}, S_avg {top.get('s_avg', '0')}s, S_p50 {top.get('s_p50', '0')}s"
            )

        # Caveat if all games have small sample
        try:
            max_users = max(int(r.get("users", 0) or 0) for r in rows)
        except ValueError:
            max_users = 0
        if max_users < 50:
            lines.append(f"  > Sample rất nhỏ (max users = {max_users}) — insights mang tính tham khảo, cần replicate.")
        lines.append("")

    # Cohort availability matrix
    lines.append("### Cohort availability matrix")
    lines.append("")
    lines.append("| Site × Date | GR | AZ | owner |")
    lines.append("|---|:-:|:-:|:-:|")
    for (site, date_str), rows in sorted_cohorts:
        site_short = site.replace(".io", "")
        present = {r.get("source", "") for r in rows}
        gr_slugs    = ", ".join(r["slug"] for r in rows if r.get("source") == "GR")    or "—"
        az_slugs    = ", ".join(r["slug"] for r in rows if r.get("source") == "AZ")    or "—"
        owner_slugs = ", ".join(r["slug"] for r in rows if r.get("source") == "owner") or "—"
        gr_cell    = f"✓ {gr_slugs}"    if "GR"    in present else "✗ none"
        az_cell    = f"✓ {az_slugs}"    if "AZ"    in present else "✗ none"
        owner_cell = f"✓ {owner_slugs}" if "owner" in present else "✗ none"
        lines.append(f"| {site_short} × {date_str[5:]} | {gr_cell} | {az_cell} | {owner_cell} |")
    lines.append("")

    lines.append("### Pattern tổng (batch auto-summary)")
    lines.append("")
    # Count GR/AZ/owner cohort wins by Eng%
    wins = {"GR": 0, "AZ": 0, "owner": 0}
    for _, rows in sorted_cohorts:
        w = best_per_metric(rows).get("eng_pct")
        if w: wins[w.get("source", "")] = wins.get(w.get("source", ""), 0) + 1
    lines.append(f"- **Engagement winners:** GR {wins.get('GR', 0)} | AZ {wins.get('AZ', 0)} | owner {wins.get('owner', 0)} (out of {len(sorted_cohorts)} cohorts)")
    # Find any cross-site portable slug
    from collections import Counter
    slug_sites = Counter()
    for r in valid:
        slug_sites[r["slug"]] += 1
    cross = [s for s, c in slug_sites.items() if c >= 2]
    if cross:
        lines.append(f"- **Cross-site portable games:** {', '.join('`' + s + '`' for s in cross)}")
    lines.append("")
    return "\n".join(lines)


# ── Main wizard ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--csv", help="Path to game_batch_N.csv (skip prompt)")
    parser.add_argument("--today", help="Cutoff date YYYY-MM-DD (default: today)")
    parser.add_argument("--out", help="Output directory (default: ./output)")
    parser.add_argument("--no-open", action="store_true", help="Don't open the dashboard in browser")
    parser.add_argument("--headless", action="store_true", help="No wizard — use only CLI args")
    args, _unknown = parser.parse_known_args()

    today = args.today or date.today().isoformat()
    out_dir = Path(args.out) if args.out else DEFAULT_OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    if not args.headless:
        banner("Engagement Workflow — Game Engagement Analytics",
               "Per-batch: CSV → query → dashboard + insights")
        print()
        print("  This tool queries ClickHouse via GMA Web MCP, then generates")
        print("  - a Plotly HTML dashboard")
        print("  - a Section-3 insights Markdown file")
        print("  - a raw results JSON")
        print()
        print(f"  Output folder: {out_dir}")
        print()

    # 1. Auth
    if not ensure_auth():
        err("Authentication failed. Cannot continue.")
        return 1

    # 2. CSV input
    if args.csv:
        csv_path = Path(args.csv)
        if not csv_path.exists():
            err(f"CSV not found: {csv_path}")
            return 1
    else:
        step(1, 3, "Select your batch CSV")
        print("  Expected columns: Game_slug, Source, Site, Upload_date")
        print("  (drag-and-drop into the console also works)")
        csv_path = prompt_path("Path to game_batch_N.csv")

    games = parse_csv(csv_path)
    if not games:
        err("No valid rows in CSV (need Game_slug + Site + Upload_date).")
        return 1
    ok(f"Parsed {len(games)} games from {csv_path.name}")

    # Derive batch number from filename
    m = re.search(r"game_batch[_-]?(\d+)", csv_path.name, re.IGNORECASE)
    batch_n = m.group(1) if m else datetime.now().strftime("%Y%m%d%H%M%S")

    if not args.headless:
        step(2, 3, f"Querying {len(games)} games (cutoff: {today})")
        print("  Methodology: v2 — gm_measurement_events / page_exit / page_duration_seconds")
        print()
    else:
        print(f"[{datetime.now().isoformat()}] Querying {len(games)} games (cutoff {today}) ...")

    t0 = time.time()
    results = run_batch(games, today)
    elapsed = time.time() - t0
    ok(f"Query done in {elapsed:.1f}s — {sum(1 for r in results if 'error' not in r)} ok, {sum(1 for r in results if 'error' in r)} errored")

    # 3. Save raw JSON
    json_path = out_dir / f"_batch{batch_n}_results_v2.json"
    json_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    ok(f"Raw results  -> {json_path}")

    # 4. Build dashboard
    valid = [r for r in results if "error" not in r]
    if not valid:
        err("No valid rows — cannot build dashboard.")
        return 1

    if not args.headless:
        step(3, 3, "Building dashboard + insights")
    sys.path.insert(0, str(BUNDLE_DIR))
    from build_dashboard import build_dashboard  # type: ignore

    today_disp = today[5:].replace("-", "/")  # 2026-10-08 -> 10/08
    title = f"Batch-{batch_n} Game Metrics Dashboard ({today_disp})"
    html_str = build_dashboard(valid, title)
    html_path = out_dir / f"dashboard_batch{batch_n}.html"
    html_path.write_text(html_str, encoding="utf-8")
    ok(f"Dashboard    -> {html_path}  ({len(html_str):,} bytes)")

    # 5. Build insights
    insights_md = render_insights(valid, batch_n, today)
    md_path = out_dir / f"insights_batch{batch_n}.md"
    md_path.write_text(insights_md, encoding="utf-8")
    ok(f"Insights     -> {md_path}  ({len(insights_md):,} chars)")

    # 6. Done
    if not args.headless:
        hr("═")
        print("  DONE")
        print(f"  Open the dashboard:  {html_path}")
        print(f"  Read the insights:   {md_path}")
        print(f"  Raw data:            {json_path}")
        hr("═")
        if prompt_yes_no("Open the dashboard in your browser now?", default_yes=True):
            webbrowser.open(html_path.as_uri())
    else:
        print(f"[{datetime.now().isoformat()}] Done. Dashboard: {html_path}  Insights: {md_path}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n  Interrupted.")
        sys.exit(130)
