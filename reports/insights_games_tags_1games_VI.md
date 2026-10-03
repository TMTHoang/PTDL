# Game & Tag Insights cho 3 Phân Khúc Người Dùng 1games.io

**Site:** 1games.io
**Khoảng thời gian:** 28 ngày kết thúc ngày 1 tháng 10, 2026
**Phương pháp:** Phân tích `top_slugs` (top 20 slug theo page view) cho mỗi user, join với `games_meta_normalized.csv`
**Cohort:** user trưởng thành (lần đầu ≥28 ngày trước)
**Đối tượng đọc:** content team, game curator, marketing
**Ngày:** 2 tháng 10, 2026

---

## Cách đọc báo cáo này

Mỗi user trong 1games có một danh sách **top 20 slug** mà họ đã xem (kèm số page view trên slug đó). ClickHouse cắt ở 20 slug hàng đầu nên:
- Với user chỉ xem vài slug, ta thấy đủ
- Với Power user (xem hàng trăm slug khác nhau), ta chỉ thấy 20 slug phổ biến nhất của họ

Từ những slug đó, ta chia thành 4 loại:

| Loại | Cách nhận biết | Vai trò |
|---|---|---|
| `home` | slug rỗng (trang chủ) | vào nhưng không click |
| `category_browse` | slug `hot-games`, `shooting.games`, v.v. | duyệt category |
| `search` | slug bắt đầu bằng `search` | tìm kiếm |
| `direct_game` | khớp pattern `[a-z0-9]+(-[a-z0-9]+)+` **AND có trong `games_meta`** | vào thẳng game |

**Quan trọng:** tag/genre chỉ có cho slug thuộc loại `direct_game` VÀ có trong bảng `games_meta_normalized.csv`. Bảng này hiện có **886 / 1.851 slug** trong chunks → **~48% slug thiếu metadata**, chủ yếu là những game mà user click trực tiếp qua URL nhưng không đi qua trang category. Điều này ảnh hưởng nhiều nhất đến phân khúc Bounce (xem bên dưới).

---

## Phân khúc 🟡 Khách chơi thử (Casual browser)

- **Số user trong cluster:** 14.052 (43% mature users)
- **User có `top_slugs` data trong chunks:** 8.223 (58% coverage)
- **Phân bổ số game đã chơi:**

| Bucket | User |
|---|---:|
| 0 game | 124 |
| 1 game | 6.963 |
| 2–3 game | 4.334 |
| 4–7 game | 2.308 |
| 8+ game | 327 |

→ **99% user trong phân khúc này chơi 1–3 game**, với số đông nhất (50%) chỉ chơi đúng 1 game.

### Top 10 game theo lượt xem (PV)

| # | Slug | Tên | PV |
|---:|---|---|---:|
| 1 | challenge-rush | Challenge Rush | 2.811 |
| 2 | slope-2 | Slope 2 | 2.346 |
| 3 | wacky-flip | Wacky Flip | 1.874 |
| 4 | traffic-road | Traffic Road | 1.374 |
| 5 | orbit-kick | Orbit Kick | 965 |
| 6 | tap-road | Tap Road | 932 |
| 7 | undead-corridor | Undead Corridor | 880 |
| 8 | ragdoll-playground | Ragdoll Playground | 848 |
| 9 | pixel-path | Pixel Path | 712 |
| 10 | slope-rider | Slope Rider | 676 |

### Top 10 game theo số user đã chơi

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | slope-2 | Slope 2 | 1.257 |
| 2 | challenge-rush | Challenge Rush | 1.194 |
| 3 | wacky-flip | Wacky Flip | 969 |
| 4 | traffic-road | Traffic Road | 811 |
| 5 | orbit-kick | Orbit Kick | 579 |
| 6 | undead-corridor | Undead Corridor | 541 |
| 7 | tap-road | Tap Road | 502 |
| 8 | pixel-path | Pixel Path | 446 |
| 9 | ragdoll-playground | Ragdoll Playground | 428 |
| 10 | city-brawl | City Brawl | 415 |

