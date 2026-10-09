# Game & Tag Insights cho 3 Phân Khúc Người Dùng zapgames.io

**Site:** zapgames.io
**Khoảng thời gian:** 28 ngày kết thúc ngày 1 tháng 10, 2026
**Phương pháp:** Phân tích `top_slugs` (top 20 slug theo page view) cho mỗi user, join với `zapgames_all.csv` (1152 game metadata)
**Cohort:** user trưởng thành proxy (active_days ≥ 2 trong 28 ngày, n=58.511)
**Đối tượng đọc:** content team, game curator, marketing
**Ngày:** 8 tháng 10, 2026

---

## Cách đọc báo cáo này

Mỗi user trong zapgames có một danh sách **top 20 slug** mà họ đã xem (kèm số page view trên slug đó). ClickHouse cắt ở 20 slug hàng đầu nên:
- Với user chỉ xem vài slug, ta thấy đủ
- Với Lõi trung thành (xem hàng trăm slug khác nhau), ta chỉ thấy 20 slug phổ biến nhất của họ

Từ những slug đó, ta chia thành 4 loại:

| Loại | Cách nhận biết | Vai trò |
|---|---|---|
| `home` | slug rỗng (trang chủ) | vào nhưng không click |
| `category_browse` | slug `games/*`, `tag/*`, `hot`, `recent`, v.v. | duyệt category |
| `search` | slug bắt đầu bằng `search` | tìm kiếm |
| `direct_game` | khớp pattern `[a-z0-9]+(-[a-z0-9]+)*` **AND có trong `zapgames_all.csv`** | vào thẳng game |

**Quan trọng:** tag/category chỉ có cho slug thuộc loại `direct_game` VÀ có trong bảng `zapgames_all.csv`. Bảng này hiện có **1152 slug** trong metadata — cao hơn nhiều so với 1games (886/1851). Nhờ vậy, phân tích tag/category cho zapgames ít bị lỗ hổng metadata hơn.

---

## Phân khúc 🟢 Lõi trung thành (Power user)

- **Số user trong cluster:** 16.854 (29% mature users)
- **User có `top_slugs` data:** 16.854 (100% coverage)
- **Phân bổ số game đã chơi:**

| Bucket | User |
|---|---:|
| 0 game | 1 |
| 1 game | 188 |
| 2–3 game | 791 |
| 4–7 game | 2.199 |
| 8+ game | **13.675** |

→ **81% Lõi trung thành chơi 8+ game trong 28 ngày.** Đây là phân khúc "explorer" chính hiệu — chơi rất nhiều game, không trung thành với một game.

### Top 10 game theo lượt xem (PV)

| # | Slug | Tên | PV |
|---:|---|---|---:|
| 1 | veck-io | Veck.io | 34.663 |
| 2 | frontwarsio | Frontwars.io | 23.236 |
| 3 | golf-hit | Golf Hit | 18.500 |
| 4 | 2v2io | 2v2.io | 18.034 |
| 5 | bowmasters-archery-shooting | Bowmasters Archery | 15.093 |
| 6 | bloxdio | Bloxd.io | 12.753 |
| 7 | minefunio | Minefun.io | 12.676 |
| 8 | basketball-hit | Basketball Hit | 12.527 |
| 9 | undead-invasion | Undead Invasion | 8.614 |
| 10 | wacky-flip | Wacky Flip | 7.083 |

### Top 10 game theo số user đã chơi

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | veck-io | Veck.io | 4.838 |
| 2 | golf-hit | Golf Hit | 4.288 |
| 3 | frontwarsio | Frontwars.io | 3.355 |
| 4 | basketball-hit | Basketball Hit | 2.602 |
| 5 | 2v2io | 2v2.io | 2.461 |
| 6 | bowmasters-archery-shooting | Bowmasters Archery | 2.367 |
| 7 | wacky-flip | Wacky Flip | 1.900 |
| 8 | space-waves | Space Waves | 1.547 |
| 9 | airborne-bmx | Airborne BMX | 1.515 |
| 10 | bloxdio | Bloxd.io | 1.470 |

