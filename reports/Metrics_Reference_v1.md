# Metrics Reference — Detailed Definitions

**Version:** 1.0
**Date:** October 9, 2026
**Companion to:** `Methodology_v4_User_Segmentation_and_Game_Tag_Insights.md`
**Scope:** Detailed definition, formula, source, and use case for every metric that appears in:
- `insights_user_segments_<site>_VI.md` (báo cáo hành vi + phân khúc)
- `insights_games_tags_<site>_VI.md` (báo cáo game/tag/genre)
- `user_features_<site>_2026-10-01.csv` (raw features)
- `clusters_<site>_2026-10-01.csv` (features + cluster_id)
- `insights_<site>_tags/cluster<N>/*.csv` (per-cluster insights)

**Notation:**
- **Nguồn DB** = bảng ClickHouse
- **Nguồn local** = tính trong Python từ chunk data
- **Công thức** = cách tính
- **Phạm vi** = 1 user / 1 cluster / 1 site
- **Ý nghĩa** = metric này nói lên điều gì

---

## 0. Tổng quan 3 nhóm metric

Pipeline có 3 nhóm metric:

```
┌──────────────────────────────────────────────────────────────────────┐
│  Nhóm 1: USER-LEVEL FEATURES (25 features)                           │
│  - Tính cho TỪNG USER                                                 │
│  - Đầu vào: ClickHouse gm_pages + Python local                       │
│  - Đầu ra: user_features_<site>_<date>.csv                           │
│  - Mục đích: input cho K-Means clustering                            │
└──────────────────────────────────────────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────────┐
│  Nhóm 2: SITE-LEVEL SUMMARY STATS (trong báo cáo)                    │
│  - Tính trên TOÀN BỘ USER (aggregate)                                │
│  - Ví dụ: "Trung vị PV = 4", "User chơi ≥1 game = 96%"              │
│  - Mục đích: mô tả tổng quan behavior của site                       │
└──────────────────────────────────────────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────────┐
│  Nhóm 3: CLUSTER-LEVEL INSIGHTS (sau clustering)                     │
│  - Tính TRONG 1 CLUSTER                                               │
│  - Ví dụ: "Top 10 game theo PV", "Tag diversity"                     │
│  - Mục đích: hiểu sở thích từng phân khúc                            │
└──────────────────────────────────────────────────────────────────────┘
```

Tài liệu này giải thích chi tiết từng metric trong 3 nhóm.

---

# PHẦN A — USER-LEVEL FEATURES (25 features)

Đây là 25 cột trong file `user_features_<site>_<date>.csv`. Mỗi dòng là 1 user.

## A.1 Activity volume (khối lượng hoạt động)

### 1. `total_pv` — Tổng page view

| | |
|---|---|
| **Nguồn** | ClickHouse `gm_pages.page_views` (sum) |
| **Công thức** | `SUM(page_views) WHERE client_id = X AND shard_date BETWEEN ...` |
| **Ý nghĩa** | User X đã xem bao nhiêu page trong window |
| **Range** | 1 → 100.000+ (heavy-tailed, log-transform khi cluster) |
| **Use case** | Đo "mức độ hoạt động" tổng thể |

**Lưu ý:** Nếu user có > 20 slug khác nhau, `total_pv` ở đây **chỉ tính tổng PV của top 20 slug** (do `groupArray(20)` của ClickHouse). User Lõi trung thành có thể `total_pv` thấp hơn thực tế. Với 1games, có 2 phiên bản:

- `user_features_1games_2026-10-01.csv` (cũ): dùng `top_slugs` sum
- `user_features_1games_2026-10-01.csv` (mới): dùng `sum(page_views)` toàn user

Trong pipeline hiện tại (`1000games_step1_features.py` và `merge_features.py`), `total_pv` = sum của top 20 slug → **lower bound**.

### 2. `distinct_slugs` — Số URL khác nhau

| | |
|---|---|
| **Nguồn** | ClickHouse `uniqExact(page_location)` |
| **Công thức** | Đếm số `page_location` unique mà user đã xem |
| **Ý nghĩa** | User "rộng" hay "sâu" trong exploration |
| **Range** | 1 → 500+ |
| **Use case** | Kết hợp với `distinct_games` để biết user duyệt category nhiều hay vào thẳng game |

**Lưu ý:** Bao gồm cả home page, category page, search page, game page. Khác với `distinct_games` (chỉ đếm game).

### 3. `distinct_games` — Số game khác nhau

| | |
|---|---|
| **Nguồn** | Local (từ `top_slugs` join với `slug_to_cats`) |
| **Công thức** | `COUNT(DISTINCT slug) WHERE slug ∈ direct_game AND slug ∈ catalog` |
| **Ý nghĩa** | User đã chơi bao nhiêu game thật sự |
| **Range** | 0 → 20 (giới hạn bởi top_slugs) |
| **Use case** | Phân biệt Power user (nhiều game) vs Bounce (1 game) |

**Quan trọng:** Có 2 "lower bound" chồng lên nhau:
1. `groupArray(20)` chỉ lấy top 20 slug → user chơi 30 game thì ta chỉ thấy 20
2. Catalog không phủ hết → user chơi `minecraft` (không có trong catalog) thì không đếm

→ `distinct_games` là **ước lượng dưới**, đặc biệt cho Power user và game thiếu metadata.

### 4. `top_game_slug` — Game được click nhiều nhất

| | |
|---|---|
| **Nguồn** | Local (max trong `top_slugs` theo `slug_pv`) |
| **Công thức** | `slug WITH MAX(slug_pv) AND slug ∈ direct_game` |
| **Ý nghĩa** | "Game yêu thích" của user (theo page view) |
| **Range** | Slug string (vd: `slope-2`) hoặc `''` nếu không có direct_game |
| **Use case** | Tìm "anchor game" — game mà user quay lại nhiều lần nhất |

### 5. `top_game_pv` — Page view của top game

| | |
|---|---|
| **Nguồn** | Local |
| **Công thức** | `MAX(slug_pv) WHERE slug ∈ direct_game` |
| **Ý nghĩa** | User dành bao nhiêu PV cho game yêu thích |
| **Range** | 0 → 100+ |
| **Use case** | Đo "độ sâu" của preference (nhiều PV = user really likes this game) |

