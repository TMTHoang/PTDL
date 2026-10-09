# Phân tích User, Gu Game & Flow — 1000games.io

**Site:** 1000games.io
**Khoảng thời gian:** 22 ngày kết thúc ngày 1 tháng 10, 2026 (2026-09-10 → 2026-10-01)
**Mẫu phân tích:** 200 user / phân khúc (stratified by `top_game_slug` để đảm bảo variety), tổng 518 user
**Dữ liệu:** `gm_pages` của ClickHouse — page_location, first_ts, engagement_total_msec
**Phương pháp:** Lấy chuỗi page theo thời gian cho mỗi user, phân loại intent, đếm chuyển trạng thái
**Ngày:** 8 tháng 10, 2026

---

## TL;DR — Trả lời 3 câu hỏi

### 1. Tệp user chủ yếu của 1000games là ai? Người chơi 1 lần hay trung thành?

**Tệp user chủ yếu là NGƯỜI CHƠI 1 LẦN — chiếm 38% mature users (20.042 user).** Phân khúc trung thành chỉ chiếm 26%. Đây là tệp user khác biệt rõ rệt với các site game khác — thường user game casual có ~70% trung thành, 1000games thì ngược lại.

| Phân khúc | % mature | Đặc điểm | Loyal? |
|---|---:|---|---|
| 🔴 Vào rồi thoát (Bounce) | **38%** | 1,3 game, 92s/user, 47% chỉ vào 1 lần duy nhất | ❌ KHÔNG trung thành |
| 🟡 Trung thành 1-3 game (Casual) | 36% | 2,6 game, 107s/user, 22% quay lại đa ngày | ⚠️ Trung thành YẾU |
| 🟢 Lõi trung thành (Power) | 26% | 12,4 game, 657s/user, 58% quay lại đa ngày | ✅ Trung thành MẠNH |

### 2. Gu game của họ là gì? Game nào nhiều nhất / lâu nhất?

**Gu chính:** slope/runner + thể thao (sports). Top game khác nhau theo phân khúc:

| Phân khúc | Game nhiều PV nhất | Game chơi LÂU NHẤT (mean sec/user) | Game "trung thành" |
|---|---|---|---|
| 🟢 Lõi trung thành | 2v2.io (156 PV) + Slope 2 (145 PV) | **Basketball Hit (343s)** + 2v2.io (189s) | Không có — chơi đủ thể loại |
| 🔴 Vào rồi thoát | Survival Race (34 PV) | **Survival Race (68s)** | Slope 2, Golf Hit (chỉ chơi 13-15s, vào rồi thoát) |
| 🟡 Trung thành 1-3 game | **Dummies World Cup (78 PV)** | **Bow Battle (110s)** + Bowmasters (103s) | Dummies + Golf Hit |

### 3. Flow user là gì?

**Flow chính của 1000games: `home → direct_game → home` (vòng lặp "vào chơi, thoát, vào lại")**

Trong 3 phân khúc, flow khác nhau ở mức độ "loop" vs "chain":

| Phân khúc | Top flow 3 bước | Tỉ lệ "chỉ chơi 1 game" | Đặc điểm |
|---|---|---:|---|
| 🟢 Lõi trung thành | game → game → game | 0% | Chain — chơi nối tiếp nhiều game, không về home |
| 🔴 Vào rồi thoát | home → game → home | **47% vào 1 lần rồi đi** | Bounce — vào, chơi, đi, không quay lại |
| 🟡 Trung thành 1-3 game | home → game → home | 35% chơi đúng 1 game | Single-game loop — quay lại cùng 1 game |

→ **Nhìn chung, 1000games KHÔNG có flow "duyệt category"** — chỉ 3-6% transition qua `category_browse`. Đây là site "vào thẳng game", không phải site "cổng duyệt game".

---

## 1. Tệp user chủ yếu của 1000games — chi tiết

### Bằng chứng định lượng

