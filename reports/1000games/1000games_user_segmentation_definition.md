# Phân tích hành vi người dùng & phân khúc — 1000games.io

**Site:** 1000games.io
**Khoảng thời gian:** 22 ngày kết thúc ngày 1 tháng 10, 2026 (2026-09-10 → 2026-10-01)
**Phương pháp:** K-Means (StandardScaler + 23 features)
**Cohort:** user trưởng thành (≥1 page view trong window, n=52.608)
**Silhouette (K=3):** 0.26
**Ngày:** 8 tháng 10, 2026

---

## 1. Tổng quan hành vi người dùng 1000games

Tổng số user có page view trong 22 ngày: **52.608 unique** (từ 784.208 page view trên 200.355 phiên, 22 ngày).

### Hành vi chung

| Chỉ số | Giá trị |
|---|---:|
| Trung bình page view / user (mean) | ~15 |
| Trung vị page view / user (median) | 4 |
| Trung vị sessions / user | 6 |
| Trung vị active days / user | 1 |
| Trung vị thời gian đến lần cuối (dslv) | 7 ngày |
| Trung vị distinct games đã chơi | 3 |
| User chơi ≥1 game | 96% |
| User có ít nhất 1 phiên engaged (>0s) | 99% |

→ **Phân bố PV lệch phải mạnh**: trung bình ~15 PV nhưng trung vị chỉ 4 — nghĩa là phần lớn user xem ít, một số ít xem rất nhiều. Đây là dấu hiệu điển hình của "long tail" — phù hợp để phân cụm.

### Phân bổ theo "số game đã chơi"

| Số game | User | % |
|---:|---:|---:|
| 0 game | 2.206 | 4,2% |
| 1 game | 16.043 | 30,5% |
| 2–3 game | 11.767 | 22,4% |
| 4–7 game | 9.964 | 18,9% |
| 8+ game | 9.070 | 17,2% |

→ **Phân bổ hình chữ U**: 35% user chơi ≤1 game, 17% user chơi 8+ game, phần còn lại ở giữa. Hai đầu của chữ U sẽ là hai phân khúc "Bounce" và "Power user".

### Phân bổ theo intent (loại page)

| Intent | PV trung bình / user | Đặc điểm |
|---|---:|---|
| `home` (trang chủ) | 1,2 | User vào nhưng không click |
| `category_browse` (games/, tag/, hot, recent, v.v.) | 2,8 | User duyệt category |
| `search` (tìm kiếm) | 0,4 | User search tên game cụ thể |
| `direct_game` (vào thẳng 1 game) | 9,1 | User click thẳng 1 game |

→ **Vào thẳng game chiếm ~60% PV** — 1000games chủ yếu là site "vào rồi chơi", không phải "duyệt rồi chọn". Đây là khác biệt lớn so với site "cổng" nơi user duyệt category để chọn game.

### 5 game được click nhiều nhất toàn site

| # | Game | PV | User |
|---:|---|---:|---:|
| 1 | slope-2 | ~26.013 | ~9.086 |
| 2 | survival-race | ~21.175 | ~9.054 |
| 3 | golf-hit | ~18.525 | ~6.465 |
| 4 | polytrack | ~16.377 | ~5.000+ |
| 5 | frontwarsio | ~13.645 | ~2.000+ |

→ **slope-2 và survival-race** chiếm 2 vị trí đầu, tương đương nhau về user (~9k) và PV (~20-26k). Đây là 2 "game cổng" của 1000games.

---

## 2. Phân khúc 3 cụm K-Means (K=3)

| Phân khúc | Số user | % | Distinct games avg | active_days avg | dslv avg | tag_diversity avg | top_game_share avg |
|---|---:|---:|---:|---:|---:|---:|---:|
| 🟢 Lõi trung thành (C0) | 13.723 | 26% | **9,6** | 3,6 | 4,9d | **28,8** | 21% |
| 🔴 Vào rồi thoát (C1) | 20.042 | 38% | 1,5 | 1,1 | 7,9d | 6,9 | 2% |
| 🟡 Trung thành 1-3 game (C2) | 18.843 | 36% | 2,5 | 1,3 | 7,8d | 10,7 | **53%** |