### 6. `top_game_share` — Tỉ lệ top game / tổng PV

| | |
|---|---|
| **Nguồn** | Local |
| **Công thức** | `top_game_pv / total_pv` |
| **Ý nghĩa** | User "trung thành 1 game" hay "đa dạng" |
| **Range** | 0.0 → 1.0 |
| **Use case** | Cao (>0.5) = anchor game, thấp (<0.2) = explorer |

**Cách đọc:**
- `top_game_share = 0.8` → 80% PV của user là 1 game duy nhất → anchor
- `top_game_share = 0.1` → user chơi nhiều game, không game nào dominant

## A.2 Session metrics (phiên truy cập)

### 7. `sessions` — Tổng số session

| | |
|---|---|
| **Nguồn** | ClickHouse `count(DISTINCT session_id)` |
| **Công thức** | `uniq(session_id) WHERE client_id = X` |
| **Ý nghĩa** | User quay lại site bao nhiêu lần |
| **Range** | 1 → 100+ |
| **Use case** | Phân biệt "vào 1 lần rồi thôi" vs "quay lại hàng ngày" |

**Lưu ý:** Đếm theo `session_id` chứ không phải theo `shard_date`. Một ngày có thể có nhiều session (sáng 1 cái, chiều 1 cái, tối 1 cái).

### 8. `engaged_sessions` — Số session có engagement

| | |
|---|---|
| **Nguồn** | ClickHouse `countIf(engagement_total_msec > 0)` |
| **Công thức** | Đếm session có tổng thời gian engage > 0 |
| **Ý nghĩa** | User có "tương tác thật" trong bao nhiêu session |
| **Range** | 0 → sessions |
| **Use case** | Đo chất lượng session (không phải lúc nào vào cũng chơi) |

### 9. `engaged_session_pct` — Tỉ lệ session có engagement

| | |
|---|---|
| **Nguồn** | Local |
| **Công thức** | `engaged_sessions / sessions` |
| **Ý nghĩa** | Có bao nhiêu % session user thật sự chơi (không phải chỉ mở rồi đóng) |
| **Range** | 0.0 → 1.0 |
| **Use case** | Phân biệt "bounce" (vào không chơi) vs "active" (vào là chơi) |

**Cách đọc:**
- `engaged_session_pct = 0.1` → 90% session user chỉ mở, không tương tác → rất nông
- `engaged_session_pct = 0.9` → hầu hết session user đều chơi game thật

### 10. `avg_session_sec` — Trung bình giây / engaged session

| | |
|---|---|
| **Nguồn** | Local |
| **Công thức** | `total_engaged_sec / engaged_sessions` |
| **Ý nghĩa** | Session "chơi thật" trung bình dài bao nhiêu |
| **Range** | 0 → 3600+ (giây) |
| **Use case** | Đo "độ sâu" mỗi lần chơi |

### 11. `total_session_sec` — Tổng thời gian engage

| | |
|---|---|
| **Nguồn** | ClickHouse `sum(engagement_total_msec) / 1000` |
| **Công thức** | Tổng tất cả `engagement_total_msec` của user, đổi sang giây |
| **Ý nghĩa** | Tổng thời gian user dành cho site trong window |
| **Range** | 0 → 100.000+ |
| **Use case** | Đo "tổng đầu tư" của user vào site |

### 12. `active_days` — Số ngày active

| | |
|---|---|
| **Nguồn** | ClickHouse `uniqExact(shard_date)` |
| **Công thức** | Đếm số `shard_date` unique mà user có page view |
| **Ý nghĩa** | User active bao nhiêu ngày trong window |
| **Range** | 1 → window_length (28 cho 1games/zapgames, 22 cho 1000games) |
| **Use case** | Phân biệt "quay lại hàng ngày" vs "chỉ vào 1-2 lần" |

**Quan trọng:** Window 28 ngày. User "mature" có thể active 28/28 ngày. User "Bounce" thường active 1/28.

### 13. `days_since_last_visit` (dslv) — Ngày từ lần cuối đến 2026-10-01

| | |
|---|---|
| **Nguồn** | Local |
| **Công thức** | `(2026-10-01 - MAX(shard_date)).days` |
| **Ý nghĩa** | User "lâu rồi không thấy quay lại" |
| **Range** | 0 → 30 (sentinel: 30 = window length) |
| **Use case** | Phân biệt "recent active" (dslv=0-2) vs "churned" (dslv=21+) |

**Quy ước sentinel:**
- `dslv = 30` → user không có observation trong window (lạ) — coi như "churned"
- `dslv = -1` → không có session record (lỗi) — được replace bằng 30

### 14. `sessions_last_7d` — Session trong 7 ngày gần nhất

| | |
|---|---|
| **Nguồn** | ClickHouse `countIf(shard_date > window_end - 7)` |
| **Công thức** | Đếm session có `shard_date` ∈ (2026-09-25, 2026-10-01] |
| **Ý nghĩa** | Hoạt động gần đây (recency) |
| **Range** | 0 → 50+ |
| **Use case** | Phân biệt "vẫn active" vs "đã bỏ" |

**Chỉ có ở 1games/zapgames.** 1000games không có vì query mới hơn (chưa thêm vào pipeline).

### 15. `sessions_last_14d` — Session trong 14 ngày gần nhất

| | |
|---|---|
| **Nguồn** | ClickHouse `countIf(shard_date > window_end - 14)` |
| **Công thức** | Tương tự `sessions_last_7d` nhưng 14 ngày |
| **Ý nghĩa** | Hoạt động gần đây 2 tuần |
| **Range** | 0 → 100+ |

## A.3 Intent metrics (phân loại page)

### 16-19. `home_pv` / `category_browse_pv` / `search_pv` / `direct_game_pv`

| | |
|---|---|
| **Nguồn** | Local (sum `slug_pv` theo `classify_slug()`) |
| **Công thức** | `SUM(slug_pv) WHERE classify_slug(slug) = X` |
| **Ý nghĩa** | User dành bao nhiêu PV cho mỗi loại page |
| **Range** | 0 → 100+ |

