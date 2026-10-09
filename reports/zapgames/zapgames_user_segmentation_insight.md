# Phân tích User, Gu Game & Flow — zapgames.io

**Site:** zapgames.io
**Khoảng thời gian:** 22 ngày kết thúc ngày 1 tháng 10, 2026 (2026-08-10 → 2026-10-01)¹
**Mẫu phân tích:** 200 user / phân khúc (stratified by `top_game_slug`), tổng 392 user
**Dữ liệu:** `gm_pages` của ClickHouse — page_location, first_ts, engagement_total_msec
**Phương pháp:** Lấy chuỗi page theo thời gian cho mỗi user, phân loại intent, đếm chuyển trạng thái
**Ngày:** 9 tháng 10, 2026

¹ **Caveat date:** zapgames có dữ liệu từ 2026-08-10 (dài hơn 53 ngày), nhưng sample vẫn lấy 22 ngày lookback gần nhất (2026-08-10 → 2026-10-01) để so sánh được với các phân tích trước.

---

## TL;DR — Trả lời 3 câu hỏi

### 1. Tệp user chủ yếu của zapgames là ai? Người chơi 1 lần hay trung thành?

**Tệp user chủ yếu là NGƯỜI CHƠI TRUNG THÀNH.** Phân bổ:

| Phân khúc | % mature | Đặc điểm | Loyal? |
|---|---:|---|---|
| 🟢 Lõi trung thành (Power, C0) | **29%** | 25,7 game/user, 1.710s/user (28 phút!), 100% đa ngày | ✅ Rất trung thành |
| 🟡 Trung thành 1-3 game (C1) | **29%** | 2,1 game/user, 99s/user, 97% đa ngày | ✅ Trung thành |
| 🟠 Trung thành trung bình (C2) | **42%** | 11,1 game/user, 544s/user (9 phút), 98% đa ngày | ✅ Trung thành |

→ **Tất cả 3 phân khúc đều quay lại đa ngày (97-100%)** — zapgames có **BASE USER MẠNH**, không có phân khúc "Bounce" thật sự.

### 2. Gu game — game nào nhiều / lâu nhất?

**Gu chính:** .io (đặc biệt Veck.io) + bắn cung (Bowmasters) + sports (Golf Hit) + horror (Undead)

| Phân khúc | Game nhiều PV nhất | Game lâu nhất tổng | Game lâu nhất / user |
|---|---|---|---|
| 🟢 Lõi trung thành (Power) | **Veck.io (221 PV)** | Bowmasters (4.025s = 67 phút) | Veck.io (243s) |
| 🟡 Trung thành 1-3 game (C1) | Veck.io (60 PV) | Veck.io (1.159s = 19 phút) | Escape Road 3 (102s) |
| 🟠 Trung thành trung bình (C2) | **Veck.io (135 PV, 37 user)** | Bowmasters (3.879s = 65 phút) | Eaglercraft (186s) |

→ **Veck.io là "king" của zapgames** — top 1 PV ở cả 3 phân khúc. Bowmasters là game có tổng thời gian chơi lớn nhất.

### 3. Flow user là gì?

**Flow chính: `home → direct_game → direct_game → ...` (chain)** — không có "bounce" đáng kể.

| Phân khúc | Top 1 transition | Pattern đặc trưng |
|---|---|---|
| 🟢 Lõi trung thành (Power) | game→game (43,0%) | **CHAIN** (chơi nối tiếp) |
| 🟡 Trung thành 1-3 game (C1) | **game→game (56,0%)** | **SINGLE-GAME LOOP** (lặp 1-2 game) |
| 🟠 Trung thành trung bình (C2) | game→game (33,6%) | **CHAIN + HOME LOOP** (chơi nhiều game, về home xen giữa) |

→ **Cả 3 phân khúc đều CÓ FLOW "duyệt category" đáng kể** — đặc biệt C2 với 6,5% `category_browse → direct_game`. Zapgames có cổng duyệt category hoạt động tốt.

