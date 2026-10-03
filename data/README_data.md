# Data folder — User Segmentation

This folder contains the **proof data** for the 1games.io user segmentation project.

## Files

| File | Size | Role |
|---|---|---|
| `clusters_1games_2026-10-01.csv` | 6.6 MB | **32,701 users × 36 columns** — features + `cluster_id` (0, 1, or 2) |
| `user_features_1games_2026-10-01.csv` | 6.7 MB | 32,701 users × 35 columns — features only (no `cluster_id`) |
| `cluster_report.md` | 2.6 KB | numeric profile per cluster (mean / median for each feature) |
| `cluster_summary.md` | 1.7 KB | short summary |
| `cluster_insights/` | — | per-cluster top games, tags, genres (CSVs + JSON) |

## Main CSV columns

The 36 columns in `clusters_1games_2026-10-01.csv`:

| Column | Meaning |
|---|---|
| `client_id` | User ID (float) |
| `cluster_id` | 0 = Casual browser, 1 = Bounce / nav-only, 2 = Power user |
| `total_pv` | Total page views in 28 days |
| `distinct_games` | Number of distinct games played |
| `top_game_slug` | The user's most-viewed game (slug) |
| `top_game_pv` | PV for that top game |
| `top_game_share` | % of user's PV that went to top game |
| `sessions` | Number of sessions |
| `engaged_sessions` | Sessions > 10 sec |
| `engaged_session_pct` | engaged / total sessions |
| `avg_session_sec` | Average session length in seconds |
| `total_session_sec` | Total session time in seconds |
| `active_days` | Days with at least 1 page view |
| `first_local_date` | First day user appeared |
| `last_local_date` | Last day user appeared |
| `days_since_last_visit` | Days since last visit (window end) |
| `sessions_last_7d` | Sessions in last 7 days |
| `sessions_last_14d` | Sessions in last 14 days |
| `home_pv` | Page views on home page |
| `category_browse_pv` | Page views on category / hub pages |
| `search_pv` | Page views starting with `/search` |
| `direct_game_pv` | Page views on individual game pages |
| `home_share`, `category_browse_share`, `search_share`, `direct_game_share` | Same, as % of total PV |
| `tag_diversity` | Number of distinct tags across user's games |
| `tag_entropy` | Shannon entropy of tag distribution |
| `distinct_genres` | Number of distinct genres |
| `dominant_tag` | Most-frequent tag |
| `dominant_tag_pv` | PV of dominant tag |
| `dominant_tag_share` | % of tag-PV that went to dominant tag |
| `dominant_genre` | Most-frequent genre |
| `dominant_genre_pv`, `dominant_genre_share` | Same |

## How to verify a claim

**Example:** "Casual browser is 14,052 users"

1. Open `clusters_1games_2026-10-01.csv` in Excel / pandas
2. Filter `cluster_id = 0`
3. Count rows → 14,052

**Example:** "Top game for Casual browser is Challenge Rush"

1. Filter `cluster_id = 0`
2. Group by `top_game_slug`, count users
3. Sort descending → Challenge Rush (1,138 users in chunks subset, 1,836 in full cluster)

**Example:** "Slope 2 has 2,855 Power users"

1. Filter `cluster_id = 2`
2. Filter `top_game_slug = "slope-2"`
3. Count → 1,975 (top_game_count) or use `cluster_insights/cluster2_top_games_by_users.csv` for chunks subset

## Cluster sizes

| Cluster | Label | Users | % |
|---:|---|---:|---:|
| 0 | Casual browser | 14,052 | 43% |
| 1 | Bounce / nav-only | 7,070 | 22% |
| 2 | Power user | 11,579 | 35% |
| | **Total** | **32,701** | **100%** |

## Caveats

- **32,701 rows have 32,593 unique client_ids** — there are 108 duplicate rows in the source data; the duplicates do not affect cluster assignment (cluster is on unique IDs).
- **58% of cluster users (19,166 / 32,701) have `top_slugs` data in chunks.** The cluster_insights/ files are computed on this 58%. To get full-cluster counts, use `clusters_1games_2026-10-01.csv` columns (`top_game_slug`, `dominant_tag`, `dominant_genre`) instead.
- **Game metadata covers 886 / 1,851 unique slugs.** Tag/genre analysis is only for games in `games_meta_normalized.csv`. The 577 Bounce users who clicked games all clicked on games missing from metadata.

See `../README.md` for the full project structure and `../methodology/User_Segmentation_Methodology_v3.md` for how the features were computed.