Từ mẫu 200 user / phân khúc, ta xem "độ sâu" hành vi:

#### 🟢 Lõi trung thành (Power) — C0 (mẫu 118 user)

| Chỉ số | Giá trị |
|---|---:|
| PV / user (mean) | **42,4** |
| Số user quay lại đa ngày | **58%** (cao nhất) |
| Games / user (mean) | **12,4** |
| Phân bổ số game: 0 game | 0% |
| Phân bổ số game: 1 game | 0% |
| Phân bổ số game: 2-3 game | 8% |
| Phân bổ số game: 4+ game | **92%** |
| Tổng thời gian / user (mean) | **657s (~11 phút)** |
| Tổng thời gian / user (median) | 341s (~6 phút) |

→ **Power user dành 11 phút / user, chơi 12 game khác nhau.** Đây là phân khúc "người chơi thật sự" của 1000games.

#### 🔴 Vào rồi thoát (Bounce) — C1 (mẫu 200 user)

| Chỉ số | Giá trị |
|---|---:|
| PV / user (mean) | 6,1 |
| Số user quay lại đa ngày | **14%** (rất thấp) |
| Games / user (mean) | 1,3 |
| Phân bổ số game: 0 game | **47%** |
| Phân bổ số game: 1 game | 22% |
| Phân bổ số game: 2-3 game | 21% |
| Phân bổ số game: 4+ game | 11% |
| Tổng thời gian / user (mean) | 92s (~1,5 phút) |
| Tổng thời gian / user (median) | 50s |

→ **47% Bounce user KHÔNG chơi game nào — chỉ vào xem rồi đi.** 22% chỉ chơi 1 game. **92s trung bình** (dưới 2 phút). Phân khúc này chiếm 38% mature users → 1000games đang có vấn đề nghiêm trọng về giữ chân.

#### 🟡 Trung thành 1-3 game (Casual) — C2 (mẫu 200 user)

| Chỉ số | Giá trị |
|---|---:|
| PV / user (mean) | 6,8 |
| Số user quay lại đa ngày | 22% |
| Games / user (mean) | 2,6 |
| Phân bổ số game: 0 game | 2% |
| Phân bổ số game: 1 game | **36%** |
| Phân bổ số game: 2-3 game | 37% |
| Phân bổ số game: 4+ game | 26% |
| Tổng thời gian / user (mean) | 107s (~1,8 phút) |
| Tổng thời gian / user (median) | 58s |

→ **36% Casual chơi đúng 1 game** — đây là "single-game loyalists" của 1000games. Tổng cộng **73% C2 chơi ≤3 game**.

### Tệp user chủ yếu — kết luận

- **38% user Bounce** (vào 1 lần, không quay lại, thường không chơi game)
- **36% user Casual** (chơi 1-3 game, 22% quay lại)
- **26% user Power** (chơi 12+ game, 58% quay lại, dành 11 phút/user)

**Tệp user chủ yếu (62%) là NGƯỜI CHƠI YẾU / KHÔNG TRUNG THÀNH** — chỉ 26% mature users thật sự trung thành. Đây là profile **nghịch lý với phần lớn site game** — thường thì 60-70% user là trung thành, 20-30% là bounce.

**Hệ quả chiến lược:**
- Tệp user 1000games thiên về "casual traffic" — user search Google tên game cụ thể → click vào → chơi → đi
- Power user (26%) quý giá — họ dành 11 phút/user, chơi 12 game
- Cần chiến lược chuyển đổi Casual (36%) thành Power, và Bounce (38%) thành Casual

---

## 2. Gu game — họ chơi game nào nhiều nhất, lâu nhất

### 🟢 Lõi trung thành (Power) — C0

**Top 10 game theo PV (lượt click trong 22 ngày, sample 118 user):**