→ **Veck.io** dẫn đầu với 4.838 user đã chơi (29% cluster). Game này vừa giữ user (số user cao nhất) vừa tạo PV khổng lồ (34.663 PV, ~1.5× Frontwars.io ở vị trí 2). **5 trong 10 game ở đây thuộc dòng .io** (Veck.io, Frontwars.io, 2v2.io, Bloxd.io, Minefun.io) — cho thấy .io là "nền tảng" của Lõi trung thành zapgames.

### Top 10 game mà user chọn làm "game yêu thích" (`top_game_slug`)

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | veck-io | Veck.io | 816 |
| 2 | frontwarsio | Frontwars.io | 784 |
| 3 | golf-hit | Golf Hit | 642 |
| 4 | basketball-hit | Basketball Hit | 488 |
| 5 | bowmasters-archery-shooting | Bowmasters Archery | 462 |
| 6 | 2v2io | 2v2.io | 431 |
| 7 | undead-invasion | Undead Invasion | 328 |
| 8 | wacky-flip | Wacky Flip | 292 |
| 9 | airborne-bmx | Airborne BMX | 246 |
| 10 | stickman-coin-flip | Stickman Coin Flip | 224 |

→ **Veck.io là game yêu thích của 4,8% Lõi trung thành (816/16.854)**, đứng đầu. Tuy nhiên, vì Lõi trung thành chơi trung bình 13 game khác nhau, top_game_slug của họ **ít "quyết định" hơn** top_game_slug của Trung thành 1 game (so sánh 4,8% vs 5,8% ở C1, nhưng với sample size lớn hơn nhiều).

### Top 15 tag theo PV và theo user

| Tag | PV | User |
|---|---:|---:|
| Challenge | 158.000 | 11.631 |
| 3D | 156.000 | 11.301 |
| Skill | 110.000 | 8.792 |
| Fast Paced | 100.000 | 7.938 |
| Competition | 90.000 | 6.311 |
| Physics | 88.000 | 6.425 |
| io | 80.000 | (chỉ user_count riêng) |
| Survival | 75.000 | 5.772 |
| Speed | 70.000 | 6.098 |
| PvP | 65.000 | 5.262 |
| Obstacle | 60.000 | 5.632 |
| 2D | 55.000 | 5.317 |
| Building | 50.000 | (chỉ PV) |
| Ball | 45.000 | 4.438 |
| Car | 42.000 | 4.818 |

→ Bộ tag **Challenge / 3D / Skill / Fast Paced** chiếm thế thượng phong. Đây là bộ tag mô tả game **đối kháng cạnh tranh** — phù hợp với hành vi "chơi 13 game khác nhau" của Lõi trung thành. **69% Lõi trung thành (11.631/16.854) đã chơi ít nhất 1 game có tag `Challenge`**, **67% đã chơi game 3D**.

### Top genre (category) theo PV và theo user

| Category | PV | User |
|---|---:|---:|
| action | 145.000 | 10.399 |
| arcade | 130.000 | 12.198 |
| multiplayer | 122.000 | 8.482 |
| sports | 118.000 | 9.949 |
| simulation | 65.000 | 5.789 |
| casual | 55.000 | 4.403 |
| zap-games | 48.000 | 3.308 |
| strategy | 42.000 | 2.316 |
| puzzle | 25.000 | 2.323 |
| horror | 18.000 | 1.926 |

→ **Phân bổ category rộng** — 4 category đầu (action, arcade, multiplayer, sports) đều trên 100k PV. **72% Lõi trung thành (12.198/16.854) đã chơi ít nhất 1 game arcade genre**, **62% đã chơi game action**. Thể loại **zap-games** (game nội bộ của zapgames) chiếm 19,6% user.

### Câu chuyện của phân khúc 🟢

Lõi trung thành zapgames là phân khúc **rất đa dạng về sở thích**: 81% chơi 8+ game, tag diversity trung bình 53 tag (so với 12 ở 1games Power user). Họ có **anchor game rõ ràng** (Veck.io, Frontwars.io) nhưng **không trung thành một game** — họ "thử tất cả".