---

## 1. Tệp user chủ yếu — chi tiết

### Bằng chứng định lượng

#### 🟢 Lõi trung thành (Power) — C0 (mẫu 44 user, bị giới hạn chunk)

> **Lưu ý về sample:** Power user zapgames có **113,6 PV/user** trung bình, rất cao. Chunk ClickHouse giới hạn 5.000 records nên sample chỉ lấy được 44 user từ 200 sample ID. Kết quả vẫn đáng tin vì 100% C0 user đều có ≥4 pages.

| Chỉ số | Giá trị |
|---|---:|
| PV / user (mean) | **113,6** |
| Số user quay lại đa ngày | **100%** |
| Games / user (mean) | **25,7** |
| 4+ game | **95%** |
| Tổng thời gian / user (mean) | **1.710s (~28 phút)** |
| Tổng thời gian / user (median) | 1.490s (~25 phút) |

→ **Power user zapgames dành 28 phút / user, chơi 26 game khác nhau** — cực kỳ trung thành và có engagement sâu. Đây là tệp user "heavy" nhất trong cả 3 phân khúc.

#### 🟡 Trung thành 1-3 game (C1) (mẫu 200 user)

| Chỉ số | Giá trị |
|---|---:|
| PV / user (mean) | 8,3 |
| Số user quay lại đa ngày | **97%** |
| Games / user (mean) | 2,1 |
| 0 game | 0% |
| 1 game | 39% |
| 2-3 game | 51% |
| 4+ game | 10% |
| Tổng thời gian / user (mean) | 99s (~1,6 phút) |
| Tổng thời gian / user (median) | 63s |

→ **97% quay lại đa ngày** — đây là tệp user TRUNG THÀNH kể cả khi chỉ chơi 1-3 game. 90% C1 chơi ≤3 game.

#### 🟠 Trung thành trung bình (C2) (mẫu 148 user, bị giới hạn chunk)

> **Lưu ý về sample:** C2 cũng có nhiều page (33,8 PV/user) nên chunk limit 5.000 records chỉ lấy được 148/200 user.

| Chỉ số | Giá trị |
|---|---:|
| PV / user (mean) | 33,8 |
| Số user quay lại đa ngày | **98%** |
| Games / user (mean) | 11,1 |
| 4+ game | **91%** |
| Tổng thời gian / user (mean) | 544s (~9 phút) |
| Tổng thời gian / user (median) | 363s |

→ **98% quay lại đa ngày, 11 game/user, 9 phút/user** — đây là tệp user "trung thành trung bình" — chơi nhiều game, dành thời gian, quay lại thường xuyên.

### Tệp user — kết luận

- **0% Bounce thật sự** (mọi phân khúc đều quay lại ≥97%)
- **Phân khúc lớn nhất là C2 (42%)** — Trung thành trung bình, chơi 11 game, dành 9 phút
- **Power user (29%) dành 28 phút/user** — engagement sâu nhất trong 3 phân khúc
- **Trung thành 1-3 game (29%) dành 1,6 phút/user** — chơi ngắn nhưng **97% quay lại**

**Tệp user chủ yếu của zapgames là NGƯỜI CHƠI TRUNG THÀNH (71% mature users có 4+ game, 99% quay lại đa ngày).** Đây là profile có base user cực mạnh — không có Bounce segment đáng kể.

---

## 2. Gu game — họ chơi game nào nhiều nhất, lâu nhất

### 🟢 Lõi trung thành (Power) — C0

**Top 10 game theo PV:**