→ Top game theo PV và theo user gần như giống nhau. **"Challenge Rush" và "Slope 2" là hai game hấp dẫn nhất** cho phân khúc này — chúng vừa giữ user (số user cao) vừa tạo nhiều lượt xem (PV cao). 7 trong 10 game ở đây thuộc dòng **slope/runner** — rất khớp với hành vi "chơi thử một game quen thuộc".

### Top 10 game mà user chọn làm "game yêu thích" (`top_game_slug`)

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | challenge-rush | Challenge Rush | 1.138 |
| 2 | slope-2 | Slope 2 | 1.005 |
| 3 | wacky-flip | Wacky Flip | 810 |
| 4 | traffic-road | Traffic Road | 561 |
| 5 | undead-corridor | Undead Corridor | 378 |

→ **~14% user trong cluster (1.138/8.223) chọn Challenge Rush làm game yêu thích.** Đây là game "anchor" cho phân khúc Casual browser.

*(Lưu ý: bảng này chỉ tính trên 8.223 user có `top_slugs` data trong chunks. Trên toàn bộ cluster 14.052 user, con số sẽ cao hơn — xem `clusters_1games_2026-10-01.csv` cột `top_game_slug` để có số liệu đầy đủ.)*

### Top 15 tag theo PV và theo user

| Tag | PV | User |
|---|---:|---:|
| arcade | 11.414 | 4.339 |
| skill | 10.626 | 4.201 |
| physics | 9.734 | 3.891 |
| fast-paced | 8.882 | 3.487 |
| avoid | 6.658 | 2.790 |
| action | 6.451 | 2.880 |
| sports | 5.713 | 2.539 |
| ball | 5.313 | 2.337 |
| platform | 5.201 | 2.343 |
| driving | 4.754 | 2.136 |
| running | 4.354 | 2.079 |
| adventure | 4.056 | 1.989 |
| slope | 3.588 | 1.585 |
| casual | 3.549 | 1.747 |
| ragdoll | 3.528 | 1.589 |

→ Bộ tag **arcade / skill / physics / fast-paced / avoid** chiếm thế thượng phong. Đây là bộ tag mô tả chính xác dòng game Casual browser ưa thích (slope/runner, hyper-casual skill). **~53% user trong cluster (4.339/8.223) đã chơi ít nhất 1 game có tag `arcade`** — cho thấy arcade không phải là dòng duy nhất nhưng chiếm đa số.

### Top genre theo PV và theo user

| Genre | PV | User |
|---|---:|---:|
| arcade | 8.560 | 3.526 |
| action | 6.451 | 2.880 |
| adventure | 3.562 | 1.780 |
| sports | 3.596 | 1.800 |
| platform | 3.147 | 1.386 |
| driving | 2.860 | 1.388 |
| clicker | 921 | 463 |
| casual | 686 | 376 |
| puzzle | 554 | 352 |
| shooting | 280 | 233 |

→ **43% user (3.526/8.223) đã chơi ít nhất 1 game arcade genre**, **35% đã chơi game action**. Clicker (463 user, 5,6%) là một phát hiện thú vị — game clicker/incremental thường chỉ cần 1 phiên chơi nên phù hợp với user "chơi thử rồi đi".

### Câu chuyện của phân khúc 🟡

Casual browser là phân khúc **rất đồng nhất về sở thích**: họ thích game arcade dạng slope/runner có tag `skill` + `physics` + `fast-paced`. **Challenge Rush** và **Slope 2** là hai game "neo" — phần lớn user trong cluster đều thử một trong hai game này.

Vì sở thích đồng nhất, **chiến lược tái kích hoạt cho phân khúc này rất rõ ràng**: push notification về game họ đã chơi (đặc biệt nếu game đó thuộc nhóm Challenge Rush / Slope 2 / Wacky Flip) có khả năng trúng cao hơn việc gợi ý game mới cùng genre.

---

## Phân khúc 🔴 Vào rồi thoát (Bounce / nav-only)