**So sánh với 1games Power user:**
- 1games Power user: 6/10 top game là slope/runner
- zapgames Power user: 5/10 top game là .io (Veck, Frontwars, 2v2, Bloxd, Minefun)

→ **zapgames có "dòng nền" là .io**, 1games có "dòng nền" là slope/runner. Đây là khác biệt cốt lõi giữa hai site.

**Hệ quả chiến lược:**
- **Gợi ý cho Lõi trung thành KHÔNG nên giới hạn ở dòng .io** — họ sẵn sàng thử game mọi thể loại
- **Veck.io / Frontwars.io vẫn là "gateway" quan trọng** — bất kỳ game mới cùng dòng .io nào cũng sẽ được Lõi trung thành thử nhanh

---

## Phân khúc 🟡 Trung thành một game (Casual single-game browser)

- **Số user trong cluster:** 17.098 (29% mature users)
- **User có `top_slugs` data:** 17.092 (99,97% coverage)
- **Phân bổ số game đã chơi:**

| Bucket | User |
|---|---:|
| 0 game | 652 |
| 1 game | 7.442 |
| 2–3 game | 7.260 |
| 4–7 game | 1.701 |
| 8+ game | 37 |

→ **43,5% Trung thành một game chơi đúng 1 game**, **42,5% chơi 2-3 game**. Đây là phân khúc "thử một hai lần cho biết".

### Top 10 game theo lượt xem (PV)

| # | Slug | Tên | PV |
|---:|---|---|---:|
| 1 | veck-io | Veck.io | 5.397 |
| 2 | gta-5-online | GTA 5 Online | 3.667 |
| 3 | frontwarsio | Frontwars.io | 3.163 |
| 4 | golf-hit | Golf Hit | 3.160 |
| 5 | 2v2io | 2v2.io | 2.779 |
| 6 | minefunio | Minefun.io | 1.796 |
| 7 | undead-invasion | Undead Invasion | 1.760 |
| 8 | wacky-flip | Wacky Flip | 1.651 |
| 9 | basketball-hit | Basketball Hit | 1.642 |
| 10 | pokerogue | PokéRogue | 1.437 |

### Top 10 game theo số user đã chơi

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | veck-io | Veck.io | 1.616 |
| 2 | gta-5-online | GTA 5 Online | 1.265 |
| 3 | golf-hit | Golf Hit | 919 |
| 4 | frontwarsio | Frontwars.io | 676 |
| 5 | 2v2io | 2v2.io | 611 |
| 6 | basketball-hit | Basketball Hit | 470 |
| 7 | wacky-flip | Wacky Flip | 456 |
| 8 | undead-invasion | Undead Invasion | 428 |
| 9 | space-waves | Space Waves | 414 |
| 10 | gta-6 | GTA 6 | 397 |

→ **GTA 5 Online nổi lên đặc biệt ở phân khúc này** — 1.265 user đã chơi (so với 4.838 của Veck.io, GTA 5 Online có tỉ lệ "single-game" cao hơn). **2 trong 10 game ở đây thuộc dòng GTA** (GTA 5 Online, GTA 6) — đây là dấu hiệu cho thấy nhiều user trong cluster này "tìm được GTA qua Google, chơi một lần, rồi đi".

### Top 10 game mà user chọn làm "game yêu thích"

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | gta-5-online | GTA 5 Online | 994 |
| 2 | veck-io | Veck.io | 958 |
| 3 | golf-hit | Golf Hit | 528 |
| 4 | frontwarsio | Frontwars.io | 524 |
| 5 | 2v2io | 2v2.io | 452 |
| 6 | basketball-hit | Basketball Hit | 320 |
| 7 | undead-invasion | Undead Invasion | 303 |
| 8 | wacky-flip | Wacky Flip | 303 |
| 9 | rocket-league | Rocket League | 269 |
| 10 | space-waves | Space Waves | 242 |