**4 intent:**

| Intent | `classify_slug()` | User làm gì |
|---|---|---|
| `home` | `slug == ''` | Vào homepage, không click |
| `category_browse` | thuộc HUB_SLUGS hoặc `games/`, `tag/`, `category/` | Duyệt category page |
| `search` | bắt đầu bằng `search` | Tìm kiếm game |
| `direct_game` | match `^[a-z0-9]+(-[a-z0-9]+)+$` AND có trong catalog | Click thẳng 1 game |

### 20-23. `*_share` — Tỉ lệ từng intent trên tổng PV

| | |
|---|---|
| **Nguồn** | Local |
| **Công thức** | `intent_pv / total_pv` (cho mỗi intent) |
| **Ý nghĩa** | User "vào kiểu gì" — tỉ lệ thời gian dành cho mỗi intent |
| **Range** | 0.0 → 1.0, tổng 4 share = 1.0 |
| **Use case** | Phân biệt site "portal" (nhiều category_browse) vs site "play" (nhiều direct_game) |

**Ví dụ 1000games C0 (Lõi trung thành):**
- `direct_game_share = 0.85` → 85% PV là click thẳng vào game → "play site"
- `home_share = 0.05` → ít khi chỉ vào home
- `search_share = 0.02` → ít search

## A.4 Tag/Genre metrics (sở thích)

### 24. `tag_diversity` — Số tag khác nhau

| | |
|---|---|
| **Nguồn** | Local (từ `top_slugs` join với `slug_to_tags`) |
| **Công thức** | `COUNT(DISTINCT tag) WHERE slug ∈ direct_game` |
| **Ý nghĩa** | User chơi bao nhiêu dòng game khác nhau (skill, action, sports, …) |
| **Range** | 0 → 100+ |
| **Use case** | Phân biệt "đa dạng" (nhiều tag) vs "1 niche" (1-2 tag) |

**Lower bound:** Giống `distinct_games` — chỉ đếm từ top 20 slug, skip game không có metadata.

### 25. `tag_entropy` — Shannon entropy của phân phối tag

| | |
|---|---|
| **Nguồn** | Local |
| **Công thức** | `H = -Σ (p_i × log2(p_i))` với `p_i = tag_pv_i / total_tag_pv` |
| **Ý nghĩa** | Đo "độ phân tán" của sở thích — entropy cao = sở thích đa dạng đều, entropy thấp = sở thích tập trung 1-2 tag |
| **Range** | 0 → log2(N) với N = số tag unique. Thường 0 → 5 |
| **Use case** | Phân biệt "balanced explorer" vs "niche player" |

**Cách đọc:**
- `tag_entropy = 0` → user chỉ chơi 1 tag duy nhất
- `tag_entropy = 1` → user chơi 2 tag với tỉ lệ 50/50 (entropy 1 bit)
- `tag_entropy = 4` → user chơi ~16 tag đều nhau (entropy 4 bit)

**Công thức chi tiết:**

```python
# total_tag_pv = tổng PV của tất cả tag user chơi
# tag_counts = {tag_1: pv_1, tag_2: pv_2, ...}
H = 0
for tag, pv in tag_counts.items():
    p = pv / total_tag_pv
    H -= p * math.log2(p)
```

### 26. `genre_diversity` (hoặc `distinct_genres`) — Số genre khác nhau

| | |
|---|---|
| **Nguồn** | Local |
| **Công thức** | `COUNT(DISTINCT genre)` tương tự `tag_diversity` |
| **Ý nghĩa** | User chơi bao nhiêu thể loại lớn (action, sports, …) |
| **Range** | 0 → 10+ |
| **Use case** | Tương tự `tag_diversity` nhưng ở mức "lớn hơn" |

**Lưu ý:** `genre` thường 1 giá trị / game (vd: `action`), còn `category` có thể nhiều (vd: `arcade, action, multiplayer`). 1000games catalog dùng `category` thay vì `genre` (đặc thù catalog).

### 27. `dominant_tag` / `dominant_tag_pv` / `dominant_tag_share`

| | |
|---|---|
| **Nguồn** | Local |
| **Công thức** | `argmax(tag_counts.items(), key=lambda x: x[1])` |
| **Ý nghĩa** | Tag được chơi nhiều nhất (top 1) của user |
| **Range** | string / int / float ∈ [0, 1] |
| **Use case** | Tìm "sở thích chính" của user |

**`dominant_tag_share` cao (>0.5)** = user "rất thích" 1 tag → dễ retention với tag đó
**`dominant_tag_share` thấp (<0.3)** = user "đa dạng" → khó retention, cần variety

### 28. `dominant_genre` / `dominant_genre_pv` / `dominant_genre_share`

Tương tự `dominant_tag` nhưng ở cấp genre.

---

# PHẦN B — SITE-LEVEL SUMMARY STATS (trong báo cáo .md)

Đây là các con số xuất hiện ở đầu báo cáo `insights_user_segments_<site>_VI.md`, mục "Tổng quan hành vi người dùng".

## B.1 Hành vi chung (5 metrics)

### B.1.1 "Trung bình page view / user"

| | |
|---|---|
| **Công thức** | `mean(user_features.total_pv)` |
| **Tính từ** | user_features CSV |
| **Ý nghĩa** | Mức PV trung bình (bị kéo bởi Power user) |
| **Cách đọc** | So sánh với trung vị để biết phân phối lệch |

### B.1.2 "Trung vị page view / user"

| | |
|---|---|
| **Công thức** | `median(user_features.total_pv)` |
| **Tính từ** | user_features CSV |
| **Ý nghĩa** | 50% user có PV dưới ngưỡng này |
| **Cách đọc** | Robust với outlier, phản ánh "user thường" |

**Tại sao mean ≠ median?**

```
Mean = 15, Median = 4
→ 50% user có ≤ 4 PV
→ Nhưng một số Power user có 500+ PV kéo mean lên 15
→ Đây là phân phối heavy-tailed
```

### B.1.3 "Trung vị sessions / user"

