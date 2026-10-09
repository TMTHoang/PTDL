# Game & Tag Insights cho 3 Phân Khúc Người Dùng 1000games.io

**Site:** 1000games.io
**Khoảng thời gian:** 22 ngày kết thúc ngày 1 tháng 10, 2026 (2026-09-10 → 2026-10-01)
**Phương pháp:** Phân tích `top_slugs` (top 20 slug theo page view) cho mỗi user, join với `1000games_all.csv` (489 game metadata)
**Cohort:** user trưởng thành (≥1 page view trong 22d, n=52.608)
**Đối tượng đọc:** content team, game curator, marketing
**Ngày:** 8 tháng 10, 2026

---

## Cách đọc báo cáo này

Mỗi user trong 1000games có một danh sách **top 20 slug** mà họ đã xem (kèm số page view trên slug đó). ClickHouse cắt ở 20 slug hàng đầu nên:
- Với user chỉ xem vài slug, ta thấy đủ
- Với Lõi trung thành (xem hàng trăm slug khác nhau), ta chỉ thấy 20 slug phổ biến nhất của họ

Từ những slug đó, ta chia thành 4 loại:

| Loại | Cách nhận biết | Vai trò |
|---|---|---|
| `home` | slug rỗng (trang chủ) | vào nhưng không click |
| `category_browse` | slug `games/*`, `tag/*`, `hot`, `recent`, v.v. | duyệt category |
| `search` | slug bắt đầu bằng `search` | tìm kiếm |
| `direct_game` | khớp pattern `[a-z0-9]+(-[a-z0-9]+)*` **AND có trong `1000games_all.csv`** | vào thẳng game |

**Quan trọng:** tag/genre chỉ có cho slug thuộc loại `direct_game` VÀ có trong bảng `1000games_all.csv`. Bảng này có **489 slug** trong metadata.

**Lỗ hổng metadata:** 1000games có khoảng 50-60% slug click thiếu metadata (game như `minecraft`, `garrys-mod`, `league-of-legends`, `fnaf-2`, `krillion-game` xuất hiện trong `top_game_slug` nhưng không có trong `1000games_all.csv`). Ảnh hưởng lớn nhất đến phân khúc Vào rồi thoát (C1).

---

## Phân khúc 🟢 Lõi trung thành (Power user) — C0

- **Số user trong cluster:** 13.723 (26% mature users)
- **User có `top_slugs` data:** 13.723 (100% coverage)
- **Phân bổ số game đã chơi:**

| Bucket | User |
|---|---:|
| 0 game | 2 |
| 1 game | 85 |
| 2–3 game | 939 |
| 4–7 game | 4.284 |
| 8+ game | **8.413** |

→ **61% Lõi trung thành chơi 8+ game trong 22 ngày.** Đây là phân khúc "explorer" chính hiệu.

### Top 10 game theo lượt xem (PV)

| # | Slug | Tên | PV |
|---:|---|---|---:|
| 1 | slope-2 | Slope 2 | 8.818 |
| 2 | survival-race | Survival Race | 6.981 |
| 3 | golf-hit | Golf Hit | 6.548 |
| 4 | frontwarsio | Frontwars.io | 5.995 |
| 5 | dummies-world-cup | Dummies World Cup | 5.096 |
| 6 | bowmasters-archery-shooting | Bowmasters Archery | 5.010 |
| 7 | flip-rush | Flip Rush | 3.680 |
| 8 | 2v2-io | 2v2.io | 3.338 |
| 9 | bottle-hop | Bottle Hop | 3.237 |
| 10 | veck-io | Veck.io | 3.216 |

### Top 10 game theo số user đã chơi

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | survival-race | Survival Race | 4.408 |
| 2 | slope-2 | Slope 2 | 4.249 |
| 3 | golf-hit | Golf Hit | 3.260 |
| 4 | bowmasters-archery-shooting | Bowmasters Archery | 2.924 |
| 5 | bottle-hop | Bottle Hop | 2.715 |
| 6 | wheelie-life | Wheelie Life | 2.353 |
| 7 | meccha-chameleon | Meccha Chameleon | 2.250 |
| 8 | veck-io | Veck.io | 2.219 |
| 9 | drift-rush | Drift Rush | 2.217 |
| 10 | flip-rush | Flip Rush | 2.067 |