- **Số user trong cluster:** 7.070 (22% mature users)
- **User có `top_slugs` data trong chunks:** 4.037 (57% coverage)
- **Phân bổ số game đã chơi:**

| Bucket | User |
|---|---:|
| 0 game | 7.061 |
| 1 game | 5 |

→ **99,93% user trong phân khúc này không chơi game nào.** Chỉ có 9 user (0,07%) click vào đúng 1 game trong cả 28 ngày. Đây chính là bản chất của phân khúc: user đến, xem trang chủ, không thấy gì để click, rồi đi.

### Top game mà Bounce user click vào (rất hiếm)

Vì hầu như không có dữ liệu game cho phân khúc này, ta buộc phải dùng dữ liệu từ `top_game_slug` trong cluster CSV (cột `top_game_slug` trong bảng clusters) thay vì tổng PV.

| # | Slug | User đã chọn làm top_game |
|---:|---|---:|
| 1 | undead-invasion | 46 |
| 2 | crash-x | 39 |
| 3 | basketball-hit | 34 |
| 4 | flip-or-fail | 31 |
| 5 | tower-rise | 23 |
| 6 | cycle-racing-game | 20 |
| 7 | kickback-dash | 18 |
| 8 | 1-weapon-evolution-online | 13 |
| 9 | top-popular | 12 |
| 10 | mine-blade-online | 11 |

**Quan sát quan trọng:** Top 20 game mà Bounce user click vào **đều không có trong bảng `games_meta_normalized.csv`**. Đây là 577 user click vào game mà hệ thống tagging chưa bao phủ — họ vào 1games bằng URL trực tiếp (có thể từ Google, social, hay bookmark cũ), không qua category page. Vì game không có metadata, **ta không thể biết tag/genre của những game này**, và phân tích tag/genre cho phân khúc Bounce bị giới hạn nghiêm trọng.

### Top tag/genres cho Bounce (gần như rỗng)

| Tag | PV |
|---|---:|
| simulation | 3 |
| driving | 3 |
| collecting | 3 |
| drifting | 3 |
| weapon | 2 |

| Genre | User |
|---|---:|
| driving | 3 |
| shooting | 1 |
| action | 1 |
| casual | 1 |
| adventure | 1 |

→ Những con số này quá nhỏ để có ý nghĩa thống kê (3 user có tag `simulation`, 1 user có genre `shooting`). **Đây là hệ quả của việc 99,93% user trong cluster không chơi game nào.**

### Câu chuyện của phân khúc 🔴

Phân khúc Bounce là **phân khúc "trống" về nội dung game**. Đây không phải là vấn đề về sở thích mà là vấn đề về **khám phá**: user đã đến 1games (có ≥28 ngày lịch sử → đã từng quay lại), nhưng trang chủ không thuyết phục được họ click vào game nào.

Một số manh mối gián tiếp:
- **577 user click vào game "không có metadata"** — nghĩa là những user này đã thấy URL game ở đâu đó (Google search, social media, hay URL trực tiếp từ phiên trước) chứ không phải từ trang chủ 1games. Đây là manh mối quan trọng: **trang chủ 1games đang thất bại trong việc đề xuất game** — nhưng game đó vẫn được tìm thấy qua kênh khác.
- Nếu hệ thống tagging có metadata cho những game này, ta sẽ biết được user Bounce thích thể loại gì. Hiện tại ta chưa biết.

**Hệ quả chiến lược:** trước khi cải thiện trang chủ, đội content nên **ưu tiên backfill metadata cho top 50 game "Bounce-user-click"** để có data-driven hypothesis cho chiến lược "cải thiện trang chủ". Hiện tại ta đang mù về sở thích thực của phân khúc này.

---

## Phân khúc 🟢 Power user

- **Số user trong cluster:** 11.579 (35% mature users)
- **User có `top_slugs` data trong chunks:** 6.906 (60% coverage)
- **Phân bổ số game đã chơi:**

| Bucket | User |
|---|---:|
| 0 game | 8 |
| 1 game | 210 |
| 2–3 game | 752 |
| 4–7 game | 2.701 |
| 8+ game | 7.908 |

