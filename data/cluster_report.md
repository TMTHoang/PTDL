# Cluster report - 1games.io - 2026-10-01

Total users clustered: **32701**
K selection sweep: K in [3, 4, 5]

| K | silhouette | inertia | cluster sizes |
|---|---|---|---|
| 3 | 0.3685 | 371235.9 | c0:14052, c1:7070, c2:11579 |
| 4 | 0.3167 | 322792.6 | c0:8951, c1:9285, c2:7432, c3:7033 |
| 5 | 0.3035 | 291765.7 | c0:9060, c1:8237, c2:6757, c3:3531, c4:5116 |

**Selected K = 3** (highest silhouette).

## Cluster profiles (raw mean per cluster)

| feature | c0 | c1 | c2 |
|---|---|---|---|
| total_pv | 5.986 | 1.276 | 48.073 |
| distinct_games | 2.265 | 0.000 | 9.766 |
| top_game_pv | 2.370 | 0.100 | 13.164 |
| top_game_share | 0.540 | 0.057 | 0.262 |
| sessions | 2.070 | 1.069 | 15.476 |
| engaged_session_pct | 0.635 | 0.116 | 0.692 |
| avg_session_sec | 392.737 | 26.134 | 791.256 |
| total_session_sec | 788.675 | 32.605 | 12284.822 |
| active_days | 1.658 | 1.047 | 8.315 |
| days_since_last_visit | 25.236 | 27.746 | 10.317 |
| sessions_last_7d | 0.010 | 0.002 | 0.908 |
| sessions_last_14d | 0.106 | 0.008 | 4.876 |
| home_pv | 1.230 | 0.918 | 10.321 |
| category_browse_pv | 0.242 | 0.049 | 2.593 |
| search_pv | 0.165 | 0.036 | 1.339 |
| direct_game_pv | 4.181 | 0.111 | 32.811 |
| home_share | 0.183 | 0.803 | 0.201 |
| category_browse_share | 0.027 | 0.017 | 0.058 |
| search_share | 0.021 | 0.011 | 0.028 |
| direct_game_share | 0.746 | 0.059 | 0.690 |
| tag_diversity | 11.790 | 0.000 | 36.742 |
| tag_entropy | 3.230 | 0.000 | 4.526 |
| distinct_genres | 1.773 | 0.000 | 4.967 |
| dominant_tag_share | 0.139 | 0.000 | 0.103 |
| dominant_genre_share | 0.800 | 0.000 | 0.538 |

## Top 5 dominant_genre per cluster

### Cluster 0 (n=14052)
- arcade : 3782 (26.9%)
- action : 3194 (22.7%)
- sports : 1624 (11.6%)
- adventure : 1621 (11.5%)
- platform : 1241 (8.8%)

### Cluster 1 (n=7070)

### Cluster 2 (n=11579)
- arcade : 4166 (36.0%)
- action : 2736 (23.6%)
- sports : 1282 (11.1%)
- adventure : 1157 (10.0%)
- driving : 926 (8.0%)

## Top 10 dominant_tag per cluster

### Cluster 0 (n=14052)
- arcade : 3103 (22.1%)
- action : 2430 (17.3%)
- sports : 1414 (10.1%)
- adventure : 1218 (8.7%)
- platform : 1145 (8.1%)
- driving : 1022 (7.3%)
- skill : 612 (4.4%)
- physics : 510 (3.6%)
- clicker : 430 (3.1%)
- casual : 321 (2.3%)

### Cluster 1 (n=7070)

### Cluster 2 (n=11579)
- arcade : 2992 (25.8%)
- physics : 1342 (11.6%)
- skill : 1286 (11.1%)
- action : 1134 (9.8%)
- sports : 835 (7.2%)
- driving : 574 (5.0%)
- fast-paced : 467 (4.0%)
- avoid : 406 (3.5%)
- adventure : 364 (3.1%)
- casual : 312 (2.7%)