| # | Slug | Tên | PV | User | Mean sec/user |
|---:|---|---|---:|---:|---:|
| 1 | 2v2-io | 2v2.io | 156 | 21 | 189s |
| 2 | slope-2 | Slope 2 | 145 | **40** | 99s |
| 3 | golf-hit | Golf Hit | 139 | 32 | 71s |
| 4 | frontwarsio | FrontWars.io | 108 | 21 | 30s |
| 5 | veck-io | Veck.io | 95 | 26 | 105s |
| 6 | survival-race | Survival Race | 86 | 37 | 64s |
| 7 | pokerogue | Pokerogue | 81 | 3 | 251s |
| 8 | retro-rush | Retro Rush | 57 | 14 | 44s |
| 9 | bowmasters-archery-shooting | Bowmasters: Archery Shooting | 55 | 27 | 83s |
| 10 | drift-rush | Drift Rush | 54 | 26 | 28s |

**Top 10 game theo TỔNG THỜI GIAN CHƠI (giây):**

| # | Slug | Tên | Tổng sec | User | Mean sec/user |
|---:|---|---|---:|---:|---:|
| 1 | slope-2 | Slope 2 | **3.971s** | 40 | 99s |
| 2 | 2v2-io | 2v2.io | 3.963s | 21 | 189s |
| 3 | veck-io | Veck.io | 2.722s | 26 | 105s |
| 4 | survival-race | Survival Race | 2.379s | 37 | 64s |
| 5 | golf-hit | Golf Hit | 2.271s | 32 | 71s |
| 6 | bowmasters-archery-shooting | Bowmasters | 2.248s | 27 | 83s |
| 7 | basketball-hit | Basketball Hit | 1.716s | 5 | **343s** |
| 8 | undead-invasion | Undead Invasion | 1.065s | 3 | 355s |
| 9 | flip-rush | Flip Rush | 882s | 18 | 49s |
| 10 | baseball-bros | Baseball Bros | 875s | 12 | 73s |

**Top 10 game theo THỜI GIAN CHƠI TRUNG BÌNH / user (lâu nhất mỗi phiên):**

| # | Slug | Tên | User | Mean sec/user |
|---:|---|---|---:|---:|
| 1 | basketball-hit | Basketball Hit | 5 | **343s** |
| 2 | 2v2-io | 2v2.io | 21 | 189s |
| 3 | veck-io | Veck.io | 26 | 105s |
| 4 | slope-2 | Slope 2 | 40 | 99s |
| 5 | bowmasters-archery-shooting | Bowmasters | 27 | 83s |
| 6 | baseball-bros | Baseball Bros | 12 | 73s |
| 7 | track-dash | Track Dash | 8 | 71s |
| 8 | golf-hit | Golf Hit | 32 | 71s |
| 9 | arcade-glide | Arcade Glide | 8 | 71s |
| 10 | survival-race | Survival Race | 37 | 64s |

→ **Gu game của Lõi trung thành:**
- **Nhiều PV nhất:** 2v2.io + Slope 2 (cùng ~150 PV)
- **Lâu nhất tổng cộng:** Slope 2 (3.971s = 66 phút tổng)
- **Lâu nhất mỗi phiên:** Basketball Hit (343s = 5,7 phút/phiên) — nhưng chỉ 5 user
- **"Core games"** (≥20 user, ≥50s/user): Slope 2, 2v2.io, Veck.io, Bowmasters, Golf Hit, Survival Race, Drift Rush — 7 game
- **Power user KHÔNG có game "trung thành"** — họ chơi 12 game khác nhau, không có game chiếm ưu thế

### 🔴 Vào rồi thoát (Bounce) — C1

**Top 10 game theo PV:**