→ **68% Power user chơi 8+ game trong 28 ngày.** Đây là phân khúc "explorer" — chơi rất nhiều game, không trung thành với một game.

### Top 10 game theo lượt xem (PV)

| # | Slug | Tên | PV |
|---:|---|---|---:|
| 1 | slope-2 | Slope 2 | 18.827 |
| 2 | challenge-rush | Challenge Rush | 15.896 |
| 3 | wacky-flip | Wacky Flip | 10.374 |
| 4 | traffic-road | Traffic Road | 8.262 |
| 5 | orbit-kick | Orbit Kick | 7.092 |
| 6 | tap-road | Tap Road | 6.567 |
| 7 | slope-rider | Slope Rider | 5.539 |
| 8 | ragdoll-playground | Ragdoll Playground | 5.460 |
| 9 | undead-corridor | Undead Corridor | 5.160 |
| 10 | pixel-path | Pixel Path | 4.272 |

### Top 10 game theo số user đã chơi

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | slope-2 | Slope 2 | 2.855 |
| 2 | wacky-flip | Wacky Flip | 2.389 |
| 3 | traffic-road | Traffic Road | 2.203 |
| 4 | challenge-rush | Challenge Rush | 2.054 |
| 5 | orbit-kick | Orbit Kick | 1.896 |
| 6 | tap-road | Tap Road | 1.581 |
| 7 | pixel-path | Pixel Path | 1.497 |
| 8 | undead-corridor | Undead Corridor | 1.474 |
| 9 | city-brawl | City Brawl | 1.386 |
| 10 | brain-lines | Brain Lines | 1.218 |

→ **Slope 2** dẫn đầu với 2.855 user — chiếm 41% user có chunks data (2.855/6.906). Game này vừa giữ user (số user cao nhất) vừa tạo PV khổng lồ (18.827 PV, ~3× Wacky Flip ở vị trí 2 về PV). **6 trong 10 game ở đây thuộc dòng slope/runner** (slope-2, challenge-rush, traffic-road, tap-road, slope-rider, pixel-path) — cho thấy slope/runner là "nền tảng" của Power user.

### Top 10 game mà Power user chọn làm "game yêu thích"

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | slope-2 | Slope 2 | 1.234 |
| 2 | wacky-flip | Wacky Flip | 769 |
| 3 | challenge-rush | Challenge Rush | 605 |
| 4 | traffic-road | Traffic Road | 524 |
| 5 | orbit-kick | Orbit Kick | 469 |

→ **~18% Power user có chunks data (1.234/6.906) chọn Slope 2 làm game yêu thích.** Tuy nhiên, vì Power user chơi trung bình 10 game khác nhau, top_game_slug của họ ít "quyết định" hơn top_game_slug của Casual browser.

*(Lưu ý: bảng này chỉ tính trên 6.906 user có `top_slugs` data trong chunks. Trên toàn bộ cluster 11.579 user, con số sẽ cao hơn — xem `clusters_1games_2026-10-01.csv` cột `top_game_slug` để có số liệu đầy đủ.)*

### Top 15 tag theo PV và theo user

| Tag | PV | User |
|---|---:|---:|
| arcade | 79.932 | 6.505 |
| physics | 65.648 | 6.182 |
| skill | 63.697 | 6.229 |
| fast-paced | 56.201 | 5.530 |
| avoid | 47.285 | 5.516 |
| action | 40.543 | 5.361 |
| ball | 39.220 | 4.923 |
| sports | 35.796 | 5.112 |
| platform | 29.871 | 4.694 |
| running | 29.798 | 4.687 |
| slope | 29.628 | 2.812 |
| driving | 28.297 | 4.638 |
| adventure | 28.041 | 4.808 |
| casual | 26.104 | 4.714 |
| ragdoll | 21.706 | 3.700 |