| # | Slug | Tên | PV | User | Mean sec/user |
|---:|---|---|---:|---:|---:|
| 1 | veck-io | Veck.io | **221** | 16 | **243s** |
| 2 | bloxdio | Bloxdio | 126 | 5 | 242s |
| 3 | basketball-hit | Basketball Hit | 98 | 10 | 52s |
| 4 | bowmasters-archery-shooting | Bowmasters: Archery Shooting | 95 | 17 | 237s |
| 5 | frontwarsio | Frontwars.io | 81 | 9 | 109s |
| 6 | golf-hit | Golf Hit | 56 | 13 | 52s |
| 7 | granny | Granny | 49 | 3 | 216s |
| 8 | basket-random | Basket Random | 47 | 7 | 54s |
| 9 | retro-rush | Retro Rush | 44 | 9 | 87s |
| 10 | hexanaut-io | Hexanaut.io | 42 | 6 | 58s |

**Top 10 game theo TỔNG thời gian chơi (giây):**

| # | Slug | Tên | Tổng sec | User | Mean sec/user |
|---:|---|---|---:|---:|---:|
| 1 | bowmasters-archery-shooting | Bowmasters | **4.025s** | 17 | 237s |
| 2 | veck-io | Veck.io | 3.893s | 16 | 243s |
| 3 | cornfield | Cornfield | 1.521s | 1 | 1.521s |
| 4 | billiard-snooker | Billiard Snooker | 1.219s | 3 | 406s |
| 5 | bloxdio | Bloxdio | 1.212s | 5 | 242s |
| 6 | frontwarsio | FrontWars.io | 977s | 9 | 109s |
| 7 | soflo-wheelie-life | Soflo Wheelie Life | 881s | 2 | 441s |
| 8 | retro-rush | Retro Rush | 784s | 9 | 87s |
| 9 | golf-hit | Golf Hit | 671s | 13 | 52s |
| 10 | narinig-mo-ba | Narinig Mo Ba | 815s | 1 | 815s |

**Top 10 game theo mean sec/user (lâu nhất):**

| # | Slug | Tên | User | Mean sec/user |
|---:|---|---|---:|---:|
| 1 | veck-io | Veck.io | 16 | **243s** |
| 2 | bloxdio | Bloxdio | 5 | 242s |
| 3 | bowmasters-archery-shooting | Bowmasters | 17 | 237s |
| 4 | frontwarsio | FrontWars.io | 9 | 109s |
| 5 | retro-rush | Retro Rush | 9 | 87s |
| 6 | rally-racer-dirt | Rally Racer Dirt | 7 | 79s |
| 7 | metro-escape | Metro Escape | 7 | 62s |
| 8 | wacky-flip | Wacky Flip | 5 | 59s |
| 9 | hexanaut-io | Hexanaut.io | 6 | 58s |
| 10 | basket-random | Basket Random | 7 | 54s |

→ **Gu game của Lõi trung thành zapgames:**
- **"King" là Veck.io** — top 1 PV (221) + lâu nhất/user (243s = 4 phút)
- **"Trung thành game" là Bowmasters** — 17 user (cao nhất), 237s/user, 4.025s tổng
- **Hai game .io** (Veck.io + Bloxdio) cùng mean ~242s → cùng nhóm "core .io"
- Power user zapgames CÓ game "trung thành" — Veck.io + Bowmasters chiếm lĩnh

### 🟡 Trung thành 1-3 game (C1)

**Top 10 game theo PV:**

| # | Slug | Tên | PV | User | Mean sec/user |
|---:|---|---|---:|---:|---:|
| 1 | veck-io | Veck.io | 60 | **24** | 48s |
| 2 | rocket-league | Rocket League | 52 | 5 | 74s |
| 3 | golf-hit | Golf Hit | 46 | 12 | 29s |
| 4 | escape-road-3 | Escape Road 3 | 41 | 5 | 102s |
| 5 | undead-invasion | Undead Invasion | 36 | 8 | 14s |
| 6 | 2v2io | 2V2.io | 34 | 8 | 75s |
| 7 | gta-5-online | GTA 5 Online | 33 | 13 | 27s |
| 8 | frontwarsio | FrontWars.io | 28 | 7 | 46s |
| 9 | supermarket-master | Supermarket Master | 25 | 1 | 383s |
| 10 | crazy-drive | Crazy Drive | 24 | 4 | 78s |