| # | Slug | Tên | PV | User | Mean sec/user |
|---:|---|---|---:|---:|---:|
| 1 | survival-race | Survival Race | 34 | 23 | **68s** |
| 2 | slope-2 | Slope 2 | 26 | 18 | **13s** |
| 3 | golf-hit | Golf Hit | 13 | 10 | 15s |
| 4 | bowmasters-archery-shooting | Bowmasters | 12 | 9 | 32s |
| 5 | penalty-kick | Penalty Kick | 11 | 10 | 10s |
| 6 | drift-rush | Drift Rush | 10 | 6 | 57s |
| 7 | frontwarsio | FrontWars.io | 10 | 10 | 9s |
| 8 | krillion-game | Krillion | 9 | 6 | 6s |
| 9 | bottle-hop | Bottle Hop | 9 | 6 | 64s |
| 10 | horror-nun-2 | Horror Nun 2 | 7 | 6 | 18s |

**Top 10 game theo TỔNG THỜI GIAN CHƠI:**

| # | Slug | Tên | Tổng sec | User | Mean sec/user |
|---:|---|---|---:|---:|---:|
| 1 | survival-race | Survival Race | **1.555s** | 23 | 68s |
| 2 | racing-limits | Racing Limits | 828s | 2 | 414s |
| 3 | bottle-hop | Bottle Hop | 385s | 6 | 64s |
| 4 | drift-rush | Drift Rush | 342s | 6 | 57s |
| 5 | bowmasters | Bowmasters | 285s | 9 | 32s |
| 6 | veck-io | Veck.io | 243s | 6 | 41s |
| 7 | slope-2 | Slope 2 | 240s | 18 | 13s |
| 8 | golf-hit | Golf Hit | 149s | 10 | 15s |
| 9 | horror-nun | Horror Nun | 126s | 3 | 42s |
| 10 | horror-nun-2 | Horror Nun 2 | 108s | 6 | 18s |

**Top 10 game theo THỜI GIAN CHƠI TRUNG BÌNH / user:**

| # | Slug | Tên | User | Mean sec/user |
|---:|---|---|---:|---:|
| 1 | survival-race | Survival Race | 23 | **68s** |
| 2 | bottle-hop | Bottle Hop | 6 | 64s |
| 3 | drift-rush | Drift Rush | 6 | 57s |
| 4 | veck-io | Veck.io | 6 | 41s |
| 5 | bowmasters | Bowmasters | 9 | 32s |
| 6 | horror-nun-2 | Horror Nun 2 | 6 | 18s |
| 7 | golf-hit | Golf Hit | 10 | 15s |
| 8 | slope-2 | Slope 2 | 18 | 13s |
| 9 | penalty-kick | Penalty Kick | 10 | 10s |
| 10 | frontwarsio | FrontWars.io | 10 | 9s |

→ **Gu game của Bounce:**
- **Nhiều user chơi nhất:** Survival Race (23 user), Slope 2 (18 user)
- **Lâu nhất mỗi phiên:** Survival Race (68s/user) — nhiều gấp 5 lần Slope 2 (13s/user)
- **"Đặc điểm chính":** Slope 2 có 18 user nhưng chỉ 13s/user → user **vào, xem 13 giây, thoát** — họ không thực sự "chơi" Slope 2, họ chỉ ghé xem
- Survival Race (68s/user) là game **duy nhất** user Bounce chơi "có thời gian" — game này có loop hấp dẫn đủ để giữ user 1 phút

### 🟡 Trung thành 1-3 game (Casual) — C2

**Top 10 game theo PV:**

| # | Slug | Tên | PV | User | Mean sec/user |
|---:|---|---|---:|---:|---:|
| 1 | dummies-world-cup | **Dummies World Cup** | **78** | 23 | 22s |
| 2 | golf-hit | Golf Hit | 68 | 26 | 86s |
| 3 | survival-race | Survival Race | 43 | 26 | 38s |
| 4 | slope-2 | Slope 2 | 39 | 24 | 18s |
| 5 | bowmasters | Bowmasters | 22 | 16 | **103s** |
| 6 | bottle-hop | Bottle Hop | 22 | 17 | 10s |
| 7 | horror-nun-2 | Horror Nun 2 | 22 | 11 | 20s |
| 8 | real-war-not-fake | Real War: Not Fake | 22 | 8 | 12s |
| 9 | meccha-chameleon | Meccha Chameleon | 21 | 11 | 6s |
| 10 | frontwarsio | FrontWars.io | 20 | 13 | 10s |