→ So với Casual browser, Power user có **tỷ lệ user theo tag rất cao**: 94% (6.505/6.906) đã chơi ít nhất 1 game có tag `arcade`, 90% đã chơi game có tag `physics`. Tag `incremental` (20.456 PV) và `simulation` (19.739 PV) có mặt trong top 20 của Power user nhưng **gần như vắng mặt trong top 20 của Casual browser**. Power user chơi cả game simulation/incremental (idle/tycoon), một thể loại mà Casual browser hầu như không chạm vào.

### Top genre theo PV và theo user

| Genre | PV | User |
|---|---:|---:|
| arcade | 60.417 | 6.179 |
| action | 40.543 | 5.361 |
| adventure | 23.639 | 4.470 |
| sports | 22.195 | 4.168 |
| driving | 17.995 | 3.897 |
| platform | 17.326 | 2.516 |
| clicker | 6.449 | 1.429 |
| casual | 5.228 | 1.657 |
| puzzle | 4.867 | 1.863 |
| shooting | 1.564 | 1.024 |

→ Power user có **phân bố genre rộng hơn nhiều** so với Casual browser: 14 genre có >500 user (so với 10 ở Casual browser). Đáng chú ý: **puzzle (1.863 user), shooting (1.024 user), horror (546 user), survival (495 user), simulation (542 user)** đều có user đáng kể trong Power user. Trong khi đó Casual browser chỉ có 10 genre đạt mốc này và các genre "deep" như horror, simulation gần như không có user.

### Câu chuyện của phân khúc 🟢

Power user có ba đặc điểm chính:

1. **Slope/runner là nền tảng, không phải tất cả.** 6/10 game top PV là slope/runner, nhưng 68% Power user chơi 8+ game và tag diversity cao — họ chơi rất nhiều game ngoài dòng này.

2. **Sở thích trải rộng, không tập trung vào một tag.** Tag `incremental`, `simulation`, `puzzle`, `shooting`, `horror` đều có PV cao trong Power user nhưng không có trong top 15 của Casual browser.

3. **Có "game neo" cho hero bài.** Slope 2 là game được nhiều Power user chọn nhất (1.975 user), nhưng vì họ chơi 10+ game, đây không phải "loyalty to one game" — mà là "tất cả đều bắt đầu ở Slope 2 rồi lan sang game khác".

**Hệ quả chiến lược:**
- **Gợi ý cho Power user không nên giới hạn ở dòng slope/runner** — họ sẵn sàng thử game mọi thể loại. Một hệ thống recommendation đa dạng theo tag sẽ hiệu quả hơn "more like the one you played".
- **Slope 2 / Challenge Rush vẫn là "gateway" quan trọng** — nếu 1games thêm game mới cùng dòng này, Power user sẽ thử nhanh hơn Casual browser.

---

## So sánh nhanh giữa 3 phân khúc

| | Casual browser 🟡 | Bounce 🔴 | Power user 🟢 |
|---|---:|---:|---:|
| Top 1 game | Challenge Rush (1.138 user) | undead-invasion (46 user) | Slope 2 (1.234 user) |
| Top 2 game | Slope 2 (1.005 user) | crash-x (39 user) | Wacky Flip (769 user) |
| Top 1 tag (theo user) | arcade (4.339 user) | simulation (3 user) | arcade (6.505 user) |
| Top 1 genre (theo user) | arcade (3.526 user) | driving (3 user) | arcade (6.179 user) |
| Distinct games trung bình | ~2 | ~0 | ~10 |
| Tag diversity | ~12 tag | 0 | ~37 tag |
| Đặc điểm chung | slope/runner, 1–3 game | không chơi game | đa dạng, 8+ game |

---

## Phát hiện quan trọng: lỗ hổng metadata

Trong khi phân tích, ta phát hiện:

- **Có 1.851 slug unique trong chunks, nhưng chỉ 886 (48%) có trong `games_meta_normalized.csv`**
- **Tất cả 20 game "top" của phân khúc Bounce đều thiếu metadata** — đây là những game mà Bounce user click vào nhưng hệ thống chưa gắn tag/genre
- Tỷ lệ game thiếu metadata trong Casual browser và Power user thấp hơn nhiều vì những user đó chơi các game "phổ biến" (đã được tag đầy đủ)