| | |
|---|---|
| **Công thức** | `median(user_features.sessions)` |
| **Tính từ** | user_features CSV |
| **Ý nghĩa** | User trung bình quay lại bao nhiêu lần |

### B.1.4 "Trung vị active days / user"

| | |
|---|---|
| **Công thức** | `median(user_features.active_days)` |
| **Tính từ** | user_features CSV |
| **Ý nghĩa** | User trung bình active bao nhiêu ngày trong window |

### B.1.5 "Trung vị thời gian đến lần cuối (dslv)"

| | |
|---|---|
| **Công thức** | `median(user_features.days_since_last_visit)` |
| **Tính từ** | user_features CSV |
| **Ý nghĩa** | 50% user quay lại trong vòng N ngày gần đây |

### B.1.6 "Trung vị distinct games đã chơi"

| | |
|---|---|
| **Công thức** | `median(user_features.distinct_games)` |
| **Tính từ** | user_features CSV |
| **Ý nghĩa** | User trung bình chơi bao nhiêu game |

### B.1.7 "User chơi ≥1 game"

| | |
|---|---|
| **Công thức** | `count(user_features.distinct_games > 0) / total_users` |
| **Tính từ** | user_features CSV |
| **Ý nghĩa** | Tỉ lệ user có click game |
| **Cách đọc** | 96% = phần lớn user đều chơi game |

### B.1.8 "User có ít nhất 1 phiên engaged"

| | |
|---|---|
| **Công thức** | `count(user_features.engaged_sessions > 0) / total_users` |
| **Tính từ** | user_features CSV |
| **Ý nghĩa** | Tỉ lệ user có tương tác thật (không chỉ mở page) |

## B.2 Phân bổ theo "số game đã chơi" (5 buckets)

| Bucket | Công thức đếm | Ý nghĩa |
|---|---|---|
| `0 game` | `count(distinct_games == 0)` | User không click game nào |
| `1 game` | `count(distinct_games == 1)` | Click đúng 1 game |
| `2-3 game` | `count(2 <= distinct_games <= 3)` | Click 2-3 game |
| `4-7 game` | `count(4 <= distinct_games <= 7)` | Click 4-7 game |
| `8+ game` | `count(distinct_games >= 8)` | Power user (nhiều game) |

| | |
|---|---|
| **Tính từ** | user_features CSV |
| **Trình bày** | Bảng 2 cột: bucket / count / % |
| **Use case** | Phát hiện phân bố hình chữ U (2 đầu) → cần K-Means phân cụm |

**Tại sao chọn 5 buckets cụ thể này?**
- `0` và `1` là 2 anchor points rõ ràng (zero-game, one-game)
- `2-3` và `4-7` là "casual" trung bình
- `8+` là "power user" (chia theo percentile thường > 80%)

## B.3 Phân bổ theo intent (4 intents)

| Intent | Công thức | Ý nghĩa |
|---|---|---|
| `home_pv avg` | `mean(user_features.home_pv)` | Trung bình PV trên homepage |
| `category_browse_pv avg` | `mean(user_features.category_browse_pv)` | Trung bình PV trên category |
| `search_pv avg` | `mean(user_features.search_pv)` | Trung bình PV trên search |
| `direct_game_pv avg` | `mean(user_features.direct_game_pv)` | Trung bình PV trực tiếp game |

| | |
|---|---|
| **Tính từ** | user_features CSV |
| **Trình bày** | Bảng 2 cột: intent / PV trung bình + "Đặc điểm" |
| **Use case** | So sánh "phong cách" dùng site: portal vs play |

**Cách đọc:**
- `direct_game_pv` chiếm 60%+ tổng PV → site "play" (vào chơi luôn)
- `category_browse_pv` chiếm 40%+ → site "portal" (duyệt trước, chơi sau)

## B.4 Top 5 game toàn site

| | |
|---|---|
| **Công thức** | `Counter(all_user_top_game_slug).most_common(5)` |
| **Tính từ** | user_features CSV (cột `top_game_slug`) |
| **Trình bày** | Bảng 3 cột: game / PV (sum) / user (count) |
| **Use case** | Game "cổng" của site — user tìm đến nhiều nhất |

**Lưu ý:**
- "PV" ở đây = tổng `top_game_pv` của những user chọn game đó làm yêu thích, KHÔNG phải tổng PV toàn site
- "User" = số user chọn game đó làm yêu thích

## B.5 Phân tích cohort (1 dòng)

| | |
|---|---|
| **Nội dung** | "User trưởng thành (n=...)" |
| **Công thức** | `count(distinct client_id) WHERE mature filter applied` |
| **Tính từ** | SQL aggregate trước khi xuất features |
| **Use case** | Xác nhận cohort đã áp dụng filter đúng |

---

# PHẦN C — CLUSTER-LEVEL INSIGHTS (sau clustering)

Mỗi metric trong phần này được tính **trong 1 cluster** (C0, C1, hoặc C2).

## C.1 Tổng quan cluster (1 bảng × 3 dòng)

### C.1.1 "Số user" / "%"

| | |
|---|---|
| **Công thức** | `count(cluster_id == c)` và `n_user / total_users` |
| **Tính từ** | clusters CSV |
| **Ý nghĩa** | Cluster lớn hay nhỏ |

### C.1.2 "Distinct games avg"

| | |
|---|---|
| **Công thức** | `mean(user_features.distinct_games) WHERE cluster_id == c` |
| **Tính từ** | clusters CSV |
| **Ý nghĩa** | Cluster này chơi trung bình bao nhiêu game |

### C.1.3 "Active days avg"

| | |
|---|---|
| **Công thức** | `mean(user_features.active_days) WHERE cluster_id == c` |
| **Ý nghĩa** | Cluster active bao nhiêu ngày trong window |

### C.1.4 "Dslv avg" (days since last visit)

| | |
|---|---|
| **Công thức** | `mean(user_features.days_since_last_visit) WHERE cluster_id == c` |
| **Ý nghĩa** | Cluster "gần đây" hay "lâu rồi" |
| **Cách đọc** | Power user thường < 7; Bounce thường > 14 |