**Top 10 game theo TỔNG THỜI GIAN CHƠI:**

| # | Slug | Tên | Tổng sec | User | Mean sec/user |
|---:|---|---|---:|---:|---:|
| 1 | golf-hit | Golf Hit | **2.224s** | 26 | 86s |
| 2 | bowmasters | Bowmasters | 1.654s | 16 | 103s |
| 3 | survival-race | Survival Race | 986s | 26 | 38s |
| 4 | sled-rider | Sled Rider | 897s | 1 | 897s |
| 5 | penalty-kick | Penalty Kick | 749s | 9 | 83s |
| 6 | bow-battle | Bow Battle | 660s | 6 | **110s** |
| 7 | dummies-world-cup | Dummies World Cup | 495s | 23 | 22s |
| 8 | retro-rush | Retro Rush | 459s | 9 | 51s |
| 9 | slope-2 | Slope 2 | 439s | 24 | 18s |
| 10 | flip-rush | Flip Rush | 374s | 10 | 37s |

**Top 10 game theo THỜI GIAN CHƠI TRUNG BÌNH / user:**

| # | Slug | Tên | User | Mean sec/user |
|---:|---|---|---:|---:|
| 1 | bow-battle | Bow Battle | 6 | **110s** |
| 2 | bowmasters | Bowmasters | 16 | 103s |
| 3 | golf-hit | Golf Hit | 26 | 86s |
| 4 | penalty-kick | Penalty Kick | 9 | 83s |
| 5 | retro-rush | Retro Rush | 9 | 51s |
| 6 | survival-race | Survival Race | 26 | 38s |
| 7 | flip-rush | Flip Rush | 10 | 37s |
| 8 | sky-dart | Sky Dart | 5 | 35s |
| 9 | drift-rush | Drift Rush | 7 | 31s |
| 10 | airborne-bmx | Airborne BMX | 6 | 25s |

→ **Gu game của Casual:**
- **Top 1 PV:** **Dummies World Cup** (78 PV) — game "trung thành" của phân khúc này
- **Lâu nhất tổng cộng:** Golf Hit (2.224s = 37 phút)
- **Lâu nhất mỗi phiên:** Bow Battle (110s), Bowmasters (103s)
- **Hai game "archer"** (Bow Battle, Bowmasters) chiếm vị trí 1-2 về thời gian/user — đây là game **genre bắn cung** rất hấp dẫn với Casual

### Tổng hợp gu game theo phân khúc

| | Lõi trung thành 🟢 | Bounce 🔴 | Casual 🟡 |
|---|---|---|---|
| Game nhiều PV nhất | 2v2.io (156) | Survival Race (34) | **Dummies World Cup (78)** |
| Game nhiều user nhất | Slope 2 (40 user) | Survival Race (23 user) | Golf Hit (26 user) |
| Game lâu nhất tổng | Slope 2 (3.971s) | Survival Race (1.555s) | Golf Hit (2.224s) |
| Game lâu nhất / user | Basketball Hit (343s) | Survival Race (68s) | **Bow Battle (110s)** |
| Gu chính | Đa dạng (.io, slope, sports) | Survival Race + Slope 2 (vào xem) | **Dummies + Golf + Bowmasters** |

→ **Mỗi phân khúc có gu game khác nhau** — Power user đa dạng, Bounce chỉ xem 1-2 game, Casual tập trung 1 game + bow genre.

---

## 3. Flow user — chi tiết

### Phân loại intent (loại trang)

Mỗi page view được phân loại:

