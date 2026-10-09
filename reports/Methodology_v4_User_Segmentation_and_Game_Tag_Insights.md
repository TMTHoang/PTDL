# User Segmentation & Game-Tag Insights — Methodology

**Version:** 4.0
**Date:** October 9, 2026
**Scope:** End-to-end pipeline used to generate `insights_user_segments_<site>_VI.md` and `insights_games_tags_<site>_VI.md` for the three sites: `1games.io`, `zapgames.io`, `1000games.io`
**Applies to:** 1games (window 2026-09-03 → 2026-10-01, 28d), zapgames (window 2026-09-03 → 2026-10-01, 28d), 1000games (window 2026-09-10 → 2026-10-01, 22d — only available history)
**Reference date:** 2026-10-01 (last day of window for all sites)
**Author:** Game analytics

---

## 0. Tổng quan pipeline

```
[ClickHouse: gm_pages]                       [Site catalog CSV]
        │                                            │
        ▼                                            ▼
   Step 1: User features (23-25 features)      [games_meta]
        │                                            │
        │                                            │
        ▼                                            │
   Step 2: K-Means clustering (K=3)                  │
        │                                            │
        ▼                                            │
   Step 3: Per-cluster game/tag/genre                │
        │              ▲                             │
        │              └──────── join ───────────────┘
        ▼
   Step 4: Write Vietnamese report
```

Bốn bước chính:

| Bước | Mục tiêu | Đầu vào | Đầu ra |
|---|---|---|---|
| **1. User features** | Tính 23-25 đặc trưng hành vi cho mỗi user | `gm_pages` ClickHouse | `user_features_<site>_<date>.csv` |
| **2. Clustering** | Nhóm user thành K=3 phân khúc bằng K-Means | features CSV | `clusters_<site>_<date>.csv` (thêm cột `cluster_id`) |
| **3. Game/tag insights** | Với mỗi cụm, tính top game/tag/genre + câu chuyện | clusters CSV + chunk slug data + catalog CSV | `insights_<site>_tags/cluster0/...`, `cluster1/...`, `cluster2/...` + `summary.json` |
| **4. Báo cáo** | Viết 2 file `.md` tiếng Việt cho từng site | tất cả CSV/JSON ở trên | `insights_user_segments_<site>_VI.md` + `insights_games_tags_<site>_VI.md` |

**Tại sao tách thành 4 bước?** Vì mỗi bước có thể chạy độc lập, dễ debug, và cho phép tái sử dụng `clusters_<site>.csv` ở các phân tích sau (journey, retention, …).

---

## 1. Định nghĩa cohort

### 1.1 Mature cohort (≥1 page view trong window)

**Áp dụng cho:** 1games và zapgames (28 ngày)
**Công thức:**

```sql
SELECT client_id
FROM gm_clients
WHERE site_id = '<site>'
  AND cohort_date <= '2026-09-03'   -- user đã được tracking ít nhất 1 ngày trước window
```

Khi áp dụng mature filter, ta đảm bảo user đã "có cơ hội" được observe trong toàn bộ 28 ngày của window. Nếu không, user mới đến vào ngày 28 sẽ chỉ có 1 ngày để "nhìn thấy" — gây bias cho `active_days`, `days_since_last_visit`, v.v.

**Kết quả áp dụng:**
- 1games: ~400k raw → **32.701 mature** (giảm 92%)
- zapgames: ~600k raw → **58.511 mature** (giảm 90%)

### 1.2 Cohort tự nhiên (window ngắn hơn)

**Áp dụng cho:** 1000games (22 ngày)

1000games mới bắt đầu được tracking từ **2026-09-10** nên không có dữ liệu trước đó để áp dụng mature filter. Ta dùng toàn bộ user có page view trong 22 ngày.

**Kết quả:**
- 1000games: 64.127 raw → **52.608 unique** sau dedupe (giảm 18% do ClickHouse pagination overlap)

### 1.3 Ảnh hưởng

| Site | Window | Raw users | Mature/Deduped | Coverage |
|---|---:|---:|---:|---|
| 1games | 28d | ~400k | 32.701 | 8,2% |
| zapgames | 28d | ~600k | 58.511 | 9,7% |
| 1000games | 22d | 64.127 | 52.608 | 82% (không có mature filter) |