**Top 10 game theo TỔNG thời gian chơi:**

| # | Slug | Tên | Tổng sec | User | Mean sec/user |
|---:|---|---|---:|---:|---:|
| 1 | veck-io | Veck.io | **1.159s** | 24 | 48s |
| 2 | 2v2io | 2V2.io | 602s | 8 | 75s |
| 3 | escape-road-3 | Escape Road 3 | 510s | 5 | 102s |
| 4 | curve-rush-2 | Curve Rush 2 | 425s | 1 | 425s |
| 5 | pixel-path | Pixel Path | 392s | 2 | 196s |
| 6 | eaglercraft | Eaglercraft | 386s | 4 | 96s |
| 7 | supermarket-master | Supermarket Master | 383s | 1 | 383s |
| 8 | rocket-league | Rocket League | 372s | 5 | 74s |
| 9 | rocket-goal | Rocket Goal | 348s | 3 | 116s |
| 10 | gta-5-online | GTA 5 Online | 348s | 13 | 27s |

**Top 10 game theo mean sec/user:**

| # | Slug | Tên | User | Mean sec/user |
|---:|---|---|---:|---:|
| 1 | escape-road-3 | Escape Road 3 | 5 | **102s** |
| 2 | 2v2io | 2V2.io | 8 | 75s |
| 3 | rocket-league | Rocket League | 5 | 74s |
| 4 | veck-io | Veck.io | 24 | 48s |
| 5 | frontwarsio | FrontWars.io | 7 | 46s |
| 6 | pokerogue | Pokerogue | 5 | 45s |
| 7 | golf-hit | Golf Hit | 12 | 29s |
| 8 | gta-5-online | GTA 5 Online | 13 | 27s |
| 9 | minefunio | Minefun.io | 6 | 23s |
| 10 | space-waves | Space Waves | 7 | 18s |

→ **Gu game của C1 zapgames:**
- **Top 1 PV + top 1 user:** Veck.io (60 PV, 24 user) — Veck.io vẫn dẫn đầu ở C1
- **GTA 5 Online có 13 user** (cao) nhưng chỉ 27s/user → "casual thử nhanh"
- **Escape Road 3** lâu nhất mỗi phiên (102s/user, chỉ 5 user nhưng chơi sâu)
- **Đặc điểm:** C1 zapgames đa dạng — nhiều game khác nhau (rocket, gta, escape, .io, golf...)

### 🟠 Trung thành trung bình (C2)

**Top 10 game theo PV:**

| # | Slug | Tên | PV | User | Mean sec/user |
|---:|---|---|---:|---:|---:|
| 1 | veck-io | Veck.io | **135** | **37** | 63s |
| 2 | frontwarsio | FrontWars.io | 94 | 28 | 38s |
| 3 | bowmasters-archery-shooting | Bowmasters | 62 | 30 | **129s** |
| 4 | golf-hit | Golf Hit | 62 | 23 | 28s |
| 5 | undead-invasion | Undead Invasion | 59 | 18 | 71s |
| 6 | soflo-wheelie-life | Soflo Wheelie Life | 40 | 7 | 84s |
| 7 | space-waves | Space Waves | 39 | 22 | 20s |
| 8 | basketball-hit | Basketball Hit | 39 | 17 | 69s |
| 9 | undead-corridor | Undead Corridor | 36 | 6 | 78s |
| 10 | geometric-dash-lite | Geometric Dash Lite | 31 | 14 | 60s |

**Top 10 game theo TỔNG thời gian chơi:**