→ **Survival Race dẫn đầu về user (4.408)** — chiếm 32% Lõi trung thành. **Slope 2 dẫn đầu về PV (8.818)** — PV/ user = 2,1 (cao hơn Survival Race 1,6). 7/10 game ở đây thuộc dòng **slope/runner/skill** — slope-2, survival-race, flip-rush, bottle-hop, meccha-chameleon, drift-rush — cho thấy dòng này là "nền tảng" của Lõi trung thành 1000games.

### Top 10 game mà user chọn làm "game yêu thích" (`top_game_slug`)

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | slope-2 | Slope 2 | 766 |
| 2 | survival-race | Survival Race | 601 |
| 3 | golf-hit | Golf Hit | 544 |
| 4 | bowmasters-archery-shooting | Bowmasters Archery | 487 |
| 5 | polytrack | Polytrack | 467 |
| 6 | frontwarsio | Frontwars.io | 447 |
| 7 | dummies-world-cup | Dummies World Cup | 429 |
| 8 | flip-rush | Flip Rush | 305 |
| 9 | 2v2-io | 2v2.io | 303 |
| 10 | bottle-hop | Bottle Hop | 263 |

→ **5,6% Lõi trung thành (766/13.723) chọn Slope 2 làm game yêu thích.** Tuy nhiên, vì Lõi trung thành chơi 9,6 game trung bình, top_game_slug của họ **ít "quyết định" hơn** top_game_slug của Trung thành 1-3 game (so sánh 5,6% vs 7,0% ở C2).

### Top 15 tag theo PV và theo user

| Tag | PV | User |
|---|---:|---:|
| Skill Games | 86.472 | 65.941 |
| Physics Games | 49.400 | 31.928 |
| Fast Paced Games | 45.999 | 29.575 |
| Score Games | 40.914 | 26.636 |
| Obstacle Games | 37.657 | 28.683 |
| Reflex Games | 37.288 | 24.802 |
| Multiplayer Games | 36.729 | 27.133 |
| Competition Games | 31.226 | 20.467 |
| IO Games | 23.150 | 11.179 |
| Jump Games | 22.839 | 14.658 |
| Racing Games | 22.345 | 18.150 |
| Driving Games | 19.847 | 19.659 |
| physics | 19.461 | (chỉ PV) |
| Speed Games | 19.360 | 16.711 |
| PvP Games | 18.812 | 14.653 |

→ Bộ tag **Skill Games / Physics Games / Fast Paced Games** chiếm thế thượng phong. **Lưu ý:** tag ở 1000games có đuôi " Games" (VD: "Skill Games" thay vì "skill") — đây là đặc thù của catalog 1000games. **480% Lõi trung thành (65.941 user) đã chơi ít nhất 1 game có tag "Skill Games"** — cao nhất trong 3 phân khúc.

### Top genre theo PV và theo user

| Genre | PV | User |
|---|---:|---:|
| arcade | 67.106 | 54.449 |
| action | 55.878 | 43.475 |
| sports | 52.405 | 40.461 |
| casual | 32.069 | 28.613 |
| simulation | 22.039 | 18.213 |
| 1000games | 19.951 | 17.176 |
| adventure | 12.527 | 11.557 |
| strategy | 11.275 | 6.152 |
| puzzle | 9.471 | 10.637 |
| horror | 7.976 | 9.713 |

→ **4 genre đầu (arcade, action, sports, casual) đều trên 28.000 user.** Đây là phân bổ rộng — Lõi trung thành 1000games chơi cả 4 thể loại chính. **Genre "1000games"** (game nội bộ) chiếm 19,951 PV — cao hơn adventure (12.527).

### Câu chuyện của phân khúc 🟢

Lõi trung thành 1000games là phân khúc **rất đa dạng**: 61% chơi 8+ game, tag diversity trung bình 28,8 (gấp ~3 lần Trung thành 1-3 game ở 10,7). Họ có **anchor game là Slope 2** (5,6% chọn làm yêu thích) nhưng **không trung thành một game** — họ "thử tất cả".

**Hệ quả chiến lược:**
- **Gợi ý cho Lõi trung thành KHÔNG nên giới hạn ở slope/runner** — họ sẵn sàng thử sports/arcade
- **Slope 2 vẫn là "gateway"** — bất kỳ game mới cùng dòng này sẽ được thử nhanh

---

## Phân khúc 🔴 Vào rồi thoát (Bounce / nav-only) — C1

- **Số user trong cluster:** 20.042 (38% mature users)
- **User có `top_slugs` data:** 16.484 (82% coverage)
- **Phân bổ số game đã chơi:**