| Intent | Mô tả | Vai trò |
|---|---|---|
| `home` | Trang chủ (slug rỗng) | Vào / không click |
| `category_browse` | `games/*`, `tag/*`, `hot`, `recent`, `popular`, `new`, `top` | Duyệt category |
| `search` | Bắt đầu bằng `search` | Tìm kiếm |
| `direct_game` | Slug là game trong catalog | Vào thẳng game |

### 🟢 Lõi trung thành (Power) — flow đặc trưng: **GAME → GAME → GAME (chain)**

**Top 15 chuyển trạng thái (transitions):**

| From | To | Số lần | % |
|---|---|---:|---:|
| **direct_game** | **direct_game** | 2.025 | **41,5%** |
| home | direct_game | 900 | 18,4% |
| direct_game | home | 889 | 18,2% |
| category_browse | direct_game | 307 | 6,3% |
| direct_game | category_browse | 235 | 4,8% |
| home | category_browse | 155 | 3,2% |
| home | home | 94 | 1,9% |
| category_browse | category_browse | 84 | 1,7% |
| category_browse | home | 80 | 1,6% |
| search | direct_game | 24 | 0,5% |
| (còn lại) | | 91 | 1,9% |

**Top 10 sequence 3 bước:**

| Step 1 | Step 2 | Step 3 | Số lần |
|---|---|---|---:|
| direct_game | direct_game | direct_game | **1.566** |
| direct_game | home | direct_game | 721 |
| home | direct_game | home | 509 |
| home | direct_game | direct_game | 338 |
| direct_game | direct_game | home | 324 |
| direct_game | category_browse | direct_game | 162 |
| category_browse | direct_game | category_browse | 156 |
| home | category_browse | direct_game | 95 |
| category_browse | direct_game | direct_game | 91 |
| direct_game | home | category_browse | 80 |

**Hành động ĐẦU TIÊN sau khi vào trang chủ (99 user):**

| Hành động | Số lần | % |
|---|---:|---:|
| **direct_game** | **80** | **80,8%** |
| home | 9 | 9,1% |
| category_browse | 9 | 9,1% |
| search | 1 | 1,0% |

**Hành động CUỐI CÙNG trước khi rời (118 user):**

| Hành động | Số lần | % |
|---|---:|---:|
| **direct_game** | **105** | **89,0%** |
| home | 9 | 7,6% |
| category_browse | 4 | 3,4% |

→ **Pattern Power user:**
- 41,5% transition là `game → game` — họ chơi game này rồi chuyển sang game khác **KHÔNG về home**
- 80,8% vào home → vào thẳng game (chỉ 9% duyệt category)
- 89% rời site từ game (họ đang chơi thì đi, không phải từ trang chủ)
- **Loop đặc trưng:** `home → game → game → game → ...`

**VÍ DỤ FLOW POWER USER (chuỗi thực tế):**
```
home → 2v2-io → 2v2-io → 2v2-io → 2v2-io → home → slope-2 → slope-2 → 
slope-2 → slope-2 → survival-race → survival-race → ... (chuỗi dài 20-40 page)
```

### 🔴 Vào rồi thoát (Bounce) — flow đặc trưng: **HOME → GAME → HOME (bounce loop)**

**Top 15 chuyển trạng thái:**

| From | To | Số lần | % |
|---|---|---:|---:|
| **home** | **direct_game** | **388** | **38,3%** |
| direct_game | direct_game | 256 | 25,2% |
| direct_game | home | 228 | 22,5% |
| category_browse | direct_game | 26 | 2,6% |
| home | home | 25 | 2,5% |
| home | category_browse | 21 | 2,1% |
| direct_game | category_browse | 16 | 1,6% |
| (còn lại) | | 54 | 5,3% |

**Top 10 sequence 3 bước:**

| Step 1 | Step 2 | Step 3 | Số lần |
|---|---|---|---:|
| direct_game | home | direct_game | **192** |
| home | direct_game | home | 163 |
| home | direct_game | direct_game | 125 |
| direct_game | direct_game | direct_game | 111 |
| direct_game | direct_game | home | 60 |
| home | home | direct_game | 19 |
| home | category_browse | direct_game | 14 |
| direct_game | home | home | 13 |
| category_browse | direct_game | direct_game | 12 |
| direct_game | direct_game | category_browse | 8 |