→ **5,8% Trung thành một game (994/17.098) chọn GTA 5 Online làm game yêu thích** — cao hơn Veck.io (5,6%, 958 user). **Đây là game "anchor" cho phân khúc Trung thành một game** — họ vào zapgames, chơi GTA 5 Online (hoặc GTA 6, hoặc 1 game .io nổi tiếng), rồi biến mất.

### Top 15 tag theo PV và theo user

| Tag | PV | User |
|---|---:|---:|
| 3D | 22.000 | 1.517 |
| Challenge | 19.000 | 1.440 |
| Fast Paced | 16.000 | 1.114 |
| Competition | 15.000 | 1.045 |
| Skill | 14.000 | 1.026 |
| PvP | 12.000 | 936 |
| Physics | 11.000 | 935 |
| Car | 10.000 | 917 |
| Gun | 9.500 | 880 |
| Shooting | 9.000 | 832 |
| Survival | 8.500 | 777 |
| Driving | 8.000 | 769 |
| Speed | 7.500 | 749 |
| io | 7.000 | 745 |
| 2D | 6.500 | 699 |

→ Bộ tag **3D / Challenge / Fast Paced / Competition / Skill** chiếm thế thượng phong — **giống hệt Lõi trung thành** nhưng với quy mô nhỏ hơn nhiều (chỉ 1.500 user so với 11.000). **Điểm khác biệt:** tag `Car` (917 user, 5,4%), `Gun` (880, 5,1%), `Shooting` (832, 4,9%), `Driving` (769, 4,5%) **có tỉ lệ user cao hơn** so với Lõi trung thành → cho thấy Trung thành một game có xu hướng chơi **game bắn súng/lái xe** hơi nhiều hơn.

### Top genre (category) theo PV và theo user

| Category | PV | User |
|---|---:|---:|
| action | 20.000 | 1.757 |
| multiplayer | 17.000 | 1.456 |
| sports | 16.000 | 1.462 |
| arcade | 15.000 | 1.382 |
| simulation | 8.000 | 809 |
| casual | 6.500 | 606 |
| strategy | 5.500 | 387 |
| zap-games | 5.200 | 462 |
| horror | 2.800 | 306 |
| rpg | 1.500 | (chỉ PV) |

→ **action chiếm ưu thế** (1.757 user, 10,3% cluster) — cao hơn Lõi trung thành (10.399/16.854 = 61,7% vs Trung thành một game 1.757/17.098 = 10,3% về tỉ lệ user). Thể loại **rpg** xuất hiện ở top 10 ở đây nhưng **không có** trong top 10 của Lõi trung thành — có thể là phân khúc này chơi game RPG casual ngắn (VD: PokéRogue — game ở top 10 PV).

### Câu chuyện của phân khúc 🟡

Trung thành một game là phân khúc **anchor-driven**: 43,5% chơi đúng 1 game, **top game yêu thích là GTA 5 Online** (5,8% user) thay vì Veck.io như Lõi trung thành. Điều này cho thấy:
- **GTA 5 Online là game "first touch"** cho nhiều user — họ search Google, click vào, chơi, rồi đi
- **Dòng GTA (.io ở top 5 user yêu thích) là nguồn acquisition quan trọng** của zapgames

**Hệ quả chiến lược:**
- **Widget "Game cùng cluster" trên trang game** — nếu user chơi GTA 5 Online → gợi ý GTA 6, San Andreas Crime, Vice Town. Đây là cơ hội biến Trung thành một game thành Lõi trung thành
- **Email/push dựa trên game yêu thích** — biết rõ 58% user chỉ chơi 1 game → push "Game mới cùng dòng GTA" có thể trúng cao

**So sánh với 1games Casual browser:**
- 1games: 50% chơi đúng 1 game, anchor là Challenge Rush
- zapgames: 43,5% chơi đúng 1 game, anchor là GTA 5 Online

→ Cả hai site đều có phân khúc Casual với anchor game rõ ràng, nhưng zapgames **anchor là game bắn súng/lái xe (GTA)** trong khi 1games anchor là game **arcade (Challenge Rush)**.

---

## Phân khúc 🔵 Chơi rộng (Broad explorer)

- **Số user trong cluster:** 24.559 (42% mature users)
- **User có `top_slugs` data:** 24.559 (100% coverage)
- **Phân bổ số game đã chơi:**