**Hệ quả chiến lược:**
- Phân tích tag/genre cho phân khúc Bounce bị giới hạn nghiêm trọng
- Trước khi thiết kế chiến lược "cải thiện trang chủ cho Bounce user", đội content cần **backfill metadata cho top 50–100 game phổ biến mà Bounce user click vào**
- Một khi metadata có đủ, ta sẽ biết Bounce user thích thể loại gì khi họ *thực sự* click — và từ đó mới gợi ý cho họ trên trang chủ

---

## Câu hỏi mở cho team

1. **Bounce user đến 1games từ đâu?** Nếu họ click vào game "không có metadata", có thể họ đến từ Google search. Kiểm tra log referrer có thể cho thấy kênh acquisition của phân khúc này.

2. **Vì sao trang chủ không thuyết phục được Bounce user?** Có phải vì trang chủ hiển thị game "đại trà" mà họ không quan tâm? Cần xem lại trang chủ và đối chiếu với 50 game Bounce user click vào.

3. **Power user có nên được "thử thách" với game mới?** Vì họ chơi 8+ game và tag diversity cao, họ có thể là audience tốt nhất để test game mới. Đây là cơ hội A/B testing "early access".

---

## Tìm dữ liệu ở đâu

| File | Nội dung |
|---|---|
| `d:\GR\03_data\processed\user_features\insights_games_tags\cluster0_top_games_by_pv.csv` | Top game theo PV — Casual browser |
| `d:\GR\03_data\processed\user_features\insights_games_tags\cluster0_top_games_by_users.csv` | Top game theo user — Casual browser |
| `d:\GR\03_data\processed\user_features\insights_games_tags\cluster0_top_tags_by_pv.csv` | Top tag theo PV — Casual browser |
| `d:\GR\03_data\processed\user_features\insights_games_tags\cluster0_top_tags_by_users.csv` | Top tag theo user — Casual browser |
| `d:\GR\03_data\processed\user_features\insights_games_tags\cluster0_top_genres_by_pv.csv` | Top genre theo PV — Casual browser |
| `d:\GR\03_data\processed\user_features\insights_games_tags\cluster0_top_genres_by_users.csv` | Top genre theo user — Casual browser |
| `d:\GR\03_data\processed\user_features\insights_games_tags\cluster0_top_game_count.csv` | Top game theo `top_game_slug` — Casual browser |
| `d:\GR\03_data\processed\user_features\insights_games_tags\cluster0_top_tag_count.csv` | Top dominant_tag — Casual browser |
| `d:\GR\03_data\processed\user_features\insights_games_tags\cluster0_top_genre_count.csv` | Top dominant_genre — Casual browser |
| `d:\GR\03_data\processed\user_features\insights_games_tags\cluster1_*.csv` | Tương tự cho Bounce |
| `d:\GR\03_data\processed\user_features\insights_games_tags\cluster2_*.csv` | Tương tự cho Power user |
| `d:\GR\03_data\processed\user_features\insights_games_tags\summary.json` | Toàn bộ summary dạng JSON |
| `d:\GR\03_data\processed\games_meta\games_meta_normalized.csv` | Bảng metadata 886 game |
| `d:\GR\03_data\processed\user_features\clusters_1games_2026-10-01.csv` | Bảng cluster gốc (32.701 user) |
| `d:\GR\03_data\processed\user_features\insights_games_tags\pretty_summary.txt` | In summary ra dạng text |
| `d:\GR\03_data\processed\user_features\build_game_tag_insights.py` | Script build insights |

---

**Ngày tạo:** 2026-10-02
**Phương pháp:** Parse top_slugs (top 20) cho mỗi user, classify intent, tính PV & user count theo game/tag/genres
**Khoảng thời gian:** 2026-09-03 đến 2026-10-01 (28 ngày)
**Site:** 1games.io
**Hạn chế:** chỉ 19,166/32.701 user (58%) có `top_slugs` data trong chunks