→ 1000games cohort **rộng hơn nhiều** so với 2 site còn lại vì thiếu lịch sử. Khi đọc phân khúc 1000games, cần lưu ý đây là "tất cả user trong 22 ngày", không chỉ "user trung thành".

---

## 2. Step 1 — User features (23-25 features)

**Mục tiêu:** Biến dữ liệu `gm_pages` (page view theo URL) thành vector đặc trưng cho mỗi user.

### 2.1 Nguồn dữ liệu: bảng `gm_pages`

Schema tóm tắt:

| Cột | Kiểu | Mô tả |
|---|---|---|
| `client_id` | string | ID ẩn danh của user (cookie-based) |
| `site_id` | string | Site (1games.io, zapgames.io, 1000games.io) |
| `shard_date` | date | Ngày session |
| `page_location` | string | URL đầy đủ |
| `page_views` | uint64 | Số page view trên location đó |
| `engagement_total_msec` | uint64 | Tổng thời gian engage (mili-giây) |
| `session_id` | string | ID session (group page view cùng visit) |

### 2.2 Quy trình trích xuất features

Pipeline gồm 3 sub-step:

```
Sub-step 1: User-level aggregates (gọi 1 SQL GROUP BY)
  ├─ total_pv, distinct_slugs, sessions, engaged_sessions,
  ├─ total_engaged_sec, active_days, first_date, last_date

Sub-step 2: Top slugs per user (gọi N SQL theo chunk)
  └─ top 20 (slug, pv) cho mỗi user (ClickHouse groupArray(20))

Sub-step 3: Local Python merge
  ├─ load games metadata (slug -> tags, genres)
  ├─ classify từng slug (home / category_browse / search / direct_game)
  └─ tính derived features (intent shares, tag entropy, dominant tag, …)
```

**Sub-step 1** aggregate trực tiếp từ ClickHouse — nhanh, nhưng giới hạn ở top-level (pv, sessions, dates).

**Sub-step 2** dùng `groupArray(20)` để lấy top 20 slug. Query:

```sql
SELECT
    client_id,
    arrayMap(x -> x.1, arr) AS slugs,
    arrayMap(x -> x.2, arr) AS slug_pvs
FROM (
    SELECT
        client_id,
        groupArray(20)((slug, slug_pv)) AS arr
    FROM (
        SELECT
            client_id,
            replaceOne(
                replaceOne(page_location, 'https://<site>/', ''),
                'http://<site>/', ''
            ) AS slug,
            sum(page_views) AS slug_pv
        FROM gm_pages
        WHERE site_id = '<site>'
          AND shard_date BETWEEN '...' AND '...'
          AND client_id IN (<chunk>)
        GROUP BY client_id, slug
        HAVING slug != ''
        ORDER BY slug_pv DESC
    )
    GROUP BY client_id
)
```

ClickHouse giới hạn trả về 5.000 rows / query, nên ta **chunk** theo `client_id` (mỗi chunk 5.000 ID). Mỗi chunk được lưu vào JSON ở `d:\GR\03_data\processed\user_features\<site>_chunks\chunk_XX_slugs.json` để debug và tái sử dụng.

**Sub-step 3** merge locally: với mỗi user, lặp qua 20 slug, phân loại intent, đếm tag/genre, tính tag_entropy.

### 2.3 Phân loại slug (intent classification)

Mỗi slug được phân thành 5 loại:

| Intent | Cách nhận biết | Vai trò |
|---|---|---|
| `home` | `slug == ''` (trang chủ) | Vào nhưng không click |
| `category_browse` | thuộc `HUB_SLUGS` (hot, recent, popular, v.v.) HOẶC bắt đầu bằng `games/`, `tag/`, `category/` | Duyệt category |
| `search` | bắt đầu bằng `search` (search?q=...) | Tìm kiếm |
| `direct_game` | match regex `^[a-z0-9]+(-[a-z0-9]+)+$` AND có trong catalog | Vào thẳng 1 game |
| `other` | còn lại (404, html, ...) | Không phân loại được |

**Hub slugs cố định theo site:**

| 1games | zapgames | 1000games |
|---|---|---|
| hot-games, recents, new, popular, trending, new-games, best-games, top-games | recent, hot, new, popular, top-rated, best, …, games/sports, games/action, … | recent, hot, new, trending, top, best, popular, search, games/popular-games, … |