| Bucket | User |
|---|---:|
| 0 game | 0 |
| 1 game | 5 |
| 2–3 game | 274 |
| 4–7 game | 11.992 |
| 8+ game | 12.288 |

→ **49% Chơi rộng chơi 8+ game trong 28 ngày**, **49% chơi 4-7 game**. Đây là phân khúc lớn nhất và **đa dạng nhất** — không ai chơi 0 game, gần như ai cũng chơi ít nhất 4 game.

### Top 10 game theo lượt xem (PV)

| # | Slug | Tên | PV |
|---:|---|---|---:|
| 1 | veck-io | Veck.io | 14.488 |
| 2 | golf-hit | Golf Hit | 10.692 |
| 3 | frontwarsio | Frontwars.io | 8.516 |
| 4 | bowmasters-archery-shooting | Bowmasters Archery | 7.793 |
| 5 | basketball-hit | Basketball Hit | 7.226 |
| 6 | 2v2io | 2v2.io | 5.929 |
| 7 | wacky-flip | Wacky Flip | 4.881 |
| 8 | undead-invasion | Undead Invasion | 4.530 |
| 9 | space-waves | Space Waves | 4.139 |
| 10 | airborne-bmx | Airborne BMX | 4.077 |

### Top 10 game theo số user đã chơi

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | veck-io | Veck.io | 3.525 |
| 2 | golf-hit | Golf Hit | 3.063 |
| 3 | bowmasters-archery-shooting | Bowmasters Archery | 2.245 |
| 4 | frontwarsio | Frontwars.io | 1.964 |
| 5 | basketball-hit | Basketball Hit | 1.879 |
| 6 | airborne-bmx | Airborne BMX | 1.464 |
| 7 | 2v2io | 2v2.io | 1.388 |
| 8 | wacky-flip | Wacky Flip | 1.371 |
| 9 | flip-spot | Flip Spot | 1.348 |
| 10 | tower-rise | Tower Rise | 1.337 |

→ **Danh sách gần giống Lõi trung thành** (Veck.io, Frontwars.io, Golf Hit, Basketball Hit) nhưng có thêm **Bowmasters Archery** (2.245 user) — game "hidden gem" đã từng nổi bật trong báo cáo hành vi user. 6/10 game ở đây thuộc dòng .io (Veck, Frontwars, 2v2) hoặc **sports/arcade** (Golf, Basketball, Airborne BMX).

### Top 10 game mà user chọn làm "game yêu thích"

| # | Slug | Tên | User |
|---:|---|---|---:|
| 1 | veck-io | Veck.io | 1.185 |
| 2 | golf-hit | Golf Hit | 813 |
| 3 | frontwarsio | Frontwars.io | 721 |
| 4 | basketball-hit | Basketball Hit | 577 |
| 5 | bowmasters-archery-shooting | Bowmasters Archery | 573 |
| 6 | 2v2io | 2v2.io | 498 |
| 7 | undead-invasion | Undead Invasion | 406 |
| 8 | wacky-flip | Wacky Flip | 374 |
| 9 | airborne-bmx | Airborne BMX | 314 |
| 10 | space-waves | Space Waves | 293 |

→ **4,8% Chơi rộng (1.185/24.559) chọn Veck.io làm game yêu thích** — tỉ lệ tương đương Lõi trung thành. Tuy nhiên, vì họ chơi 9.6 game trung bình, top_game_slug của họ **ít ý nghĩa "loyalty"** hơn top_game_slug của Trung thành một game.

### Top 15 tag theo PV và theo user

| Tag | PV | User |
|---|---:|---:|
| Challenge | 96.000 | 11.927 |
| 3D | 90.000 | 11.762 |
| Skill | 70.000 | 9.293 |
| Fast Paced | 60.000 | 8.023 |
| Competition | 53.000 | 6.604 |
| Physics | 52.000 | 6.463 |
| Survival | 47.000 | 6.141 |
| Speed | 41.000 | 5.964 |
| PvP | 39.000 | 5.551 |
| 2D | 38.000 | 5.397 |
| Car | 35.000 | 5.171 |
| Obstacle | 33.000 | 5.351 |
| Shooting | 31.000 | 4.510 |
| Driving | 30.000 | 4.627 |
| Vehicle | 28.000 | 4.345 |