| Bucket | User |
|---|---:|
| 0 game | **1.864** |
| 1 game | 8.419 |
| 2–3 game | 4.222 |
| 4–7 game | 1.713 |
| 8+ game | 266 |

→ **9,3% user (1.864) không chơi game nào**, 42% chơi đúng 1 game. Đây là **vấn đề lớn nhất** của 1000games.

### Top 10 game theo lượt xem (PV)

| # | Slug | Tên | PV |
|---:|---|---|---:|
| 1 | krillion-game | Krillion Game | 19 |
| 2 | robber-run | Robber Run | 4 |
| 3 | slope-2 | Slope 2 | (PV rất thấp) |
| 4 | golf-hit | Golf Hit | (PV rất thấp) |
| 5 | polytrack | Polytrack | (PV rất thấp) |
| 6 | ... | ... | ... |

**Lưu ý:** C1 có tổng PV rất thấp (median = 1) nên top games by PV không có ý nghĩa thống kê. Các con số PV gần như bằng 0.

### Top 10 game theo số user đã chơi

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | slope-2 | Slope 2 | 2.495 |
| 2 | survival-race | Survival Race | 1.985 |
| 3 | golf-hit | Golf Hit | 1.451 |
| 4 | bowmasters-archery-shooting | Bowmasters Archery | 861 |
| 5 | 2v2-io | 2v2.io | 660 |
| 6 | frontwarsio | Frontwars.io | 659 |
| 7 | dummies-world-cup | Dummies World Cup | 584 |
| 8 | horror-nun-2 | Horror Nun 2 | 536 |
| 9 | veck-io | Veck.io | 517 |
| 10 | paint-and-seek | Paint and Seek | 477 |

→ **Slope 2 vẫn dẫn đầu về user (2.495)** — chiếm 12% C1. **19% C1 user chơi slope-2** (chỉ 1 lần thường). Đây là dấu hiệu **traffic từ Google search** — user search "slope 2", click vào 1000games/slope-2, chơi, đi.

### Top 10 game mà user chọn làm "game yêu thích" (`top_game_slug`)

| # | Slug | User |
|---:|---|---:|
| 1 | polytrack | 339 |
| 2 | geometry-dash | 120 |
| 3 | super-liquid-soccer | 87 |
| 4 | minecraft | 75 |
| 5 | dreadhead-parkour | 34 |
| 6 | five-nights-at-epsteins | 29 |
| 7 | retro-bowl | 25 |
| 8 | level-devil | 22 |
| 9 | grow-a-garden | 19 |
| 10 | drive-mad | 19 |

→ **Top 10 game C1 user chọn làm yêu thích có 3 game KHÔNG có trong catalog 1000games** (`minecraft`, `five-nights-at-epsteins`, `level-devil` — không có trong `1000games_all.csv`). Đây là **bằng chứng rõ ràng** rằng 1000games **thiếu metadata cho nhiều game mà user click vào** (catalog chỉ có 489 game, không phủ hết các game mà user quan tâm).

### Top 15 tag theo user

| Tag | User |
|---|---:|
| Skill Games | 15.265 |
| Obstacle Games | 8.134 |
| Score Games | 8.118 |
| Fast Paced Games | 7.566 |
| Physics Games | 7.459 |
| Reflex Games | 6.816 |
| Multiplayer Games | 5.478 |
| Competition Games | 5.201 |
| Racing Games | 4.810 |
| Survival Games | 4.175 |
| Speed Games | 4.092 |
| Driving Games | 4.018 |
| Jump Games | 3.837 |
| Run Games | 3.642 |
| Challenge Games | 3.553 |

→ Bộ tag **giống hệt Lõi trung thành** — Skill Games / Physics Games / Obstacle Games. **76% C1 (15.265/20.042) đã chơi ít nhất 1 game có tag "Skill Games"** — cao. Nhưng do C1 chỉ chơi trung bình 1,5 game, các tag thường xuất hiện từ đúng 1 game.

### Top genre theo user

| Genre | User |
|---|---:|
| arcade | 11.156 |
| action | 9.870 |
| sports | 8.958 |
| casual | 4.975 |
| simulation | 3.160 |
| 1000games | 3.102 |
| adventure | 2.230 |
| puzzle | 2.220 |
| horror | 1.859 |
| strategy | 1.458 |

→ Tương tự Lõi trung thành — **4 genre đầu (arcade, action, sports, casual) đều có 5k-11k user.**