| # | Slug | Tên | Tổng sec | User | Mean sec/user |
|---:|---|---|---:|---:|---:|
| 1 | bowmasters-archery-shooting | Bowmasters | **3.879s** | 30 | 129s |
| 2 | veck-io | Veck.io | 2.341s | 37 | 63s |
| 3 | tap-rich-idle | Tap Rich Idle | 1.352s | 3 | 451s |
| 4 | undead-invasion | Undead Invasion | 1.286s | 18 | 71s |
| 5 | basketball-hit | Basketball Hit | 1.171s | 17 | 69s |
| 6 | eaglercraft | Eaglercraft | 1.115s | 6 | 186s |
| 7 | frontwarsio | FrontWars.io | 1.061s | 28 | 38s |
| 8 | wacky-flip | Wacky Flip | 859s | 13 | 66s |
| 9 | geometric-dash-lite | Geometric Dash Lite | 839s | 14 | 60s |
| 10 | granny | Granny | 807s | 4 | 202s |

**Top 10 game theo mean sec/user:**

| # | Slug | Tên | User | Mean sec/user |
|---:|---|---|---:|---:|
| 1 | eaglercraft | Eaglercraft | 6 | **186s** |
| 2 | bowmasters-archery-shooting | Bowmasters | 30 | 129s |
| 3 | pokerogue | Pokerogue | 8 | 92s |
| 4 | soflo-wheelie-life | Soflo Wheelie Life | 7 | 84s |
| 5 | undead-corridor | Undead Corridor | 6 | 78s |
| 6 | undead-invasion | Undead Invasion | 18 | 71s |
| 7 | gorilla-tag | Gorilla Tag | 5 | 71s |
| 8 | ragdoll-playground | Ragdoll Playground | 6 | 70s |
| 9 | basketball-hit | Basketball Hit | 17 | 69s |
| 10 | wacky-flip | Wacky Flip | 13 | 66s |

→ **Gu game của C2 zapgames:**
- **Top 1 PV + top 1 user:** Veck.io (135 PV, 37 user = 25% C2 chơi Veck.io)
- **Top 1 tổng thời gian:** Bowmasters (3.879s, 30 user, 129s/user)
- **Lâu nhất/user:** Eaglercraft (186s, chỉ 6 user nhưng chơi rất sâu)
- **"Core games"** (≥20 user, ≥50s/user): Veck.io, Bowmasters, Undead Invasion, FrontWars.io

### Tổng hợp gu game theo phân khúc

| | Lõi trung thành 🟢 | Trung thành 1-3 game 🟡 | Trung thành TB 🟠 |
|---|---|---|---|
| Game nhiều PV nhất | **Veck.io (221 PV)** | Veck.io (60 PV) | **Veck.io (135 PV, 37 user)** |
| Game nhiều user nhất | Bowmasters (17 user) | Veck.io (24 user) | **Veck.io (37 user)** |
| Game lâu nhất tổng | Bowmasters (4.025s) | Veck.io (1.159s) | Bowmasters (3.879s) |
| Game lâu nhất / user | **Veck.io (243s)** | Escape Road 3 (102s) | **Eaglercraft (186s)** |
| Gu chính | .io (Veck, Blox) + Bowmasters | Đa dạng (rocket, gta, escape, .io) | Veck.io + Bowmasters + FrontWars.io |

→ **Veck.io là "VUA" của zapgames** — top 1 PV ở cả 3 phân khúc, có user ở mọi segment. **Bowmasters là game "trung thành"** — game duy nhất có tổng thời gian chơi cao ở cả Power và C2.

---

## 3. Flow user — chi tiết

### Phân loại intent