**Quan trọng:** Mỗi site có URL pattern khác nhau, phải chỉnh lại hub slugs cho phù hợp.

### 2.4 Tính tag/genre (local join với catalog)

Với mỗi slug được phân loại `direct_game`, ta lookup trong file `*_all.csv` (catalog):

```python
slug_to_cats[slug]   # ['arcade', 'action']  -- có thể nhiều category
slug_to_tags[slug]   # ['Skill Games', 'Physics Games', ...]
slug_to_genre[slug]  # 'arcade'  -- thường 1 genre (nhưng 1000games thì comma-separated)
```

Cộng dồn PV của mỗi tag/genre/category → đếm được sở thích.

**Catalog lỗ hổng:** rất nhiều game mà user click vào (vd: `minecraft`, `fnaf-2`, `krillion-game`, `league-of-legends`, …) **không có trong catalog**. Những game này sẽ bị skip → giảm coverage tag/genre.

| Site | Catalog | Tỉ lệ coverage ước tính |
|---|---:|---:|
| 1games | 886 | ~52% (48% slug click thiếu metadata) |
| zapgames | 1.152 | ~95% (gần như đủ) |
| 1000games | 489 | ~40-50% (catalog nhỏ) |

### 2.5 Danh sách 25 features đầy đủ

| # | Feature | Ý nghĩa | Log-transform? |
|---:|---|---|---|
| 1 | `total_pv` | Tổng page view | ✓ |
| 2 | `distinct_games` | Số game khác nhau đã click | ✓ |
| 3 | `top_game_pv` | PV của game được click nhiều nhất | ✓ |
| 4 | `top_game_share` | Tỉ lệ PV của top game trên tổng | – |
| 5 | `sessions` | Số session | ✓ |
| 6 | `engaged_session_pct` | Tỉ lệ session có engagement >0 | – |
| 7 | `avg_session_sec` | Trung bình thời gian / engaged session | ✓ |
| 8 | `total_session_sec` | Tổng thời gian engage | ✓ |
| 9 | `active_days` | Số ngày active trong window | ✓ |
| 10 | `days_since_last_visit` | Số ngày từ lần visit cuối đến 2026-10-01 | ✓ |
| 11 | `sessions_last_7d`* | Số session trong 7 ngày gần nhất | ✓ |
| 12 | `sessions_last_14d`* | Số session trong 14 ngày gần nhất | ✓ |
| 13 | `home_pv` | PV trên home page | ✓ |
| 14 | `category_browse_pv` | PV trên category pages | ✓ |
| 15 | `search_pv` | PV trên search results | ✓ |
| 16 | `direct_game_pv` | PV trực tiếp vào game | ✓ |
| 17–20 | `*_share` | Tỉ lệ từng intent trên tổng PV | – |
| 21 | `tag_diversity` | Số tag khác nhau | ✓ |
| 22 | `tag_entropy` | Shannon entropy của phân phối tag (đa dạng sở thích) | – |
| 23 | `genre_diversity` / `distinct_genres` | Số genre khác nhau | ✓ |
| 24 | `dominant_tag_share` | Tỉ lệ của tag phổ biến nhất | – |
| 25 | `dominant_genre_share` | Tỉ lệ của genre phổ biến nhất | – |

*`sessions_last_7d` và `sessions_last_14d` chỉ có ở 1games/zapgames (cột 11, 12). 1000games không có vì query mới hơn.

**Cột 1000games dùng:** 23 features (bỏ 2 cột `sessions_last_7d`, `sessions_last_14d`).

### 2.6 Preprocessing

```python
# Null-safe
X = df[NUMERIC_FEATURES].fillna(0).replace([np.inf, -np.inf], 0).astype(float)

# Log-transform cho features heavy-tailed
for col in LOG_FEATURES:
    X[col] = np.log1p(np.maximum(X[col], 0))

# Standardize
scaler = StandardScaler()
X_std = scaler.fit_transform(X)
```

**Tại sao log1p?** Phân phối của `total_pv`, `sessions`, `active_days` heavy-tailed (trung bình thấp, một số user rất cao). Log1p nén range, giúp K-Means (dùng Euclidean distance) không bị kéo bởi outlier.

**Tại sao StandardScaler?** K-Means cần features cùng scale. Nếu không, feature lớn (vd: `total_pv` 0-1000) sẽ dominate feature nhỏ (vd: `engaged_session_pct` 0-1).