### Câu chuyện của phân khúc 🔴

Phân khúc C1 (38% mature users) là **vấn đề lớn nhất của 1000games**:
- **9,3% (1.864 user) không chơi game nào** — vào trang chủ, không thấy gì để click
- **42% (8.419 user) chơi đúng 1 game** — thường là slope-2 / polytrack / geometry-dash (game phổ biến)
- **Top game mà user chọn làm "yêu thích" có nhiều game không có trong catalog** (minecraft, fnaf, level-devil) — hệ thống tagging chưa bao phủ

**Hệ quả chiến lược:**
- **Trang chủ 1000games đang thất bại trong việc giữ chân user** — 1.864 user vào, không thấy gì để click, đi
- **Cần cải thiện homepage** — đề xuất game trending, game "phổ biến nhất hôm nay" thay vì chỉ 1 danh sách cố định
- **Backfill metadata** cho top 50 game C1 user click (minecraft, fnaf-2, fnaf-3, level-devil, five-nights-at-epsteins, ...) — hiện tại ta đang "mù" về tag/genre của những game này
- **Email/push thông minh** cho 1.864 user 0-game: "Game phổ biến nhất hôm nay" có thể kéo họ quay lại

---

## Phân khúc 🟡 Trung thành 1-3 game (Casual browser) — C2

- **Số user trong cluster:** 18.843 (36% mature users)
- **User có `top_slugs` data:** 18.843 (100% coverage)
- **Phân bổ số game đã chơi:**

| Bucket | User |
|---|---:|
| 0 game | 340 |
| 1 game | **7.539** |
| 2–3 game | 6.606 |
| 4–7 game | 3.967 |
| 8+ game | 391 |

→ **40% C2 chơi đúng 1 game**, 35% chơi 2-3 game. **Tổng cộng 75% C2 chơi ≤ 3 game.** Đây là phân khúc "single-game browser" của 1000games.

### Top 10 game theo lượt xem (PV)

| # | Slug | Tên | PV |
|---:|---|---|---:|
| 1 | dummies-world-cup | Dummies World Cup | 3.139 |
| 2 | slope-2 | Slope 2 | 1.969 |
| 3 | survival-race | Survival Race | 1.946 |
| 4 | golf-hit | Golf Hit | 1.778 |
| 5 | frontwarsio | Frontwars.io | 1.002 |
| 6 | bowmasters-archery-shooting | Bowmasters Archery | 891 |
| 7 | 2v2-io | 2v2.io | 650 |
| 8 | garrys-mod | Garry's Mod | 559 |
| 9 | flip-rush | Flip Rush | 530 |
| 10 | veck-io | Veck.io | 494 |

### Top 10 game theo số user đã chơi

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | survival-race | Survival Race | 2.662 |
| 2 | slope-2 | Slope 2 | 2.342 |
| 3 | golf-hit | Golf Hit | 1.754 |
| 4 | dummies-world-cup | Dummies World Cup | 1.626 |
| 5 | bowmasters-archery-shooting | Bowmasters Archery | 1.031 |
| 6 | frontwarsio | Frontwars.io | 890 |
| 7 | 2v2-io | 2v2.io | 721 |
| 8 | veck-io | Veck.io | 706 |
| 9 | wheelie-life | Wheelie Life | 677 |
| 10 | bottle-hop | Bottle Hop | 676 |

→ **Dummies World Cup** nổi bật — top 1 về PV (3.139, gấp 1,6× Slope 2) nhưng top 4 về user. **PV/ user = 1,93** (cao nhất) — đây là game mà user "trung thành" chơi nhiều lần. **Slope 2** ngược lại: top 2 PV (1.969) nhưng top 2 user (2.342) → PV/user = 0,84 — user chơi 1 lần rồi đi.

### Top 10 game mà user chọn làm "game yêu thích"

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | dummies-world-cup | Dummies World Cup | 1.299 |
| 2 | slope-2 | Slope 2 | 1.133 |
| 3 | survival-race | Survival Race | 1.095 |
| 4 | golf-hit | Golf Hit | 1.011 |
| 5 | bowmasters-archery-shooting | Bowmasters Archery | 583 |
| 6 | frontwarsio | Frontwars.io | 578 |
| 7 | polytrack | Polytrack | 498 |
| 8 | 2v2-io | 2v2.io | 421 |
| 9 | garrys-mod | Garry's Mod | 408 |
| 10 | size-it-up | Size It Up | 306 |