### C.1.5 "Tag diversity avg"

| | |
|---|---|
| **Công thức** | `mean(user_features.tag_diversity) WHERE cluster_id == c` |
| **Ý nghĩa** | Cluster chơi bao nhiêu dòng game |

### C.1.6 "Top game share avg"

| | |
|---|---|
| **Công thức** | `mean(user_features.top_game_share) WHERE cluster_id == c` |
| **Ý nghĩa** | Cluster "trung thành 1 game" hay "đa dạng" |

## C.2 Phân bổ distinct games trong cluster (5 buckets)

| | |
|---|---|
| **Công thức** | `count(distinct_games IN bucket) WHERE cluster_id == c` |
| **Tính từ** | clusters CSV + chunk slug data |
| **Trình bày** | Bảng 3 cột: bucket / count / % |
| **Use case** | Xem cluster phân bố thế nào theo số game |

**5 buckets giống B.2:** 0 / 1 / 2-3 / 4-7 / 8+

**Tại sao tính từ 2 nguồn?** Count từ `distinct_games` column trong clusters CSV (đã có sẵn) — chính xác nhất. Count lại từ chunk data chỉ để verify.

## C.3 Slug coverage

| | |
|---|---|
| **Công thức** | `count(client_id IN chunks) / count(client_id IN cluster)` |
| **Ý nghĩa** | Bao nhiêu % user trong cluster có `top_slugs` data (chunk coverage) |
| **Cách đọc** | 100% = đầy đủ; < 90% = có thể thiếu insight |

## C.4 Top 10 game theo PV (cluster-level)

| | |
|---|---|
| **Công thức** | `SUM(slug_pv) WHERE slug ∈ direct_game AND cluster_id == c, GROUP BY slug, ORDER BY sum DESC LIMIT 10` |
| **Tính từ** | chunk slug data + cluster mapping |
| **Trình bày** | Bảng 4 cột: rank / slug / tên game / PV |
| **Ý nghĩa** | Game "gây nghiện" nhất trong cluster (nhiều lượt chơi) |

**Công thức SQL tương đương:**

```sql
SELECT slug, SUM(slug_pv) AS total_pv
FROM user_slugs
JOIN clusters USING (client_id)
WHERE cluster_id = 0
  AND slug IN (SELECT slug FROM games_meta)
GROUP BY slug
ORDER BY total_pv DESC
LIMIT 10
```

## C.5 Top 10 game theo user count (cluster-level)

| | |
|---|---|
| **Công thức** | `COUNT(DISTINCT client_id) WHERE slug IN direct_game AND cluster_id == c, GROUP BY slug, LIMIT 10` |
| **Ý nghĩa** | Game "phổ biến" nhất trong cluster (nhiều user) |
| **Khác với C.4** | C.4 = nhiều PV, C.5 = nhiều user |

**Ví dụ 1000games C0:**

| Game | PV (C.4) | User (C.5) | PV/User | Ý nghĩa |
|---|---:|---:|---:|---|
| slope-2 | 8.818 | 4.249 | 2,1 | User chơi nhiều lần |
| survival-race | 6.981 | 4.408 | 1,6 | Nhiều user, chơi trung bình |

## C.6 Top 10 game "anchor" (cluster-level)

| | |
|---|---|
| **Công thức** | `COUNT(client_id) WHERE top_game_slug = X AND cluster_id == c, GROUP BY top_game_slug, LIMIT 10` |
| **Tính từ** | clusters CSV (cột `top_game_slug`) |
| **Ý nghĩa** | Game mà user chọn làm "yêu thích" nhất (top_game) |

**Khác với C.5:** C.5 = user đã chơi game X bất kỳ. C.6 = user chọn X làm top_game (nhiều PV nhất).

## C.7 Top 15 tag theo PV (cluster-level)

| | |
|---|---|
| **Công thức** | `SUM(slug_pv) cho mỗi tag, GROUP BY tag, ORDER BY sum DESC LIMIT 15` |
| **Tính từ** | chunk slug data (join `slug_to_tags`) + cluster mapping |
| **Trình bày** | Bảng 3 cột: tag / PV / User (count) |
| **Ý nghĩa** | Tag được chơi nhiều nhất trong cluster |

**Công thức:**

```
For each user in cluster:
    For each (slug, pv) in top_slugs:
        if slug in games_meta:
            for tag in slug_to_tags[slug]:
                tag_pv[tag] += pv
                tag_users[tag] += 1  # 1 user count max / tag
```

## C.8 Top genre (cluster-level)

Tương tự C.7 nhưng ở cấp genre (1 game = 1 genre).

**Lưu ý:** 1000games catalog dùng "category" thay vì "genre" — pipeline lấy từ cột `category` thay vì `genre`.

## C.9 Distinct games bucket (cluster-level)

| | |
|---|---|
| **Công thức** | Đếm user trong cluster theo 5 buckets ở B.2 |
| **Tính từ** | clusters CSV (`distinct_games` column) |
| **Trình bày** | Bảng 3 cột: bucket / count / % |
| **Use case** | Xem phân bố "độ sâu" của cluster |

## C.10 Summary JSON

Mỗi cluster được tổng hợp thành 1 dict trong `summary.json`:

```json
{
  "cluster_0": {
    "n_users": 13723,
    "all_users_in_chunks": 13723,
    "distinct_games_buckets": {
      "0 game": 2, "1 game": 85, "2-3 game": 939,
      "4-7 game": 4284, "8+ game": 8413
    },
    "top_10_games_by_pv": [["slope-2", 8818], ...],
    "top_10_games_by_users": [["survival-race", 4408], ...],
    "top_10_top_game_slug": [["slope-2", 766], ...],
    "top_15_tags_by_pv": [["Skill Games", ...], ...],
    "top_15_tags_by_users": [...],
    "top_10_genres_by_pv": [...],
    "top_10_genres_by_users": [...],
    "top_10_dominant_tag": [...],
    "top_10_dominant_genre": [...]
  },
  "cluster_1": {...},
  "cluster_2": {...}
}
```

---

# PHẦN D — METRICS CHUYÊN BIỆT (nâng cao)

## D.1 Silhouette score