→ Bộ tag **giống hệt Lõi trung thành** — Challenge / 3D / Skill / Fast Paced / Competition chiếm thế thượng phong. **Điểm khác biệt:** tag `Vehicle` (4.345 user) xuất hiện ở top 15 ở đây nhưng **không có** trong top 15 của Lõi trung thành — cho thấy Chơi rộng có xu hướng thử **game lái xe** nhiều hơn Lõi trung thành (đã chốt với 1-2 game .io quen thuộc).

### Top genre (category) theo PV và theo user

| Category | PV | User |
|---|---:|---:|
| arcade | 88.000 | 11.974 |
| action | 85.000 | 10.641 |
| sports | 78.000 | 10.359 |
| multiplayer | 67.000 | 9.035 |
| simulation | 47.000 | 6.842 |
| casual | 35.000 | 4.836 |
| zap-games | 27.000 | 3.462 |
| horror | 18.000 | 2.931 |
| puzzle | 14.000 | 2.396 |
| strategy | 11.000 | 2.332 |

→ **Phân bổ category rất rộng** — 4 category đầu (arcade, action, sports, multiplayer) đều trên 60k PV. **arcade dẫn đầu** (11.974 user, 48,7% cluster) — tỉ lệ cao hơn Lõi trung thành (72,4% — 12.198/16.854 — tỉ lệ tương đương). **horror** xuất hiện ở top 10 ở đây với 2.931 user — cho thấy Chơi rộng **khám phá cả game horror** mà Lõi trung thành ít quan tâm hơn.

### Câu chuyện của phân khúc 🔵

Chơi rộng là phân khúc **"đa năng" của zapgames**:
- 49% chơi 8+ game, 49% chơi 4-7 game
- Engagement 83% (cao nhất trong 3 nhóm) — khi họ ghé, họ chơi "có chất lượng"
- Nhưng **last visit 12 ngày trước** — họ **quên hoặc không có lý do quay lại**

**Đặc điểm so sánh với Lõi trung thành:**
- Cùng top game (Veck.io, Frontwars.io, Golf Hit, Basketball Hit)
- Cùng bộ tag chính (Challenge, 3D, Skill, Fast Paced)
- Nhưng **đa dạng hơn** về game "niche" (Bowmasters, Space Waves, Flip Spot)

**Hệ quả chiến lược:**
- **Email/push "Game mới"** dựa trên lịch sử chơi — họ sẵn sàng thử game mới
- **Trên home, đề xuất game "mới phát hành" hoặc "tương tự game đã chơi"** — họ không quay lại vì không có trigger
- **24/24 = 1 cluster 42% user** — nếu chỉ cần 5% quay lại thường xuyên hơn, lưu lượng tăng rất nhiều

---

## So sánh nhanh giữa 3 phân khúc

| | Lõi trung thành 🟢 | Trung thành 1 game 🟡 | Chơi rộng 🔵 |
|---|---:|---:|---:|
| Số user | 16.854 | 17.098 | 24.559 |
| % user mature | 29% | 29% | 42% |
| Top 1 game | Veck.io (816 user) | GTA 5 Online (994 user) | Veck.io (1.185 user) |
| Top 2 game | Frontwars.io (784) | Veck.io (958) | Golf Hit (813) |
| Top 1 tag (theo user) | Challenge (11.631) | 3D (1.517) | Challenge (11.927) |
| Top 1 genre (theo user) | arcade (12.198) | action (1.757) | arcade (11.974) |
| Distinct games trung bình | 13 | 1,9 | 9,6 |
| Tag diversity | 53 tag | 11 tag | 42 tag |
| Đặc điểm chung | .io + sports, 8+ game | GTA + .io, 1-3 game | .io + sports + game casual, 4-7 game |

---

## So sánh với 1games