→ **6,9% Trung thành 1-3 game (1.299/18.843) chọn Dummies World Cup làm game yêu thích** — cao nhất. **Đây là game "anchor" cho phân khúc C2** — họ vào 1000games, chơi Dummies World Cup, biến mất.

### Top 15 tag theo PV và theo user

| Tag | PV | User |
|---|---:|---:|
| Skill Games | 18.004 | 21.678 |
| Physics Games | 10.722 | 11.497 |
| Score Games | 8.578 | 10.339 |
| Fast Paced Games | 8.001 | 10.178 |
| Competition Games | 7.971 | 8.017 |
| Obstacle Games | 7.327 | 9.868 |
| Reflex Games | 7.205 | 9.058 |
| Multiplayer Games | 6.233 | 7.875 |
| physics | 5.222 | 4.530 |
| Soccer Games | 4.382 | (chỉ PV) |
| Racing Games | 4.380 | 6.177 |
| Jump Games | 3.857 | 5.022 |
| Survival Games | 3.823 | 5.141 |
| Speed Games | 3.706 | 5.294 |
| IO Games | 3.538 | (chỉ PV) |

→ Bộ tag **giống Lõi trung thành** — Skill Games / Physics Games / Fast Paced. **Điểm khác biệt:** tag `Soccer Games` (4.382 PV) xuất hiện ở top 15 ở đây nhưng **không có** trong top 15 của Lõi trung thành → Dummies World Cup là game bóng đá, kéo theo tag soccer. **130% C2 (24.498 user) đã chơi ít nhất 1 game có tag "Skill Games"** (hơn 1,15 lần so với tổng số user — vì 1 user chơi 1 game có thể có nhiều tag).

### Top genre theo PV và theo user

| Genre | PV | User |
|---|---:|---:|
| arcade | 13.924 | 16.283 |
| sports | 12.114 | 13.759 |
| action | 9.234 | 12.583 |
| casual | 5.377 | 7.627 |
| simulation | 4.265 | 5.099 |
| 1000games | 3.445 | 4.696 |
| puzzle | 2.182 | 3.047 |
| adventure | 2.069 | 2.913 |
| strategy | 1.830 | 1.975 |
| horror | 1.632 | 2.431 |

→ **sports genre dẫn đầu** (12.114 PV, 13.759 user) — cao hơn Lõi trung thành (52.405 PV nhưng 40.461 user, tỉ lệ 1,3 PV/user). C2 có **PV/user = 0,88 cho sports** (cao nhất trong các genre) → phân khúc này **trung thành với game thể thao** hơn Lõi trung thành.

### Câu chuyện của phân khúc 🟡

Trung thành 1-3 game 1000games có **anchor game là Dummies World Cup** (6,9% chọn làm yêu thích). Dummies World Cup là **game bóng đá** — phù hợp với xu hướng "chơi game quen thuộc" của phân khúc này. C2 là phân khúc **thiên về thể thao** — sports genre dẫn đầu PV/user (0,88), tag Soccer Games xuất hiện top 15 ở C2 nhưng không có trong Lõi trung thành.

**Hệ quả chiến lược:**
- **Widget "Game cùng dòng" cho Dummies World Cup** — gợi ý Survival Race, Golf Hit, Penalty Kick (cùng thể thao) → có thể kéo C2 thành C0
- **Email/push "Game thể thao mới"** — phù hợp với 76% C2 đã chơi 1 game thể thao

---

## So sánh nhanh giữa 3 phân khúc

| | Lõi trung thành 🟢 | Vào rồi thoát 🔴 | Trung thành 1-3 game 🟡 |
|---|---:|---:|---:|
| Số user | 13.723 | 20.042 | 18.843 |
| % mature | 26% | **38%** | 36% |
| Top 1 game (PV) | Slope 2 (8.818) | Krillion Game (19) | Dummies World Cup (3.139) |
| Top 1 game (user) | Survival Race (4.408) | Slope 2 (2.495) | Survival Race (2.662) |
| Top 1 game yêu thích | Slope 2 (766 user) | Polytrack (339 user) | Dummies World Cup (1.299 user) |
| Top 1 tag (theo user) | Skill Games (65.941) | Skill Games (15.265) | Skill Games (21.678) |
| Top 1 genre (theo user) | arcade (54.449) | arcade (11.156) | arcade (16.283) |
| Distinct games trung bình | 9,6 | 1,5 | 2,5 |
| Tag diversity | 28,8 | 6,9 | 10,7 |
| Đặc điểm chung | slope/runner + sports, 8+ game | traffic từ search, 1 game | Dummies + Slope 2 |