| | |
|---|---|
| **Công thức** | `silhouette = mean((b_i - a_i) / max(a_i, b_i))` với `a_i` = mean distance từ i đến các điểm cùng cụm, `b_i` = mean distance từ i đến cụm gần nhất |
| **Range** | -1 → 1 |
| **Cách đọc** | |
| - `> 0.5` | Cụm tách biệt rất rõ |
| - `0.2 - 0.5` | Tách biệt vừa phải |
| - `< 0.2` | Cụm chồng lấn (typical cho hành vi người dùng) |
| **Trong pipeline** | Sample 3.000 user, tính trên sample |
| **Công thức triển khai** | `from sklearn.metrics import silhouette_score` |

## D.2 Top game share (cluster-level)

| | |
|---|---|
| **Công thức** | `mean(user_features.top_game_share) WHERE cluster_id == c` |
| **Ý nghĩa** | Trung bình "anchor share" của user trong cluster |
| **Cách đọc** | |
| - `> 0.5` | Cluster "trung thành 1 game" |
| - `0.3 - 0.5` | Trung thành một vài game |
| - `< 0.3` | Explorer |

## D.3 Tag entropy (cluster-level)

| | |
|---|---|
| **Công thức** | `mean(user_features.tag_entropy) WHERE cluster_id == c` |
| **Ý nghĩa** | Trung bình "độ đa dạng" sở thích |

**Kết hợp với `tag_diversity`:**
- High diversity + High entropy = balanced explorer
- High diversity + Low entropy = nhiều tag nhưng tập trung vào 1-2
- Low diversity + Low entropy = niche player

## D.4 Active days (cluster-level)

| | |
|---|---|
| **Công thức** | `mean(user_features.active_days) WHERE cluster_id == c` |
| **Cách đọc** | |
| - `> 10` (28d window) | Cluster "habitual" (vào hàng tuần) |
| - `3-10` | "Regular" |
| - `1-3` | "Bounce" (chỉ vào 1-3 ngày) |
| - `1` | "True bounce" (chỉ vào đúng 1 ngày) |

## D.5 Days since last visit (cluster-level)

| | |
|---|---|
| **Công thức** | `mean(user_features.days_since_last_visit) WHERE cluster_id == c` |
| **Cách đọc** | |
| - `< 7` | Cluster "still active" |
| - `7-14` | "Cooling down" |
| - `> 14` | "Likely churned" |

---

# PHẦN E — BẢNG TỔNG HỢP 30+ METRICS

| Metric | Loại | Nguồn | Phạm vi | Use case chính |
|---|---|---|---|---|
| total_pv | feature | ClickHouse | 1 user | Khối lượng PV |
| distinct_slugs | feature | ClickHouse | 1 user | Số URL unique |
| distinct_games | feature | local | 1 user | Số game đã chơi |
| top_game_slug | feature | local | 1 user | Game yêu thích |
| top_game_pv | feature | local | 1 user | PV của top game |
| top_game_share | feature | local | 1 user | Độ trung thành 1 game |
| sessions | feature | ClickHouse | 1 user | Số session |
| engaged_sessions | feature | ClickHouse | 1 user | Session có engage |
| engaged_session_pct | feature | local | 1 user | Tỉ lệ session chất lượng |
| avg_session_sec | feature | local | 1 user | Độ dài TB session |
| total_session_sec | feature | ClickHouse | 1 user | Tổng thời gian |
| active_days | feature | ClickHouse | 1 user | Số ngày active |
| days_since_last_visit | feature | local | 1 user | Recency |
| sessions_last_7d | feature | ClickHouse | 1 user | Recency 7d |
| sessions_last_14d | feature | ClickHouse | 1 user | Recency 14d |
| home_pv | feature | local | 1 user | PV trên home |
| category_browse_pv | feature | local | 1 user | PV trên category |
| search_pv | feature | local | 1 user | PV trên search |
| direct_game_pv | feature | local | 1 user | PV trực tiếp game |
| *_share (4) | feature | local | 1 user | Tỉ lệ intent |
| tag_diversity | feature | local | 1 user | Số tag unique |
| tag_entropy | feature | local | 1 user | Shannon entropy tag |
| genre_diversity | feature | local | 1 user | Số genre unique |
| dominant_tag_share | feature | local | 1 user | Tỉ lệ top tag |
| dominant_genre_share | feature | local | 1 user | Tỉ lệ top genre |
| **mean total_pv** | site-summary | aggregate | toàn site | Trung bình PV |
| **median total_pv** | site-summary | aggregate | toàn site | Trung vị PV |
| **median sessions** | site-summary | aggregate | toàn site | Trung vị sessions |
| **median active_days** | site-summary | aggregate | toàn site | Trung vị ngày active |
| **median dslv** | site-summary | aggregate | toàn site | Trung vị recency |
| **median distinct_games** | site-summary | aggregate | toàn site | Trung vị game |
| **% user chơi ≥1 game** | site-summary | aggregate | toàn site | Coverage game |
| **% user có engaged session** | site-summary | aggregate | toàn site | Coverage engaged |
| **5 bucket distinct_games** | site-summary | aggregate | toàn site | Phân bổ game |
| **4 intent avg_pv** | site-summary | aggregate | toàn site | Phân bổ intent |
| **Top 5 game toàn site** | site-summary | aggregate | toàn site | Game "cổng" |
| **Cluster size** | cluster-summary | aggregate | 1 cluster | Số user cụm |
| **Cluster %** | cluster-summary | aggregate | 1 cluster | Tỉ lệ cụm |
| **Cluster avg features (6)** | cluster-summary | aggregate | 1 cluster | Hồ sơ cụm |
| **5 bucket trong cluster** | cluster-summary | aggregate | 1 cluster | Phân bổ game trong cụm |
| **Slug coverage** | cluster-summary | aggregate | 1 cluster | Coverage chunk data |
| **Top 10 game by PV** | cluster-insight | Counter | 1 cluster | Game nhiều PV |
| **Top 10 game by users** | cluster-insight | Counter | 1 cluster | Game nhiều user |
| **Top 10 anchor game** | cluster-insight | Counter | 1 cluster | Game "yêu thích" |
| **Top 15 tag by PV** | cluster-insight | Counter | 1 cluster | Tag nhiều PV |
| **Top 15 tag by users** | cluster-insight | Counter | 1 cluster | Tag nhiều user |
| **Top 10 genre by PV** | cluster-insight | Counter | 1 cluster | Genre nhiều PV |
| **Top 10 genre by users** | cluster-insight | Counter | 1 cluster | Genre nhiều user |
| **Silhouette score** | cluster-quality | sklearn | toàn site | K-Means quality |