---

## 3. Step 2 — K-Means clustering

### 3.1 Thuật toán

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

km = KMeans(
    n_clusters=3,        # K=3 (chọn sau khi sweep)
    n_init=10,           # chạy 10 lần với centroid init khác nhau, lấy inertia thấp nhất
    random_state=42,     # reproducible
    max_iter=300,
)
labels = km.fit_predict(X_std)
```

`n_init=10` rất quan trọng: K-Means nhạy với initialization (k-means++), chạy 10 lần giảm variance. `random_state=42` cố định để kết quả reproducible.

### 3.2 Chọn K bằng silhouette

Trước khi chọn K=3, ta sweep K ∈ {2, 3, 4, 5} và tính silhouette score:

```python
for k in K_RANGE:
    km = KMeans(n_clusters=k, n_init=10, random_state=42, max_iter=300)
    labels = km.fit_predict(X_std)
    sil = silhouette_score(X_std[sample_idx], labels[sample_idx])
```

**Silhouette score** đo "trung bình khoảng cách từ 1 điểm đến các điểm cùng cụm" so với "khoảng cách đến cụm gần nhất". Range [-1, 1], càng cao càng tách biệt.

**Tại sao sample?** Tính silhouette trên toàn bộ 32k-58k user quá chậm. Ta sample 3.000 user ngẫu nhiên (random seed=42) — đủ đại diện.

**Kết quả silhouette 3 site:**

| Site | K=2 | K=3 | K=4 | K=5 | Chọn |
|---|---:|---:|---:|---:|---:|
| 1games | 0,29 | **0,30** | 0,27 | 0,26 | K=3 |
| zapgames | 0,18 | **0,19** | 0,17 | 0,18 | K=3 |
| 1000games | 0,28 | 0,26 | 0,27 | 0,28 | **K=3** (vì lý do business) |

→ **Lưu ý:** ở 1000games, K=2 có silhouette cao nhất (0,28), nhưng ta vẫn chọn K=3 để **đồng nhất phương pháp với 2 site khác** và cho phép so sánh 3 phân khúc. Lý do business: 3 phân khúc (Power / Casual / Bounce) phù hợp với hành vi người dùng 1000games hơn 2 phân khúc.

### 3.3 Dedupe trước khi cluster (1 bài học quan trọng)

Vấn đề phát hiện: 1000games pagination với `LIMIT 5000 OFFSET N` trả về **overlap rows** do ClickHouse không đảm bảo total ordering khi nhiều user có cùng `total_pv`. Hệ quả: 64.127 raw rows nhưng chỉ 52.608 unique `client_id`.

**Fix:** Trước khi cluster, drop_duplicates(subset='client_id', keep='first'). Code:

```python
feat = pd.read_csv(CSV_IN, dtype={'client_id': str}, low_memory=False)
feat = feat.drop_duplicates(subset='client_id', keep='first')  # 64127 → 52608
```

**Tại sao `keep='first'`?** Vì mỗi user chỉ có 1 bản ghi duy nhất trong ClickHouse — khi pagination overlap, các bản ghi trùng nhau thực sự giống nhau (cùng `client_id`, cùng `total_pv` vì cùng GROUP BY).

### 3.4 Labeling 3 cụm

Sau khi cluster, ta **không** dùng `km.cluster_centers_` để label trực tiếp. Thay vào đó, ta nhìn vào **mean feature values** để gán nhãn bằng tay:

| Cụm (K=3) | Label | Đặc điểm phân biệt |
|---|---|---|
| C0 | **Power user (Lõi trung thành)** | distinct_games cao (~9-10), active_days cao, tag_diversity cao, top_game_share thấp |
| C1 | **Bounce (Vào rồi thoát)** | distinct_games thấp (~1-2), active_days thấp, top_game_share thấp, nhiều 0-game users |
| C2 | **Casual (Trung thành 1-3 game)** | distinct_games trung bình (~2-3), top_game_share cao (~50%), tag_diversity trung bình |

→ **Không bao giờ** gán nhãn tự động — luôn kiểm tra bằng feature means + vài sample user để hiểu hành vi thực tế.

### 3.5 Output

`clusters_<site>_<date>.csv` = features CSV + 1 cột `cluster_id` (0, 1, hoặc 2).

---

## 4. Step 3 — Per-cluster game/tag/genre insights

**Mục tiêu:** Với mỗi cụm, tóm tắt user thích game/tag/genre gì.

### 4.1 Hai nguồn dữ liệu

| Nguồn | Cấu trúc | Dùng để |
|---|---|---|
| `clusters_<site>_<date>.csv` | 1 dòng / user, có `top_game_slug`, `dominant_tag`, `dominant_genre` | Đếm "anchor game" — game user chọn làm yêu thích |
| `<site>_chunks/chunk_XX_slugs.json` | top 20 (slug, pv) của từng user | Tính top game/tag/genre theo PV & user count |

**Lý do cần 2 nguồn:**
- `top_game_slug` cho ta biết "game yêu thích" của user (PV cao nhất trong top 20) → 1 user chỉ có 1 top_game.
- Chunk data cho ta biết user đã chơi những game nào → 1 user có thể đóng góp vào nhiều game.

### 4.2 Top game theo PV vs theo user

Hai metric khác nhau và cả hai đều quan trọng:

| Metric | Công thức | Ý nghĩa | Use case |
|---|---|---|---|
| **PV (page view)** | Tổng PV của tất cả user trong cụm trên 1 game | Game được chơi **nhiều lần** (engagement) | Xếp hạng "game gây nghiện" |
| **User count** | Số distinct user trong cụm đã chơi 1 game | Game có **nhiều user** (reach) | Xếp hạng "game phổ biến" |

**Ví dụ 1000games C0:**
- `slope-2` PV=8.818, user=4.249 → PV/user=2,1 → user chơi nhiều lần
- `survival-race` PV=6.981, user=4.408 → PV/user=1,6 → user chơi trung bình 1-2 lần
- `krillion-game` PV=19, user=18 → PV/user=1,1 → user chơi 1 lần

### 4.3 Top tag/genre: tương tự

- **Tag PV** = tổng PV của tất cả game có tag đó
- **Tag user** = số user đã chơi ít nhất 1 game có tag đó (1 user có thể count vào nhiều tag)

**Tại sao tách user và PV?** Một user chơi 5 game có cùng tag → vẫn chỉ count 1 cho user. Ngược lại, 5 game × 3 PV = 15 PV. Tag nào có PV cao mà user thấp = game của tag đó rất addictive.

### 4.4 Distinct games bucket

Đếm số user trong cụm theo "đã chơi bao nhiêu game trong top 20":

| Bucket | Ý nghĩa |
|---|---|
| `0 game` | User không click game nào trong catalog |
| `1 game` | Click đúng 1 game |
| `2-3 game` | Click 2-3 game |
| `4-7 game` | Click 4-7 game |
| `8+ game` | Click 8+ game (power user thật sự) |

→ Phân khúc nào càng nhiều user ở bucket `8+` → càng "trung thành đa dạng".

### 4.5 NaN filtering

Một số user chỉ click vào game **không có trong catalog** (vd: `minecraft`, `fnaf-2`). Họ có `top_game_slug` nhưng:
- `top_game_slug` không NaN (vì họ có top game)
- Nhưng khi lookup tag/genre, ta skip → `dominant_tag` = NaN

Khi ghi CSV/JSON, **filter NaN** trước khi ghi. Code:

```python
def save_csv(counter, path):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['key', 'count'])
        for k, v in counter.most_common(20):
            if pd.notna(k) and k != '':  # <-- filter
                w.writerow([k, v])