### Phân khúc 🟢 Lõi trung thành (Power user) — C0

- **Số user:** 13.723 (26%)
- **Hành vi:** chơi 9,6 game trung bình, 3,6 active days, 28,8 tag diversity
- **Slug coverage:** 100% (13.723/13.723)
- **Phân bổ distinct games:**

| Bucket | User | % |
|---|---:|---:|
| 0 game | 2 | 0,01% |
| 1 game | 85 | 0,6% |
| 2–3 game | 939 | 6,8% |
| 4–7 game | 4.284 | 31,2% |
| 8+ game | **8.413** | **61,3%** |

→ **61% Lõi trung thành chơi 8+ game trong 22 ngày.** Phân khúc này thật sự "explorer" — chơi rất nhiều, không trung thành với 1 game.

### Phân khúc 🔴 Vào rồi thoát (Bounce / nav-only) — C1

- **Số user:** 20.042 (38%)
- **Hành vi:** 1,5 distinct games, 1,1 active days, gần như 0% top_game_share
- **Slug coverage:** 82% (16.484/20.042)
- **Phân bổ distinct games:**

| Bucket | User | % |
|---|---:|---:|
| 0 game | **1.864** | **9,3%** |
| 1 game | 8.419 | 42,0% |
| 2–3 game | 4.222 | 21,1% |
| 4–7 game | 1.713 | 8,5% |
| 8+ game | 266 | 1,3% |

→ **9,3% user trong C1 không chơi game nào** (1.864 user). 42% chơi đúng 1 game. Đây là phân khúc "thử một lần" của 1000games — họ vào, xem, click 1 game (slope-2 / polytrack / geometry-dash) rồi biến mất.

### Phân khúc 🟡 Trung thành 1-3 game (Casual browser) — C2

- **Số user:** 18.843 (36%)
- **Hành vi:** 2,5 distinct games, 53% top_game_share (cao nhất), 10,7 tag diversity
- **Slug coverage:** 100% (18.843/18.843)
- **Phân bổ distinct games:**

| Bucket | User | % |
|---|---:|---:|
| 0 game | 340 | 1,8% |
| 1 game | **7.539** | 40,0% |
| 2–3 game | 6.606 | 35,1% |
| 4–7 game | 3.967 | 21,1% |
| 8+ game | 391 | 2,1% |

→ **40% Trung thành 1-3 game chơi đúng 1 game**, 35% chơi 2-3 game. **Tổng cộng 75% C2 chơi ≤ 3 game.** **Anh/chị em của họ (C0) chơi 9,6 game trung bình** — đây là 2 phân khúc hoàn toàn khác nhau về hành vi chơi.

---

## 3. Câu hỏi mở cho team

1. **38% Bounce (C1) — 20.042 user chỉ xem 1-2 lần. Traffic đến từ đâu?** Nếu từ Google search → cần SEO/landing page tốt hơn. Nếu từ social → cần "nội dung hấp dẫn giữ chân".

2. **Tại sao Trung thành 1-3 game (C2) KHÔNG chuyển thành Lõi trung thành (C0)?** Họ thích 1-3 game, 53% top_game_share. Cần widget "Game cùng cluster" hoặc recommendation để kéo họ lên.

3. **Có nên "early access" game mới cho C0?** Họ chơi 9,6 game, 28,8 tag diversity → sẵn sàng thử game mới.

---

## Tìm dữ liệu ở đâu

| File | Nội dung |
|---|---|
| `d:\GR\User Segmentation\data\user_features_1000games_2026-10-01.csv` | 64.127 user features (sau dedupe 52.608) |
| `d:\GR\User Segmentation\data\clusters_1000games_2026-10-01.csv` | Features + cluster_id |
| `d:\GR\03_data\processed\user_features\1000games_chunks\` | 13 chunks of top-slugs data |
| `d:\GR\1000games_all.csv` | Metadata 489 game |
| `d:\GR\1000games_step1_features.py` | Script build features |
| `d:\GR\1000games_step3_insights.py` | Script build game/tag insights |

---

**Ngày tạo:** 2026-10-08
**Phương pháp:** StandardScaler + 23 features + K-Means (K=3, n_init=10, random_state=42)
**Silhouette (K=3, sample 3.000 user):** 0.26