---

# PHẦN F — ĐỊNH NGHĨA 4 INTENT CHI TIẾT

Đây là 4 loại page mà mỗi slug được phân loại, dùng để tính nhiều feature và insight.

## F.1 `home`

| | |
|---|---|
| **Slug pattern** | `slug == ''` (sau khi strip `https://<site>/`) |
| **Công thức Python** | `if slug == '': return 'home'` |
| **URL thực tế** | `https://1games.io/`, `https://zapgames.io/`, `https://1000games.io/` |
| **Hành vi user** | Vào homepage, không click bất kỳ link nào |
| **Use case** | Đếm "user vào không click" → bounce / nav-only |

## F.2 `category_browse`

| | |
|---|---|
| **Slug pattern 1** | Thuộc `HUB_SLUGS` (hardcoded list) |
| **Slug pattern 2** | Bắt đầu bằng `games/`, `tag/`, `category/` |
| **Công thức Python** | `if slug in HUB_SLUGS: return 'category_browse'` |
| **URL thực tế 1games** | `https://1games.io/hot-games`, `https://1games.io/recents` |
| **URL thực tế zapgames** | `https://zapgames.io/recent`, `https://zapgames.io/games/sports` |
| **URL thực tế 1000games** | `https://1000games.io/games/popular-games`, `https://1000games.io/games/action` |
| **Hành vi user** | Duyệt category page để chọn game |
| **Use case** | Đếm "user duyệt" → portal-style behavior |

**`HUB_SLUGS` mỗi site khác nhau** (xem methodology doc phần 2.3).

## F.3 `search`

| | |
|---|---|
| **Slug pattern** | Bắt đầu bằng `search` |
| **Công thức Python** | `if slug.startswith('search') or slug.startswith('search?'): return 'search'` |
| **URL thực tế** | `https://1games.io/search?q=slope`, `https://1000games.io/search?keyword=fnaf` |
| **Hành vi user** | User tìm kiếm game cụ thể (thường đã biết tên) |
| **Use case** | Đếm "user có ý định rõ ràng" → intent-based |

## F.4 `direct_game`

| | |
|---|---|
| **Slug pattern 1** | Match `^[a-z0-9]+(-[a-z0-9]+)+$` (game slug pattern) |
| **Slug pattern 2** | AND có trong catalog (`<site>_all.csv`) |
| **Công thức Python** | `if GAME_SLUG_RE.match(slug) and slug in slug_to_cats: return 'direct_game'` |
| **URL thực tế 1games** | `https://1games.io/games/slope-2` (sau strip `/games/`) |
| **URL thực tế 1000games** | `https://1000games.io/slope-2` |
| **Hành vi user** | User click thẳng vào 1 game (thường từ Google search hoặc bookmark) |
| **Use case** | Đếm "user chơi game" → play-style behavior |

**Quan trọng:** Game slug phải match regex AND có trong catalog. Nếu chỉ match regex nhưng không có metadata → `other` (không tính tag/genre).

## F.5 `other` (không phân loại)

| | |
|---|---|
| **Slug pattern** | Không thuộc 4 loại trên |
| **Ví dụ** | `404`, `sitemap.xml`, `robots.txt`, `wp-admin`, v.v. |
| **Cách xử lý** | Bỏ qua (không tính vào `*_pv`, không tag) |

---

# PHẦN G — BẢNG TÓM TẮT: METRIC NÀO DÙNG Ở ĐÂU

| Metric | `user_features` | `clusters` | `insights_*_tags` | Báo cáo .md |
|---|:---:|:---:|:---:|:---:|
| total_pv | ✓ | ✓ (col) | | mean, median, top 5 |
| distinct_slugs | ✓ | ✓ (col) | | |
| distinct_games | ✓ | ✓ (col) | ✓ (bucket) | bucket table (site + cluster) |
| top_game_slug | ✓ | ✓ (col) | ✓ (top_game_count) | top 10 anchor (cluster) |
| top_game_pv | ✓ | ✓ (col) | | |
| top_game_share | ✓ | ✓ (col) | | mean (cluster) |
| sessions | ✓ | ✓ (col) | | median (site) |
| engaged_sessions | ✓ | ✓ (col) | | |
| engaged_session_pct | ✓ | ✓ (col) | | mean (cluster) |
| avg_session_sec | ✓ | ✓ (col) | | mean (cluster) |
| total_session_sec | ✓ | ✓ (col) | | |
| active_days | ✓ | ✓ (col) | | median (site), mean (cluster) |
| days_since_last_visit | ✓ | ✓ (col) | | median (site), mean (cluster) |
| sessions_last_7d | ✓ | ✓ (col) | | |
| sessions_last_14d | ✓ | ✓ (col) | | |
| home_pv, category_browse_pv, search_pv, direct_game_pv | ✓ | ✓ (col) | | avg_pv (site) |
| *_share (4) | ✓ | ✓ (col) | | |
| tag_diversity | ✓ | ✓ (col) | | mean (cluster) |
| tag_entropy | ✓ | ✓ (col) | | mean (cluster) |
| genre_diversity | ✓ | ✓ (col) | | |
| dominant_tag_share | ✓ | ✓ (col) | | mean (cluster) |
| dominant_genre_share | ✓ | ✓ (col) | | mean (cluster) |
| top_10_games_by_pv (cluster) | | | ✓ | bảng top game (cluster) |
| top_10_games_by_users (cluster) | | | ✓ | bảng top game (cluster) |
| top_10_top_game_slug (cluster) | | | ✓ | bảng top game (cluster) |
| top_15_tags_by_pv (cluster) | | | ✓ | bảng top tag (cluster) |
| top_15_tags_by_users (cluster) | | | ✓ | bảng top tag (cluster) |
| top_10_genres_by_pv (cluster) | | | ✓ | bảng top genre (cluster) |
| top_10_genres_by_users (cluster) | | | ✓ | bảng top genre (cluster) |
| silhouette | | | | báo cáo (header) |
| cohort n | | | | báo cáo (header) |