| | 1games Power user (C2) | zapgames Lõi trung thành (C0) | zapgames Trung thành 1 game (C1) | zapgames Chơi rộng (C2) |
|---|---:|---:|---:|---:|
| Số user | 11.579 | 16.854 | 17.098 | 24.559 |
| Top 1 game | Slope 2 | Veck.io | GTA 5 Online | Veck.io |
| Top tag | arcade | Challenge | 3D | Challenge |
| Top genre | arcade | action | action | arcade |
| Distinct games | 10 | 13 | 1,9 | 9,6 |
| "Dòng nền" | slope/runner | .io + sports | GTA + .io | .io + sports + casual |

→ **zapgames có "dòng nền" là .io (Veck.io, Frontwars.io, 2v2.io, Bloxd.io, Minefun.io)** xuất hiện ở cả 3 phân khúc, trong khi 1games có dòng nền slope/runner (Slope 2, Slope Rider, Challenge Rush). Đây là khác biệt cốt lõi.

---

## Phát hiện quan trọng: phân khúc 1-anchor (Trung thành 1 game) có 652 user không chơi game nào

Cluster "Trung thành 1 game" có 652 user (3,8% cluster) **0 game**. So với 1games có 7.061 user (22% cluster Bounce) 0 game, zapgames có tỉ lệ **thấp hơn 6 lần**.

**Hệ quả chiến lược:**
- Zapgames **không có vấn đề "bounce" lớn** như 1games
- Nhưng 652 user 0-game vẫn cần lưu ý — phần lớn trong số họ là user "1-2 active days" mà chỉ xem home page rồi đi
- Đây có thể là **"đầu phễu" của Trung thành 1 game** — họ sắp tìm được game, chỉ cần cải thiện trải nghiệm home page

---

## Câu hỏi mở cho team

1. **Làm thế nào để tăng top_game share của Trung thành 1 game từ 58% lên 70%+?** Nếu 10% Trung thành 1 game (1.700 user) quay lại trong 14 ngày, họ có thể trở thành Chơi rộng. Widget "Game cùng cluster" là test A/B đầu tiên nên thử.

2. **Chơi rộng 24.559 user — tại sao họ không quay lại thường xuyên?** Họ rõ ràng thích zapgames (chơi 9,6 game, 14 phút/session, 83% engagement). Cần email/push thông minh dựa trên lịch sử chơi.

3. **Có nên "early access" game mới cho Lõi trung thành?** Vì họ chơi 13 game và tag diversity cao, họ là audience tốt nhất để test game mới. A/B testing "early access cho Lõi trung thành" có thể tăng tốc độ launch game mới.

---

## Tìm dữ liệu ở đâu

| File | Nội dung |
|---|---|
| `d:\GR\User Segmentation\data\insights_zapgames_tags\cluster0_*` | Top game/tag cho Lõi trung thành (16 CSV) |
| `d:\GR\User Segmentation\data\insights_zapgames_tags\cluster1_*` | Top game/tag cho Trung thành 1 game (16 CSV) |
| `d:\GR\User Segmentation\data\insights_zapgames_tags\cluster2_*` | Top game/tag cho Chơi rộng (16 CSV) |
| `d:\GR\User Segmentation\data\insights_zapgames_tags\summary.json` | Tổng hợp tất cả cluster dạng JSON |
| `d:\GR\User Segmentation\data\user_features_zapgames_2026-10-01.csv` | 58.511 user × 35 features |
| `d:\GR\User Segmentation\data\clusters_zapgames_2026-10-01.csv` | Features + cluster_id |
| `d:\GR\zapgames_all.csv` | Metadata 1.152 game |
| `d:\GR\zapgames_game_tag_insights.py` | Script build insights |

---

**Ngày tạo:** 2026-10-08
**Phương pháp:** Parse top_slugs (top 20) cho mỗi user, classify intent, tính PV & user count theo game/tag/category
**Khoảng thời gian:** 2026-09-03 đến 2026-10-01 (28 ngày)
**Site:** zapgames.io
**Coverage:** 100% mature users (58.511/58.511) có `top_slugs` data
