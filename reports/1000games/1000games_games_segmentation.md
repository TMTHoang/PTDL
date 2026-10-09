# 1000games.io Portfolio Analysis

**Window:** 2026-09-10 → 2026-10-08  (28 days)  
**Site:** `1000games.io`  
**Generated:** 2026-10-09  
**Source:** `1000games_all.csv` (485 games)  
**Engagement metrics:** `1000games_p50p90_engpct.csv` (97 rows)  

---

## 1. Executive summary

- **Catalog size:** 485 games (those with any `users_with_as_top`)
- **Top 20%:** 97 games carry **82.8%** of users and **85.1%** of pageviews
- **Total users (catalog):** 37,986  |  **Total PV:** 410,891  |  **Top-game PV:** 101,264
- **Median engagement rate (top 20%):** 43.6%  |  **mean:** 42.2%
- **Session duration — p50:** 7.1s  |  **p90:** 142.8s  |  **avg:** 56.0s
- **Tier split (top 20%):** 19 T1_Star · 29 T2_Niche_Loyal · 34 T3_Discovery · 15 T4_Underperformer

## 2. Portfolio concentration

| Slice | N | % users_with_as_top | % total_pv | % top_game_pv |
|---|---:|---:|---:|---:|
| Top 5% | 24 | 50.4% | 51.5% | 55.0% |
| Top 10% | 48 | 67.0% | 69.0% | 71.8% |
| Top 20% | 97 | 82.8% | 85.1% | 87.1% |
| Top 30% | 146 | 89.9% | 91.1% | 92.2% |
| Top 50% | 242 | 96.1% | 96.8% | 97.2% |
| All | 485 | 100.0% | 100.0% | 100.0% |

The catalog is **classic 80/20**: the top 97 games (20% of the catalog) account for 82.8% of users and 85.1% of pageviews. The bottom 50% of the catalog collectively drives only ~3.9% of users.

## 3. Tier classification (top 20%)

| Tier | Definition | Count |
|---|---|---:|
| T1_Star | Top 20% of top-20%, or users_with_as_top ≥ 1,000 | 19 |
| T2_Niche_Loyal | Top 50% of top-20%, or users_with_as_top ≥ 300 | 29 |
| T3_Discovery | Top 75% of top-20%, or users_with_as_top ≥ 100 | 34 |
| T4_Underperformer | Bottom 25% of top-20% with < 100 users | 15 |

## 4. Headline acts (top 10 by users_with_as_top)

| # | Slug | Genre | users | PV | top-game PV | avg_top_share | eng% | p50 | p90 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `slope-2` | action | 2,135 | 26,920 | 7,100 | 0.406 | 45.0% | 4.8s | 162.4s |
| 2 | `dummies-world-cup` | sports | 2,088 | 15,466 | 6,778 | 0.697 | 32.1% | 4.2s | 65.0s |
| 3 | `survival-race` | sports | 1,947 | 19,070 | 4,583 | 0.412 | 45.2% | 7.9s | 157.5s |
| 4 | `golf-hit` | sports | 1,604 | 18,734 | 4,848 | 0.397 | 45.1% | 3.8s | 128.7s |
| 5 | `polytrack` | sports | 1,374 | 16,531 | 4,359 | 0.434 | 40.9% | 5.1s | 90.3s |
| 6 | `bowmasters-archery-shooting` | action | 1,070 | 13,258 | 3,262 | 0.384 | 53.3% | 9.9s | 306.5s |
| 7 | `frontwarsio` | strategy | 1,025 | 17,131 | 4,869 | 0.436 | 46.8% | 4.5s | 94.3s |
| 8 | `2v2-io` | action | 724 | 8,973 | 2,259 | 0.402 | 46.7% | 9.5s | 158.2s |
| 9 | `flip-rush` | action | 611 | 8,456 | 2,059 | 0.408 | 46.1% | 4.7s | 146.4s |
| 10 | `veck-io` | action | 533 | 6,746 | 1,761 | 0.417 | 45.7% | 8.1s | 173.6s |

## 5. Genre breakdown (top 20%)

| Genre | Games | users | % users | PV | % PV | top-game PV | % top-game PV |
|---|---:|---:|---:|---:|---:|---:|---:|
| sports | 27 | 12,365 | 39.3% | 127,102 | 36.4% | 33,239 | 37.7% |
| action | 23 | 8,728 | 27.8% | 107,869 | 30.9% | 26,690 | 30.2% |
| arcade | 18 | 3,816 | 12.1% | 41,125 | 11.8% | 8,637 | 9.8% |
| strategy | 4 | 1,411 | 4.5% | 22,616 | 6.5% | 6,408 | 7.3% |
| 1000games | 6 | 1,138 | 3.6% | 9,919 | 2.8% | 2,281 | 2.6% |
| casual | 4 | 1,045 | 3.3% | 10,243 | 2.9% | 2,479 | 2.8% |
| simulation | 3 | 965 | 3.1% | 6,551 | 1.9% | 2,336 | 2.6% |
| puzzle | 6 | 905 | 2.9% | 8,010 | 2.3% | 1,733 | 2.0% |
| adventure | 4 | 787 | 2.5% | 13,378 | 3.8% | 3,937 | 4.5% |
| horror | 2 | 290 | 0.9% | 2,837 | 0.8% | 503 | 0.6% |