---

# PHẦN H — CÔNG THỨC PYTHON (tham khảo)

## H.1 Tính tag entropy

```python
import math
from collections import Counter

def tag_entropy(tag_counts: Counter) -> float:
    """Shannon entropy của phân phối tag.
    tag_counts: {tag: pv}
    Returns: H = -Σ (p * log2(p))
    """
    total = sum(tag_counts.values())
    if total == 0:
        return 0.0
    H = 0.0
    for pv in tag_counts.values():
        if pv > 0:
            p = pv / total
            H -= p * math.log2(p)
    return H
```

## H.2 Tính top game theo PV (cluster-level)

```python
from collections import Counter, defaultdict

# per_cluster: {cluster_id: {game_pv: Counter, game_users: Counter, ...}}
def top_games_by_pv(cluster_data, n=10):
    """Trả về top N game theo tổng PV trong cluster."""
    return cluster_data['game_pv'].most_common(n)

# Quá trình tích lũy:
for user in cluster_users:
    for slug, pv in user['top_slugs']:
        if classify_slug(slug) == 'direct_game' and slug in catalog:
            per_cluster[user['cluster_id']]['game_pv'][slug] += int(pv)
            per_cluster[user['cluster_id']]['game_users'][slug] += 1
```

## H.3 Tính top tag theo user (1 user 1 vote)

```python
def top_tags_by_users(cluster_data, n=15):
    """Trả về top N tag theo số user trong cluster."""
    return cluster_data['tag_users'].most_common(n)

# Quá trình tích lũy (KHÁC với by_pv):
for user in cluster_users:
    user_tags_touched = set()  # <-- 1 user 1 vote
    for slug, pv in user['top_slugs']:
        if classify_slug(slug) == 'direct_game' and slug in catalog:
            for tag in catalog[slug]['tags']:
                user_tags_touched.add(tag)
    for tag in user_tags_touched:
        per_cluster[user['cluster_id']]['tag_users'][tag] += 1
```

## H.4 Tính distinct games bucket

```python
def bucket_distinct_games(n: int) -> str:
    """Chuyển số game thành bucket label."""
    if n == 0:   return '0 game'
    elif n == 1: return '1 game'
    elif n <= 3: return '2-3 game'
    elif n <= 7: return '4-7 game'
    else:        return '8+ game'

# Trong báo cáo 1games (version cũ) dùng bucket khác:
def bucket_distinct_games_v1(n: int) -> str:
    if n == 0:   return '0'
    elif n == 1: return '1'
    elif n <= 3: return '2-3'
    elif n <= 7: return '4-7'
    else:        return '8+'
```

## H.5 Tính silhouette

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import numpy as np

# Scale features
scaler = StandardScaler()
X_std = scaler.fit_transform(X)

# Sweep K
results = []
sample_idx = np.random.default_rng(42).choice(len(X), size=3000, replace=False)
for k in [3, 4, 5]:
    km = KMeans(n_clusters=k, n_init=10, random_state=42, max_iter=300)
    labels = km.fit_predict(X_std)
    sil = silhouette_score(X_std[sample_idx], labels[sample_idx])
    results.append({'k': k, 'silhouette': sil, 'model': km, 'labels': labels})

# Pick best
best = max(results, key=lambda r: r['silhouette'])
K = best['k']
final_labels = best['labels']
```

---

# PHẦN I — DEPENDENCIES & OUTPUTS

## I.1 Code dependencies (mỗi metric phụ thuộc vào gì)

```
ClickHouse gm_pages
  └─ Step 1: User aggregates (SQL GROUP BY)
      └─ total_pv, distinct_slugs, sessions, engaged_sessions,
      └─ total_engaged_sec, active_days, first_date, last_date
  └─ Step 1b: Top slugs (groupArray(20))
      └─ top 20 (slug, pv) per user

Catalog CSV (<site>_all.csv)
  └─ slug_to_cats, slug_to_tags, slug_to_genre
  └─ used in classify_slug() and tag/genre calculation

Local Python (Step 1c)
  └─ 25 features written to user_features_<site>.csv

K-Means (Step 2)
  └─ clusters_<site>.csv (adds cluster_id column)

Per-cluster aggregations (Step 3)
  └─ 10 CSV per cluster + summary.json
```

## I.2 Output files (mỗi metric xuất hiện ở đâu)

```
user_features_<site>_2026-10-01.csv
  └─ 25 columns, 1 row / user
  └─ ~32k-58k rows

clusters_<site>_2026-10-01.csv
  └─ user_features columns + cluster_id
  └─ same row count

insights_<site>_tags/
  ├─ summary.json
  └─ cluster0/cluster1/cluster2/
      ├─ top_games_by_pv.csv (10 rows)
      ├─ top_games_by_users.csv (10 rows)
      ├─ top_game_count.csv (10 rows)
      ├─ top_tags_by_pv.csv (15 rows)
      ├─ top_tags_by_users.csv (15 rows)
      ├─ top_tag_count.csv (15 rows)
      ├─ top_genres_by_pv.csv (10 rows)
      ├─ top_genres_by_users.csv (10 rows)
      ├─ top_genre_count.csv (10 rows)
      └─ distinct_games_buckets.csv (5 rows)

insights_user_segments_<site>_VI.md
  └─ Site-level summary + 3 cluster profiles

insights_games_tags_<site>_VI.md
  └─ 3 cluster sections (game/tag/genre tables) + comparisons
```

---

**Tác giả:** Game analytics
**Ngày tạo:** 2026-10-09
**Phiên bản:** 1.0
**Áp dụng cho:** 1games.io, zapgames.io, 1000games.io (window 2026-09-03 → 2026-10-01)