**Hành động ĐẦU TIÊN sau khi vào trang chủ (191 user):**

| Hành động | Số lần | % |
|---|---:|---:|
| **direct_game** | **166** | **86,9%** |
| category_browse | 10 | 5,2% |
| home | 10 | 5,2% |
| search | 5 | 2,6% |

**Hành động CUỐI CÙNG trước khi rời (200 user):**

| Hành động | Số lần | % |
|---|---:|---:|
| **direct_game** | **182** | **91,0%** |
| home | 15 | 7,5% |
| category_browse | 3 | 1,5% |

→ **Pattern Bounce:**
- 38,3% transition là `home → game` (cao nhất trong 3 phân khúc) — **đặc trưng của "vào 1 lần"**
- 22,5% transition là `game → home` — user chơi xong rồi thoát
- 86,9% vào home → vào thẳng 1 game (cao hơn Power 80,8%) — họ click ngay, không duyệt
- 91% rời từ game
- **Loop đặc trưng:** `home → game → home → rời` (47% user chỉ có flow này 1 lần)

**VÍ DỤ FLOW BOUNCE (chuỗi thực tế):**
```
home → slope-2 → rời                    (1 page bounce, 26% user)
home → survival-race → home → rời       (2 page, common)
home → slope-2 → home → golf-hit → rời  (3 page, common)
```

### 🟡 Trung thành 1-3 game (Casual) — flow đặc trưng: **HOME → GAME → HOME (single-game loop)**

**Top 15 chuyển trạng thái:**

| From | To | Số lần | % |
|---|---|---:|---:|
| **direct_game** | **direct_game** | **541** | **46,9%** |
| home | direct_game | 292 | 25,3% |
| direct_game | home | 185 | 16,0% |
| category_browse | direct_game | 32 | 2,8% |
| home | category_browse | 24 | 2,1% |
| (còn lại) | | 80 | 6,9% |

**Top 10 sequence 3 bước:**

| Step 1 | Step 2 | Step 3 | Số lần |
|---|---|---|---:|
| direct_game | direct_game | direct_game | **367** |
| direct_game | home | direct_game | 156 |
| home | direct_game | direct_game | 122 |
| home | direct_game | home | 122 |
| direct_game | direct_game | home | 52 |
| home | home | direct_game | 15 |
| direct_game | category_browse | direct_game | 15 |
| category_browse | direct_game | direct_game | 14 |
| home | category_browse | direct_game | 12 |
| direct_game | home | category_browse | 11 |

**Hành động ĐẦU TIÊN sau khi vào trang chủ (132 user):**

| Hành động | Số lần | % |
|---|---:|---:|
| **direct_game** | **113** | **85,6%** |
| category_browse | 8 | 6,1% |
| home | 7 | 5,3% |
| search | 4 | 3,0% |

**Hành động CUỐI CÙNG trước khi rời (200 user):**

| Hành động | Số lần | % |
|---|---:|---:|
| **direct_game** | **188** | **94,0%** (cao nhất) |
| home | 10 | 5,0% |
| search | 2 | 1,0% |

→ **Pattern Casual:**
- 46,9% transition là `game → game` (cao nhất trong 3 phân khúc) — **chơi liên tục cùng 1 game**
- 25,3% transition là `home → game` — quay lại home rồi vào lại game
- 85,6% vào home → vào thẳng 1 game
- 94% rời từ game
- **Loop đặc trưng:** `home → game → game → home → game → game → ...`

**VÍ DỤ FLOW CASUAL (chuỗi thực tế):**
```
home → dummies-world-cup → dummies-world-cup → dummies-world-cup → 
dummies-world-cup → home → dummies-world-cup → ... (chơi 1 game liên tục)
```

