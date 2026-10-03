# Cluster analysis - 1games.io - 2026-10-01

## Result

K-Means selected **K=3** (silhouette 0.37, the highest among K=3,4,5).

## The three clusters

| Cluster | n | % | Label | Defining behavior |
|---|---|---|---|---|
| **C0** | 14,052 | 43% | Casual browser | 1-2 sessions, 6 PVs, plays 1-2 different games, mostly direct visits. Came, played, left. Old (>25 days). |
| **C1** | 7,070 | 22% | Bounce / nav-only | 1 session, 0 games played, 80% home-page visits. Came, didn't click into a game, left. |
| **C2** | 11,579 | 35% | Power user | 15 sessions, 48 PVs, 9.8 distinct games, broad taste (37 tags, 5 genres). Recent (last visit ~10d ago). |

## How this is different from the old doc

The old segmentation produced C0/C1/C2 = low/medium/high activity, with manual centroids.
That solution was one-dimensional (volume) and didn't distinguish intent.

The new K-Means, on 25 features across 7 behavioral dimensions, surfaced:

- The same low/high activity split (Cluster 0 vs 2)
- **Plus** a meaningful new segment (Cluster 1) that the old solution missed:
  - users who came to the site, hit the home page, but never clicked into a game
  - they exist because volume features can't tell "play" from "look"

This validates the seven-dimension design from the feedback file: the new solution
captures behavioral segments, not just activity volumes.

## Files

| File | Content |
|---|---|
| `user_features_1games_2026-10-01.csv` | 32,701 users x 35 columns, the input |
| `d:\GR\03_data\processed\user_features\clusters_1games_2026-10-01.csv` | same + cluster_id |
| `cluster_report.md` | full cluster profile tables |
| `cluster_users.py` | the script that produced this |