## 6. Top tags (top 20%, by summed users_with_as_top)

| Tag | Games | users | % users |
|---|---:|---:|---:|
| Skill Games | 95 | 30,888 | 98.2% |
| Multiplayer Games | 68 | 25,344 | 80.6% |
| Fast Paced Games | 47 | 20,445 | 65.0% |
| Physics Games | 47 | 19,409 | 61.7% |
| Scary Games | 44 | 18,142 | 57.7% |
| Obstacle Games | 55 | 17,354 | 55.2% |
| Score Games | 37 | 15,747 | 50.1% |
| Escape Games | 35 | 15,586 | 49.6% |
| Driving Games | 46 | 14,592 | 46.4% |
| Competition Games | 32 | 13,694 | 43.5% |
| Reflex Games | 22 | 11,073 | 35.2% |
| Racing Games | 23 | 9,191 | 29.2% |
| Survival Games | 21 | 9,181 | 29.2% |
| Exploration Games | 22 | 8,248 | 26.2% |
| Jump Games | 21 | 8,203 | 26.1% |
| Soccer Games | 21 | 8,111 | 25.8% |
| FPS Games | 24 | 7,816 | 24.9% |
| Speed Games | 15 | 7,499 | 23.8% |
| PvP Games | 13 | 7,447 | 23.7% |
| Battle Games | 15 | 6,813 | 21.7% |
| Car Games | 20 | 6,429 | 20.4% |
| Shooting Games | 18 | 5,703 | 18.1% |
| Sandbox Games | 17 | 5,555 | 17.7% |
| Challenge Games | 6 | 4,512 | 14.3% |
| Animals Games | 13 | 4,368 | 13.9% |

## 7. Engagement deep-dive (top 20%)

Across the top 20%, a session is counted as **engaged** if total time on that game > 30s.

- **engagement rate (eng%)** — share of users spending > 30s on the game
  - median **43.6%**  |  mean **42.2%**  |  min 5.6%  |  max 57.0%
- **session duration p50** — median session length
  - median **7.1s**  |  mean **7.5s**
- **session duration p90** — 90th-percentile session length
  - median **142.8s**  |  mean **142.6s**
- **avg session** — mean session length
  - median **55.2s**  |  mean **56.0s**

### 8.1 Watchlist — high-traffic, low-engagement

Big-audience games where the engagement rate is below median — most leverage opportunity.

| # | Slug | users | eng% | p50 | p90 |
|---:|---|---:|---:|---:|---:|
| 1 | `gta-san-andreas` | 223 | 23.2% | 6.6s | 67.7s |
| 2 | `garrys-mod` | 455 | 24.6% | 5.6s | 66.4s |
| 3 | `steal-an-egg` | 273 | 26.9% | 7.2s | 76.9s |
| 4 | `size-it-up` | 416 | 28.7% | 4.5s | 107.4s |
| 5 | `geometry-dash` | 441 | 31.8% | 0.0s | 164.7s |
| 6 | `dummies-world-cup` | 2,088 | 32.1% | 4.2s | 65.0s |
| 7 | `super-liquid-soccer` | 349 | 33.8% | 3.3s | 77.4s |
| 8 | `meccha-chameleon` | 382 | 35.4% | 9.0s | 153.2s |
| 9 | `red-face-horror` | 222 | 35.8% | 3.8s | 149.4s |
| 10 | `speed-stars` | 388 | 37.4% | 12.2s | 137.5s |

### 8.2 Hidden gems — high-engagement, mid-audience

Smaller-audience games with strong engagement — candidates to surface more aggressively.

| # | Slug | users | eng% | p50 | p90 |
|---:|---|---:|---:|---:|---:|
| 1 | `deer-adventure` | 193 | 57.0% | 13.3s | 146.8s |
| 2 | `pokerogue` | 104 | 55.8% | 11.7s | 135.7s |
| 3 | `bloxd-io` | 154 | 54.4% | 8.3s | 83.2s |
| 4 | `minefunio` | 309 | 54.1% | 3.0s | 90.1s |
| 5 | `soflo-wheelie-life` | 177 | 52.7% | 16.4s | 136.5s |
| 6 | `rider-rush` | 131 | 52.4% | 18.9s | 114.8s |
| 7 | `bow-battle` | 456 | 51.6% | 9.9s | 299.0s |
| 8 | `fish-it-online` | 107 | 50.9% | 13.1s | 222.7s |
| 9 | `tag-game` | 113 | 50.3% | 11.8s | 168.8s |
| 10 | `real-war-not-fake` | 324 | 49.9% | 11.2s | 111.2s |

---

**Files generated:**

- `1000games_portfolio_report.md` — this report
- `1000games_portfolio_supporting.csv` — full top-20% with tier + engagement metrics
- `1000games_portfolio_genre.csv` — genre breakdown
- `1000games_portfolio_tags.csv` — top-60 tags

**Methodology:**

- `users_with_as_top` = unique users who had this game as their top game during the window
- `total_pv` = total pageviews to the game's page
- `top_game_pv` = pageviews where this game was the top game
- `avg_top_share` = mean of `top_game_pv / total_pv` across users who ranked this game top
- `eng%` = share of users with > 30s total time on the game (engaged = yes)
- `p50` / `p90` = median / 90th-percentile session duration in seconds
- Tier classification uses rank within top-20% with absolute-volume overrides (see §3).