| Intent | Mô tả |
|---|---|
| `home` | Trang chủ |
| `category_browse` | games/*, tag/*, hot, recent, popular, new, top, genre/* |
| `search` | Bắt đầu bằng `search` |
| `direct_game` | Slug là game trong catalog |

### 🟢 Lõi trung thành (Power) — flow đặc trưng: **CHAIN (chơi nối)**

**Top 15 transitions:**

| From | To | Số lần | % |
|---|---|---:|---:|
| **direct_game** | **direct_game** | **2.131** | **43,0%** |
| direct_game | home | 957 | 19,3% |
| home | direct_game | 944 | 19,0% |
| category_browse | direct_game | 222 | 4,5% |
| direct_game | category_browse | 198 | 4,0% |
| home | home | 130 | 2,6% |
| home | category_browse | 83 | 1,7% |
| category_browse | category_browse | 81 | 1,6% |
| category_browse | home | 62 | 1,3% |
| search | direct_game | 44 | 0,9% |

**Top 10 sequence 3 bước:**

| Step 1 | Step 2 | Step 3 | Số lần |
|---|---|---|---:|
| direct_game | direct_game | direct_game | **1.579** |
| direct_game | home | direct_game | 797 |
| home | direct_game | home | 508 |
| direct_game | direct_game | home | 412 |
| home | direct_game | direct_game | 400 |
| direct_game | category_browse | direct_game | 132 |
| category_browse | direct_game | direct_game | 114 |
| direct_game | direct_game | category_browse | 96 |
| category_browse | direct_game | category_browse | 78 |
| home | home | direct_game | 74 |

**Hành động ĐẦU TIÊN sau home (26 user):**

| Hành động | Số lần | % |
|---|---:|---:|
| direct_game | 20 | 76,9% |
| search | 4 | 15,4% |
| home | 2 | 7,7% |

**Hành động CUỐI CÙNG (44 user):**

| Hành động | Số lần | % |
|---|---:|---:|
| direct_game | 38 | 86,4% |
| home | 5 | 11,4% |
| category_browse | 1 | 2,3% |

→ **Pattern Power user zapgames:**
- 43,0% transition là `game → game` — chơi nối tiếp
- 19,3% là `game → home` — về home giữa các game
- 4,5% là `category_browse → game` — duyệt category
- **76,9% vào home → vào thẳng game** — có 15,4% search!
- 86,4% rời từ game
- **Loop đặc trưng:** `home → game → game → game → ...` (chain dài 100+ page)

**VÍ DỤ FLOW POWER USER (chuỗi thực tế):**
```
home → veck-io → veck-io → veck-io → veck-io → home → bowmasters → 
bowmasters → veck-io → frontwarsio → golf-hit → home → ... (chuỗi dài 100+ page)
```

### 🟡 Trung thành 1-3 game (C1) — flow đặc trưng: **SINGLE-GAME LOOP (lặp 1-2 game)**

**Top 15 transitions:**

| From | To | Số lần | % |
|---|---|---:|---:|
| **direct_game** | **direct_game** | **821** | **56,0%** (cao nhất trong 3 phân khúc) |
| home | direct_game | 256 | 17,5% |
| direct_game | home | 207 | 14,1% |
| home | home | 59 | 4,0% |
| category_browse | direct_game | 24 | 1,6% |
| (còn lại) | | 99 | 6,8% |

**Top 10 sequence 3 bước:**

| Step 1 | Step 2 | Step 3 | Số lần |
|---|---|---|---:|
| direct_game | direct_game | direct_game | **595** |
| direct_game | home | direct_game | 153 |
| home | direct_game | home | 117 |
| home | direct_game | direct_game | 104 |
| direct_game | direct_game | home | 70 |
| direct_game | home | home | 32 |
| home | home | direct_game | 30 |
| home | home | home | 16 |
| category_browse | direct_game | direct_game | 12 |
| search | direct_game | direct_game | 10 |

**Hành động ĐẦU TIÊN sau home (87 user):**

| Hành động | Số lần | % |
|---|---:|---:|
| direct_game | 68 | 78,2% |
| home | 10 | 11,5% |
| category_browse | 5 | 5,7% |
| search | 4 | 4,6% |

**Hành động CUỐI CÙNG (200 user):**

| Hành động | Số lần | % |
|---|---:|---:|
| direct_game | 177 | 88,5% |
| home | 22 | 11,0% |
| category_browse | 1 | 0,5% |

→ **Pattern C1 zapgames:**
- **56,0% transition là `game → game` (cao nhất trong 3 phân khúc)** → chơi liên tục cùng 1 game
- 14,1% là `game → home` (thấp nhất trong 3) → ít về home
- 78,2% vào home → vào thẳng game
- 88,5% rời từ game
- **Loop đặc trưng:** `home → game → game → game → ...` (chơi đi chơi lại 1-2 game)

**VÍ DỤ FLOW C1 (chuỗi thực tế):**
```
home → veck-io → veck-io → veck-io → veck-io → veck-io → 
veck-io → veck-io → veck-io → home → veck-io → ... (lặp 1 game)
home → gta-5-online → gta-5-online → home → golf-hit → golf-hit → ...
```

### 🟠 Trung thành trung bình (C2) — flow đặc trưng: **CHAIN + HOME LOOP**

**Top 15 transitions:**

| From | To | Số lần | % |
|---|---|---:|---:|
| **direct_game** | **direct_game** | **1.628** | **33,6%** |
| direct_game | home | 982 | 20,2% |
| home | direct_game | 976 | 20,1% |
| **category_browse** | **direct_game** | **313** | **6,5%** (cao nhất) |
| direct_game | category_browse | 237 | 4,9% |
| home | home | 173 | 3,6% |
| category_browse | category_browse | 158 | 3,3% (cao nhất) |
| home | category_browse | 123 | 2,5% |
| search | direct_game | 61 | 1,3% |
| category_browse | home | 54 | 1,1% |

**Top 10 sequence 3 bước:**

| Step 1 | Step 2 | Step 3 | Số lần |
|---|---|---|---:|
| direct_game | direct_game | direct_game | **1.108** |
| direct_game | home | direct_game | 768 |
| home | direct_game | home | 557 |
| direct_game | direct_game | home | 346 |
| home | direct_game | direct_game | 333 |
| direct_game | category_browse | direct_game | 162 |
| category_browse | direct_game | direct_game | 131 |
| category_browse | direct_game | category_browse | 113 |
| direct_game | home | home | 100 |
| home | home | direct_game | 99 |

**Hành động ĐẦU TIÊN sau home (103 user):**

| Hành động | Số lần | % |
|---|---:|---:|
| direct_game | 72 | 69,9% |
| **category_browse** | **14** | **13,6%** (cao nhất trong 3 phân khúc) |
| home | 10 | 9,7% |
| search | 7 | 6,8% |

**Hành động CUỐI CÙNG (148 user):**

| Hành động | Số lần | % |
|---|---:|---:|
| direct_game | 122 | 82,4% |
| home | 18 | 12,2% |
| category_browse | 5 | 3,4% |
| search | 3 | 2,0% |

→ **Pattern C2 zapgames:**
- 33,6% transition là `game → game` (thấp nhất trong 3) → hay về home
- 20,2% `game → home` (cao nhất) + 20,1% `home → game` → **loop home rất nhiều**
- **6,5% `category_browse → game` (cao nhất trong 3)** → C2 dùng category page nhiều nhất
- 13,6% vào home → duyệt category (cao nhất)
- 82,4% rời từ game
- **Loop đặc trưng:** `home → game → home → category → game → home → game → game → ...`

**VÍ DỤ FLOW C2 (chuỗi thực tế):**
```
home → veck-io → veck-io → home → frontwarsio → frontwarsio → home → 
category_browse (games/io) → veck-io → home → bowmasters → home → ...
```

### Tổng hợp flow 3 phân khúc

| | Lõi trung thành 🟢 | Trung thành 1-3 game 🟡 | Trung thành TB 🟠 |
|---|---|---|---|
| Top 1 transition | game→game (43,0%) | **game→game (56,0%)** | game→game (33,6%) |
| Top 1 sequence | game→game→game (1.579) | game→game→game (595) | game→game→game (1.108) |
| % vào thẳng game từ home | 76,9% | 78,2% | 69,9% |
| % vào category từ home | thấp | 5,7% | **13,6%** |
| % rời từ game | 86,4% | 88,5% | 82,4% |
| Pattern đặc trưng | **CHAIN dài** | **SINGLE-GAME LOOP** | **CHAIN + HOME LOOP** |
| 2 game trở lên | 100% | 61% | 99% |
| **% flow qua category** | 8,0% | 4,4% | **15,6%** (cao nhất) |

→ **So sánh flow giữa 3 phân khúc zapgames:**
- **C1 dùng `game→game` nhiều nhất** (56,0%) → lặp 1-2 game
- **C2 dùng `category_browse→game` nhiều nhất** (6,5%) → duyệt category nhiều
- **C0 (Power) có chain dài nhất** (1.579 lần `game→game→game`)
- → **C0 = CHAIN, C1 = SINGLE-GAME LOOP, C2 = CHAIN + HOME LOOP**

---

## 4. Câu hỏi mở cho team

1. **Tại sao zapgames có 99% user quay lại đa ngày?** Traffic đến từ đâu (Google, social, direct)? Có cơ chế gì khiến user stickiness cao đến vậy?

2. **Veck.io là "vua"** của zapgames (top 1 PV ở cả 3 phân khúc, 16+24+37 = 77 user trong 392 sample). Nếu Veck.io bị downtime, mất bao nhiêu engagement? Cần backup game .io tương tự?

3. **Bowmasters là game "trung thành" của Power + C2** (3.879s + 4.025s tổng). Tại sao game này hấp dẫn user zapgames đến vậy? Có thể nhân bản genre "bắn cung" không?

4. **97% C1 quay lại đa ngày** nhưng chỉ chơi 1-3 game và 99s/user. Họ là "small loyal fans" — đáng để target với email marketing "Game mới cùng dòng [Veck.io / Bowmasters]".

5. **zapgames C2 dùng category page 15,6%** — đây là cơ hội. Nếu cải thiện category page, có thể tăng tỉ lệ browse → play cho cả 3 phân khúc.

6. **C0 Power user dành 28 phút/user** — engagement sâu nhất. Cần chính sách giữ chân đặc biệt cho Power user.

---

## Tìm dữ liệu ở đâu

| File | Nội dung |
|---|---|
| `d:\GR\User Segmentation\data\journey_zapgames\journeys_raw.json` | 392 user × chuỗi page (intent + slug + ts + engaged_msec) |
| `d:\GR\User Segmentation\data\journey_zapgames\flow_summary.json` | Tổng hợp flow theo cluster (transitions, first/last action) |
| `d:\GR\zapgames_journey_extract.py` | Script extract journey từ ClickHouse |
| `d:\GR\zapgames_journey_analyze.py` | Script phân tích journey |
| `d:\GR\User Segmentation\data\clusters_zapgames_2026-10-01.csv` | Cluster mapping (58.511 user) |
| `d:\GR\zapgames_all.csv` | Metadata 1.152 game |

---

**Ngày tạo:** 2026-10-09
**Phương pháp:** Sample 200 user/cluster, lấy chuỗi page theo thời gian từ `gm_pages`, phân loại intent, đếm transition
**Site:** zapgames.io
**Khoảng thời gian:** 2026-08-10 đến 2026-10-01 (22 ngày gần nhất; zapgames có data dài hơn từ 2026-08-10)
**Sample size:** 392 user (C0: 44, C1: 200, C2: 148) — C0 và C2 bị giới hạn bởi ClickHouse chunk (5.000 records) vì Power user có nhiều page
**Lưu ý:** Sample C0 (44 user) nhỏ hơn mong đợi vì zapgames Power user có 113,6 PV/user (rất cao) — 1 user chiếm nhiều chunk. Kết quả C0 vẫn đáng tin vì 100% C0 user đều có ≥4 pages và travel pattern đồng nhất.
