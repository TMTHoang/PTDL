# Engagement Workflow — Standalone Package

> **One file. No Python. No IDE. Double-click and it runs.**

## What it does

```
CSV file (game_batch_N.csv)
        │
        ▼
  EngagementWorkflow.exe  ── OAuth if needed ──► ClickHouse
                                              (gm_measurement_events)
                                                      │
                                    ┌─────────────────┼─────────────────┐
                                    ▼                 ▼                 ▼
                    dashboard_batch<N>.html   insights_batch<N>.md   _batch<N>_results_v2.json
                    (interactive Plotly)      (Section 3 markdown)    (raw JSON)
```

**Output:** a Plotly HTML dashboard + Section-3 insights markdown with the best game per cohort.

---

## Usage (3 steps)

### Step 1 — Copy to the new machine

Copy the entire `engagement_workflow` folder to the new machine. You only need:
- `EngagementWorkflow.exe` — the main program
- `.gma_token.json` — your OAuth token (export from the original machine, see below)

If you don't have a token, the first run will open a browser for OAuth sign-in.

### Step 2 — Export your OAuth token

On the original machine, run:
```powershell
Copy-Item "D:\GR\.gma_token.json" "D:\packages\engagement_workflow\dist\.gma_token.json"
```
Or copy the file manually to the new machine's `dist/` folder next to the .exe.

> **On a brand-new machine with no token:** The .exe will launch the OAuth flow automatically.
> It opens your browser to `gma-web.readyplayer1.xyz`. Sign in, click "Allow",
> and the token is saved next to the .exe automatically.

### Step 3 — Run

**Interactive (wizard):**
```
Double-click EngagementWorkflow.exe
```
- It will ask for the path to your `game_batch_N.csv`
- It will ask for a cutoff date (default: today)
- It will query ClickHouse and generate the dashboard + insights

**CLI mode (no prompts):**
```
EngagementWorkflow.exe --csv "C:\path\to\game_batch_N.csv" --today 2026-10-09
```

**CLI mode (with custom output folder):**
```
EngagementWorkflow.exe --csv "C:\path\to\game_batch_N.csv" --out "D:\reports"
```

---

## CSV format

Expected columns in `game_batch_N.csv`:

| Column | Example | Notes |
|---|---|---|
| `Game_slug` | `snake-game` | Game URL slug |
| `Source` | `GR` | One of: `GR`, `AZ`, `owner` |
| `Site` | `1games` | One of: `1games`, `1000games`, `zapgames` |
| `Upload_date` | `1/10` or `2026-10-01` | D/M or ISO format |

Example `game_batch_6.csv`:
```
Game_slug,Source,Site,Upload_date
snake-game,owner,1games,1/10
vex-10,owner,1games,1/10
collect-all-the-leaves,GR,1games,1/10
```

---

## Output files

All output goes to `D:\packages\engagement_workflow\dist\output\` (next to the .exe):

| File | What it is |
|---|---|
| `dashboard_batch<N>.html` | Interactive Plotly dashboard — open in any browser |
| `insights_batch<N>.md` | Section-3 insights: best game per cohort, availability matrix, pattern summary |
| `_batch<N>_results_v2.json` | Raw ClickHouse output — 12 metrics per game |

---

## First-run OAuth (what to expect)

```
══════════════════════════════════════════════════════════════════════
  Engagement Workflow — Game Engagement Analytics
══════════════════════════════════════════════════════════════════════
  [OK] No token cache. Starting one-time OAuth flow.

  ┌──────────────────────────────────────────────────────┐
  │  A browser window will open for GMA Web sign-in.     │
  │  1. Sign in to your GMA Web account.                │
  │  2. Click 'Allow' to grant access.                  │
  │  3. The browser will redirect to localhost:8765      │
  └──────────────────────────────────────────────────────┘

  Opening browser for sign-in...
  Waiting for callback on http://127.0.0.1:8765 ...
  Got code, state=...
  OAuth completed. Token saved.
```

---

## Command-line options

| Flag | What it does |
|---|---|
| `--csv "path"` | Skip CSV prompt, use this file |
| `--today YYYY-MM-DD` | Cutoff date (default: today) |
| `--out "path"` | Output directory (default: next to .exe/output/) |
| `--headless` | No prompts, run fully automated |
| `--no-open` | Don't open dashboard in browser after completion |

---

## Troubleshooting

### "401 unauthenticated" / "Token expired"
Re-run OAuth:
```
EngagementWorkflow.exe --headless --csv "dummy.csv"
```
The .exe will detect the expired token and re-run the OAuth flow.

### "Port 8765 already in use"
Close other programs using port 8765, then retry.

### "NO DATA" for some games
Expected if games were uploaded today (no data yet) or if the slug doesn't match the ClickHouse records. Check `upload_date` — the query window is `upload_date → today`.

---

## Methodology

- **Table:** `gm_measurement_events`
- **Event:** `page_exit`
- **Duration:** `params_num['page_duration_seconds']` (wall-time)
- **Filters:** `bot = 0`, `client_id != ''`, `session_id != ''`
- **Engagement:** `sum(page_dur_s) > 30s` per `(client_id, session_id, page_location)`
- **Eng%:** `engaged_users / total_users × 100`

Full spec: `D:\GR\engagement_workflow\docs\methodology_v2.md`

---

## Package info

- **Built with:** PyInstaller 6.22.3
- **Python:** bundled (no Python installation needed)
- **Size:** ~12 MB (standalone)
- **Requires:** Windows, internet access to `gma-web.readyplayer1.xyz`