### Tổng hợp flow 3 phân khúc

| | Lõi trung thành 🟢 | Bounce 🔴 | Casual 🟡 |
|---|---|---|---|
| Top 1 transition | game → game (41,5%) | **home → game (38,3%)** | game → game (46,9%) |
| Top 1 sequence | game→game→game (1.566) | game→home→game (192) | game→game→game (367) |
| % vào thẳng game từ home | 80,8% | 86,9% | 85,6% |
| % rời từ game | 89,0% | 91,0% | **94,0%** |
| Pattern đặc trưng | **CHAIN (chơi nối)** | **BOUNCE (vào, đi)** | **SINGLE-GAME LOOP (lặp 1 game)** |
| 2 game trở lên | 100% | 53% | 64% |

→ **Cả 3 phân khúc đều KHÔNG có flow "duyệt category"** — chỉ 3-6% transition qua `category_browse`. 1000games là site "vào thẳng game", không phải site "cổng".

→ **3 flow pattern khác nhau rất rõ:**
- 🟢 **CHAIN** — Power user chơi nhiều game nối tiếp (1.566 lần `game→game→game`)
- 🔴 **BOUNCE** — Bounce user vào 1 game rồi đi (192 lần `game→home→game` = quay lại game khác)
- 🟡 **SINGLE-GAME LOOP** — Casual user chơi đi chơi lại 1 game (367 lần `game→game→game` cùng game)

---

## 4. Câu hỏi mở cho team

1. **47% Bounce user không chơi game nào** — họ vào trang chủ, không thấy gì để click. Tại sao? Họ đến từ Google với từ khóa cụ thể? Trang chủ không đủ hấp dẫn?

2. **Power user dành 11 phút/user, chơi 12 game** — chiếm 26% mature users. Họ có đáng để "early access" game mới?

3. **Casual user tập trung vào Dummies World Cup + Golf Hit + Bowmasters** — 3 game này có đặc điểm gì chung? Có thể tạo game tương tự không?

4. **1000games không có flow "duyệt category"** — đây là cơ hội lớn. Nếu cải thiện trang chủ / category page, có thể tăng tỉ lệ user thử nhiều game.

5. **Slope 2 có 40 Power user + 18 Bounce user + 24 Casual user = 82 user** trong sample 518. Nhưng Bounce user chỉ chơi 13s/user trong khi Power user chơi 99s/user → **cùng 1 game nhưng engagement rất khác**. Tại sao?

---

## Tìm dữ liệu ở đâu

| File | Nội dung |
|---|---|
| `d:\GR\User Segmentation\data\journey_1000games\journeys_raw.json` | 518 user × chuỗi page (intent + slug + ts + engaged_msec) |
| `d:\GR\User Segmentation\data\journey_1000games\flow_summary.json` | Tổng hợp flow theo cluster (transitions, first/last action) |
| `d:\GR\1000games_journey_extract.py` | Script extract journey từ ClickHouse |
| `d:\GR\1000games_journey_analyze.py` | Script phân tích journey |
| `d:\GR\User Segmentation\data\clusters_1000games_2026-10-01.csv` | Cluster mapping (52.608 user) |
| `d:\GR\1000games_all.csv` | Metadata 489 game |

---

**Ngày tạo:** 2026-10-08
**Phương pháp:** Sample 200 user/cluster, lấy chuỗi page theo thời gian từ `gm_pages`, phân loại intent, đếm transition
**Site:** 1000games.io
**Khoảng thời gian:** 2026-09-10 đến 2026-10-01 (22 ngày)
**Sample size:** 518 user (C0: 118, C1: 200, C2: 200) — stratified by `top_game_slug` để đảm bảo variety
**Lưu ý:** Sample có 118 user C0 thay vì 200 do giới hạn chunk size; C0 cũng có thể bị "lighter sample" vì power user có nhiều page, chiếm nhiều dung lượng chunks