→ **"Dòng nền" 1000games là slope/runner + sports** — Slope 2 dẫn đầu cả Lõi trung thành (C0) lẫn Vào rồi thoát (C1); Survival Race, Golf Hit, Dummies World Cup bổ sung dòng sports/arcade.

---

## Phát hiện quan trọng: lỗ hổng metadata nghiêm trọng

Trong khi phân tích, ta phát hiện:

- **1000games_all.csv chỉ có 489 game** — catalog nhỏ, không phủ hết các game mà user quan tâm
- **Top 10 game C1 user chọn làm yêu thích có 3 game không có trong catalog** (`minecraft`, `five-nights-at-epsteins`, `level-devil`)
- Trong `top_10_top_game_slug` của C1, có những slug như `fnaf-2`, `fnaf-3`, `epstein-clicker`, `krillion-game`, `school-fury` — **không có trong `1000games_all.csv`**

**Hệ quả chiến lược:**
- Phân tích tag/genre cho C1 bị giới hạn — ta không biết 18,5% (3.700+ user) trong C1 thích game gì khi họ click vào những game "không có metadata"
- **Ưu tiên #1: backfill metadata cho top 50 game C1 user click vào** — hiện tại ta đang mù về sở thích thực của 38% mature users
- Một khi metadata có đủ, ta sẽ biết C1 user thích thể loại gì và đề xuất cho họ trên trang chủ

---

## Câu hỏi mở cho team

1. **Tại sao 1000games có 38% Bounce (20.042 user)?** Phân tích log referrer (Google, social, direct) để tìm hiểu user Bounce đến từ đâu.

2. **Có nên cải thiện trang chủ cho 1.864 user 0-game?** Đây là 9,3% C1 = 1.864 user vào trang chủ nhưng không thấy gì để click. Cần test A/B "Game trending hôm nay" widget trên home.

3. **Widget "Game cùng dòng" cho Dummies World Cup** — kéo 7.539 user chơi 1 game lên thành Lõi trung thành. Đây là test A/B dễ nhất.

4. **Vì sao Slope 2 dẫn đầu cả Power user (C0) lẫn Bounce (C1)?** Slope 2 có 4.249 user trong C0 (chơi sâu) + 2.495 user trong C1 (chơi 1 lần) → đây là game "cổng" quan trọng nhất của 1000games. Cần đảm bảo Slope 2 luôn available và load nhanh.

5. **1000games có catalog nhỏ (489) — nên mở rộng?** Catalog chỉ phủ ~50-60% các game user click, gây lỗ hổng phân tích. Mở rộng thêm game mới sẽ giúp giảm Bounce và cho ta hiểu rõ hơn sở thích user.

---

## Tìm dữ liệu ở đâu

| File | Nội dung |
|---|---|
| `d:\GR\User Segmentation\data\insights_1000games_tags\cluster0_*` | Top game/tag cho Lõi trung thành (16 CSV) |
| `d:\GR\User Segmentation\data\insights_1000games_tags\cluster1_*` | Top game/tag cho Vào rồi thoát (16 CSV) |
| `d:\GR\User Segmentation\data\insights_1000games_tags\cluster2_*` | Top game/tag cho Trung thành 1-3 game (16 CSV) |
| `d:\GR\User Segmentation\data\insights_1000games_tags\summary.json` | Tổng hợp tất cả cluster dạng JSON |
| `d:\GR\User Segmentation\data\user_features_1000games_2026-10-01.csv` | 64.127 user features (dedupe 52.608) |
| `d:\GR\User Segmentation\data\clusters_1000games_2026-10-01.csv` | Features + cluster_id (52.608 user) |
| `d:\GR\1000games_all.csv` | Metadata 489 game |
| `d:\GR\1000games_step3_insights.py` | Script build insights |

---

**Ngày tạo:** 2026-10-08
**Phương pháp:** Parse top_slugs (top 20) cho mỗi user, classify intent, tính PV & user count theo game/tag/genre
**Khoảng thời gian:** 2026-09-10 đến 2026-10-01 (22 ngày — 1000games mới tracking từ 2026-09-10)
**Site:** 1000games.io
**Coverage:** 49.050/52.608 user (93%) có `top_slugs` data trong chunks