```

### 4.6 Output files

Với mỗi site:
```
insights_<site>_tags/
├── summary.json                              # tổng hợp tất cả cụm
├── cluster0/
│   ├── top_games_by_pv.csv
│   ├── top_games_by_users.csv
│   ├── top_game_count.csv                    # "anchor game"
│   ├── top_tags_by_pv.csv
│   ├── top_tags_by_users.csv
│   ├── top_tag_count.csv
│   ├── top_genres_by_pv.csv
│   ├── top_genres_by_users.csv
│   ├── top_genre_count.csv
│   └── distinct_games_buckets.csv
├── cluster1/  (cùng cấu trúc)
└── cluster2/  (cùng cấu trúc)
```

Mỗi cluster có **10 file CSV** + 1 `summary.json` = 31 file / site.

---

## 5. Step 4 — Báo cáo tiếng Việt

Mỗi site có 2 báo cáo:

### 5.1 `insights_user_segments_<site>_VI.md` — Hành vi + Phân khúc

**Cấu trúc:**

1. **Tổng quan hành vi người dùng** — 4 phần nhỏ:
   - Hành vi chung (trung vị PV, sessions, active_days, distinct_games)
   - Phân bổ số game đã chơi (1 bảng 5 bucket)
   - Phân bổ theo intent (1 bảng 4 intent)
   - Top 5 game toàn site (1 bảng ngắn)

2. **Phân khúc 3 cụm K-Means** — 1 bảng tổng + 3 phần nhỏ (1 / cụm):
   - Số user, % mature
   - Hành vi đặc trưng
   - Phân bổ số game (1 bảng 5 bucket / cụm)
   - "Câu chuyện" 1-2 dòng

3. **Câu hỏi mở cho team** — 3-5 câu hỏi business cần data team / content team trả lời.

### 5.2 `insights_games_tags_<site>_VI.md` — Game/Tag/Genre insights

**Cấu trúc:**

1. **Cách đọc báo cáo** — giải thích 4 intent, tại sao catalog lỗ hổng, …
2. **3 phần lớn (1 / cụm)** — mỗi phần có:
   - Số user + coverage (số user có top_slugs data)
   - Phân bổ số game (1 bảng)
   - Top 10 game theo PV (1 bảng)
   - Top 10 game theo user count (1 bảng)
   - Top 10-15 game "anchor" (top_game_slug) (1 bảng)
   - Top 15 tag theo PV + theo user (1 bảng 2 cột)
   - Top genre theo PV + theo user (1 bảng 2 cột)
   - "Câu chuyện của phân khúc" — 1-2 đoạn
   - "Hệ quả chiến lược" — 2-4 bullet gợi ý hành động
3. **So sánh nhanh 3 phân khúc** (trong cùng site) — 1 bảng
4. **Phát hiện quan trọng** — vd: lỗ hổng metadata, anchor game, …
5. **Câu hỏi mở** — 5 câu cho team
6. **Tìm dữ liệu ở đâu** — bảng file paths

### 5.3 Quy tắc viết

- **Số liệu phải chính xác** — lấy từ CSV/JSON, không suy luận
- **Câu chuyện ngắn gọn** — tối đa 2-3 dòng / phân khúc
- **Hệ quả chiến lược = actionable** — "Test A/B widget X" chứ không phải "Cần cải thiện"
- **Câu hỏi mở phải có data team trả lời được** — "Tại sao 38% Bounce?" (cần log analysis) thay vì "Cần làm gì để tăng engagement" (quá mơ hồ)

---

## 6. Pipeline scripts (tham khảo)

### 6.1 1games / zapgames (mature filter, 28d)

| Bước | Script | Output |
|---|---|---|
| Step 1a (user aggregates) | `User Segmentation/scripts/<site>_query_batch.py` | chunks ở `03_data/processed/user_features/chunks/` |
| Step 1b (top slugs) | `User Segmentation/scripts/<site>_query_batch.py` | chunks `chunk_XX_pv.json` |
| Step 1c (merge features) | `User Segmentation/scripts/merge_features.py` | `user_features_<site>_2026-10-01.csv` |
| Step 2 (clustering) | `User Segmentation/scripts/cluster_users.py` | `clusters_<site>_2026-10-01.csv` + `cluster_report.md` |
| Step 3 (insights) | `User Segmentation/scripts/build_game_tag_insights.py` | `insights_<site>_tags/cluster0..2/*.csv` + `summary.json` |

### 6.2 1000games (no mature filter, 22d)

| Bước | Script | Output |
|---|---|---|
| Step 1 (combined: aggregates + top slugs) | `1000games_step1_features.py` | `user_features_1000games_2026-10-01.csv` + `1000games_chunks/chunk_XX_slugs.json` |
| Step 2 (clustering + dedupe) | inline trong `1000games_step3_insights.py` (cũng có `1000games_step2b_recluster.py` riêng) | `clusters_1000games_2026-10-01.csv` |
| Step 3 (insights) | `1000games_step3_insights.py` | `insights_1000games_tags/cluster0..2/*.csv` + `summary.json` |

### 6.3 Helper

| Tool | Mô tả |
|---|---|
| `gma_client.py` | Wrapper MCP để gọi `run_query` ClickHouse |
| `gma_oauth.py` | OAuth flow cho Google Meridian Analytics |
| `User Segmentation/scripts/inspect_chunks.py` | Debug: in summary 1 chunk |
| `User Segmentation/scripts/explore_clusters.py` | Debug: phân tích 1 cluster sâu |

---

## 7. Bài học kinh nghiệm (lessons learned)

### 7.1 URL pattern khác nhau giữa các site

Mỗi site có URL structure riêng:

| Site | Pattern | Extract |
|---|---|---|
| 1games | `https://1games.io/games/slope-2` | `extract(page_location, '/games/([a-z0-9-]+)')` |
| zapgames | `https://zapgames.io/play/slope-2.html` | `extract(page_location, '/play/([a-z0-9-]+)')` |
| 1000games | `https://1000games.io/slope-2` | `replaceOne(page_location, 'https://1000games.io/', '')` |

**Fix:** Mỗi site cần `classify_slug()` và `HUB_SLUGS` riêng. Không thể dùng chung.

### 7.2 ClickHouse pagination overlap

Dùng `LIMIT N OFFSET M` không đảm bảo total ordering khi `total_pv` của nhiều user bằng nhau. Hệ quả: rows overlap giữa các chunk → duplicate `client_id`.

**Fix:** Dedupe sau khi load (drop_duplicates subset='client_id', keep='first').

### 7.3 Tag format không đồng nhất giữa các site

| Site | Format | Ví dụ |
|---|---|---|
| 1games | lowercase | `skill`, `physics` |
| zapgames | Capitalized, không " Games" | `Skill`, `Physics` |
| 1000games | "Capitalized" + " Games" | `Skill Games`, `Physics Games` |

**Fix:** Khi phân tích tag cho 1000games, tag thường có suffix " Games" — chấp nhận và không strip. Khi so sánh giữa 3 site, cần normalize trước.

### 7.4 Catalog không phủ hết game user click

Đặc biệt ở 1000games: 489 catalog, ~50% user click vào game không có metadata. Những user đó:
- Có `top_game_slug` (vì họ có game được click nhiều nhất)
- Nhưng `distinct_games` thấp hơn thực tế (vì ta skip slug không có metadata)
- `dominant_tag` = NaN

**Fix:** Tăng coverage bằng cách bổ sung metadata cho top game thiếu (ngoài phạm vi báo cáo).

### 7.5 top_slugs giới hạn 20

`groupArray(20)` chỉ lấy top 20 slug. User Lõi trung thành có thể đã click 50+ slug khác nhau → ta chỉ thấy "20 phổ biến nhất". Mất thông tin về niche game.

**Trade-off:** Tăng N (vd: 50) sẽ tăng memory ClickHouse và thời gian query. Hiện tại 20 là đủ cho 80-90% phân tích.

### 7.6 NaN propagation trong pandas operations

Một số operation (như `max(tag_counts.items(), key=lambda x: x[1])`) trả về NaN nếu dict rỗng. Khi ghi CSV, NaN trở thành chuỗi rỗng. Khi đọc lại, phải filter cả NaN lẫn chuỗi rỗng.

**Fix:** Dùng `if pd.notna(k) and k != ''` ở mọi nơi filter.

### 7.7 K=2 silhouette cao hơn K=3 ở 1000games

Về mặt toán học, K=2 tốt hơn. Nhưng về business, K=3 cho phân khúc "Bounce" tách bạch hơn và cho insight rõ hơn. Trade-off: chọn K theo use case, không chỉ theo metric.

**Lưu ý:** Khi chọn K ≠ K tối ưu silhouette, cần giải thích lý do business trong báo cáo.

---

## 8. Validation & quality checks

### 8.1 K-Means quality

```python
from sklearn.metrics import silhouette_score
sil = silhouette_score(X_std[sample_idx], labels[sample_idx])
# Range [-1, 1]; > 0.2 là tạm ổn, > 0.4 là tốt, > 0.5 là rất tốt
```

3 site đều có silhouette 0.19-0.30 — tạm ổn cho hành vi người dùng (vốn phức tạp, không có cluster "tự nhiên" rõ ràng).

### 8.2 Cluster size sanity check

Mỗi cluster nên có ≥ 5% tổng user. Nếu cluster nào < 5% → có thể là noise.

| Site | C0 | C1 | C2 | Tổng |
|---|---:|---:|---:|---:|
| 1games | 35% (11.491) | 22% (7.158) | 43% (14.052) | 32.701 |
| zapgames | 0% (?) | 29% (17.098) | 71% (41.413)* | 58.511 |
| 1000games | 26% (13.723) | 38% (20.042) | 36% (18.843) | 52.608 |

*zapgames có 1 cluster rất lớn (~71%) do silhouette thấp (0.19) — K-Means khó tách các nhóm nhỏ hơn.

### 8.3 Feature sanity

Trước khi cluster, kiểm tra:

```python
print(df[NUMERIC_FEATURES].describe())
print(df[NUMERIC_FEATURES].isna().sum())  # NaN count
print(np.isinf(X).sum())  # inf count
```

Mọi giá trị phải finite và trong range hợp lý (vd: `engaged_session_pct` ∈ [0, 1]).

### 8.4 Top game sanity check

Với mỗi cluster, top 5 game nên là game **phổ biến toàn site** (kiểm tra bằng cách so với top 10 toàn site). Nếu cluster có game "lạ" ở top → có thể là noise, cần điều tra.

### 8.5 Reproducibility

- `random_state=42` ở KMeans + sample → cùng kết quả mỗi lần chạy
- Chunk data lưu JSON → có thể re-run Step 3 mà không cần re-query ClickHouse
- Scripts idempotent: chạy lại cho cùng output

---

## 9. Cách reproduce (cho data team khác)

### 9.1 Yêu cầu

- Python 3.10+
- `pandas`, `numpy`, `scikit-learn`, `scipy`
- ClickHouse access qua `gma_client.call_mcp`
- Catalog CSV ở `d:\GR\<site>_all.csv`

### 9.2 Thứ tự chạy

**1games / zapgames:**
```bash
cd "d:\GR"
python "User Segmentation/scripts/zapgames_query_batch.py"  # tạo chunks
python "User Segmentation/scripts/merge_features.py"          # merge → features CSV
python "User Segmentation/scripts/cluster_users.py"           # cluster
python "User Segmentation/scripts/build_game_tag_insights.py" # insights
# Sau đó viết báo cáo .md thủ công
```

**1000games:**
```bash
cd "d:\GR"
python 1000games_step1_features.py  # features + chunks
python 1000games_step3_insights.py # cluster + insights (combined)
# Sau đó viết báo cáo .md thủ công
```

### 9.3 Tham số cần chỉnh khi áp dụng site mới

1. **URL pattern** trong `classify_slug` — phải khớp với cấu trúc URL site mới
2. **HUB_SLUGS** — tên các category/tag page của site
3. **DATE_START / DATE_END** — cửa sổ thời gian
4. **Mature filter** — chỉ áp dụng nếu site có ≥ 2x window lịch sử
5. **Catalog CSV** — schema có thể khác (category / tags / genre); cần chỉnh loader

---

## 10. Tóm tắt

| Bước | Input | Tool chính | Output | Quyết định thiết kế chính |
|---|---|---|---|---|
| 1. Features | ClickHouse `gm_pages` | Python + ClickHouse SQL | CSV 25 cột | log1p + StandardScaler |
| 2. Clustering | features CSV | sklearn KMeans | CSV + cluster_id | K=3 (business > silhouette) |
| 3. Insights | clusters + chunks + catalog | Python + Counter | 30 CSV + summary.json | 2 metric: PV & user count |
| 4. Report | tất cả output trên | (manual) | 2 file .md / site | tiếng Việt, actionable |

**3 site đã áp dụng:**
- 1games.io: 32.701 mature users, K=3, silhouette 0.30
- zapgames.io: 58.511 mature users, K=3, silhouette 0.19
- 1000games.io: 52.608 users, K=3, silhouette 0.26

**Output mỗi site:**
- `user_features_<site>_2026-10-01.csv`
- `clusters_<site>_2026-10-01.csv`
- `insights_<site>_tags/cluster0..2/*.csv` (30 file)
- `insights_<site>_tags/summary.json`
- `insights_user_segments_<site>_VI.md` (báo cáo hành vi + phân khúc)
- `insights_games_tags_<site>_VI.md` (báo cáo game/tag/genre)

---

**Tác giả:** Game analytics
**Ngày tạo:** 2026-10-09
**Phiên bản:** 4.0
**Áp dụng cho:** 1games.io, zapgames.io, 1000games.io (window 2026-09-03 → 2026-10-01)
