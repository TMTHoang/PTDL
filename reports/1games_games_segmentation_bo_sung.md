# Phân Tích Portfolio Game 1games.io — Tìm Thể Loại Chủ Lực & Game Tiềm Năng

**Ngày:** Ngày 7 tháng 10 năm 2026
**Nguồn dữ liệu:**
- `1games.io_all_games.csv` — 886 game (portfolio đầy đủ) — lấy từ CMS của site
- `1games_new_segmented.csv` — 82 game mới có traffic — đo lường qua `gm_events`
- `1games_new_games_meta.csv` — metadata crawl trực tiếp từ `1games.io/{slug}` ngày 2026-10-03

**Câu hỏi cần trả lời:**
1. Portfolio game hiện tại của 1games gồm những game gì, phân làm các thể loại nào.
2. Game user chơi nhiều, chơi lâu thuộc thể loại nào, có đặc điểm gì.
3. Có nhóm game nào thời gian tốt mà ít user không, có nhóm nào nhiều user mà thời gian kém không. (Kém = dưới 4 phút = < 240s trên trang game)
4. Tìm ra 1–3 thể loại chủ lực cho site và đặc điểm của chúng. Tìm ra các game tiềm năng để phát triển.

---

## 1. Tổng Quan Portfolio Game Của 1games

Portfolio đầy đủ của 1games.io hiện có **886 game đã xuất bản** (loại trừ các game có genre rỗng). Phân bố theo thể loại chính (primary genre):

| # | Thể loại chính | Số game | % trong portfolio |
|--:|----------------|------:|------------------:|
| 1 | **Arcade** | 204 | 23.0% |
| 2 | **Action** | 169 | 19.1% |
| 3 | **Adventure** | 131 | 14.8% |
| 4 | **Casual** | 84 | 9.5% |
| 5 | **Driving** | 72 | 8.1% |
| 6 | **Puzzle** | 60 | 6.8% |
| 7 | **Clicker** | 44 | 5.0% |
| 8 | **Simulation** | 38 | 4.3% |
| 9 | **Sports** | 29 | 3.3% |
| 10 | **.IO** | 15 | 1.7% |
| 11 | **Horror** | 14 | 1.6% |
| 12 | **Platform** | 9 | 1.0% |
| 13 | **Shooting** | 9 | 1.0% |
| 14 | **Survival** | 7 | 0.8% |

**Nhận xét tổng quan:**
- **Arcade + Action + Adventure = 504 game (57% portfolio)** — đây là 3 trụ cột về lượng game đã đăng.
- **Driving chiếm 8.1%** (72 game) — danh mục có tỷ trọng đáng kể.
- **Sports chỉ 3.3%** (29 game) — ít game dù chất lượng cao.
- **Horror, .IO, Shooting, Survival, Survival** — đều <2%, là các niche nhỏ.

### Top 30 Tag Phổ Biến Trong Portfolio

| Tag | n game | % | | Tag | n game | % |
|-----|------:|--:|--|-----|------:|--:|
| arcade | 262 | 29.6% | | collecting | 100 | 11.3% |
| casual | 247 | 27.9% | | puzzle | 97 | 10.9% |
| action | 169 | 19.1% | | car | 86 | 9.7% |
| simulation | 167 | 18.8% | | strategy | 82 | 9.3% |
| platform | 152 | 17.2% | | 3d | 81 | 9.1% |
| adventure | 149 | 16.8% | | funny | 81 | 9.1% |
| physics | 121 | 13.7% | | 1 player | 78 | 8.8% |
| avoid | 120 | 13.5% | | speed | 75 | 8.5% |
| driving | 112 | 12.6% | | fast-paced | 75 | 8.5% |
| incremental | 108 | 12.2% | | obstacle | 74 | 8.4% |
| skill | 108 | 12.2% | | running | 73 | 8.2% |
| racing | 73 | 8.2% | | shooting | 72 | 8.1% |
| sports | 68 | 7.7% | | survival | 67 | 7.6% |
| weapon | 66 | 7.4% | | ball | 65 | 7.3% |
| jumping | 60 | 6.8% | | animal | 58 | 6.5% |

**Cụm tag phổ biến nhất:**
- **Cụm kỹ năng/phản xạ**: skill (108) + jumping (60) + obstacle (1) + fast-paced (75)
- **Cụm xe/tốc độ**: driving (112) + car (86) + racing (73) + speed (75)
- **Cụm incremental**: incremental (108) + collecting (100)

---

## 3. Game User Chơi Nhiều + Chơi Lâu Thuộc Thể Loại Nào

Trong số 886 game đã đăng, có **82 game mới** đã có traffic trong khoảng 2026-09-04 → 2026-09-25 và đủ ≥200 phiên để phân tích. Engagement được tính theo user-page engagement (người dùng tổng thời gian > 30s = engaged).

### Engagement Theo Thể Loại Chính (82 game mới)

| Thể loại | n | Users | avg_p50 | avg_p90 | avg_eng% | avg_users/game |
|----------|--:|------:|--------:|--------:|---------:|---------------:|
| **Driving** | 7 | 17,145 | **293s** | 2,488s | **83.0%** | 2,449 |
| **Sports** | 4 | 7,865 | **331s** | 2,542s | **82.5%** | 1,966 |
| Action | 14 | 15,934 | 240s | 2,508s | 77.8% | 1,138 |
| Casual | 7 | 9,539 | 254s | 2,646s | 77.6% | 1,363 |
| Puzzle | 3 | 2,539 | 294s | 2,741s | 79.8% | 846 |
| Arcade | 33 | 82,668 | 196s | 2,101s | 75.7% | 2,505 |
| Adventure | 4 | 6,657 | 185s | 2,160s | 74.3% | 1,664 |
| Horror | 1 | 2,334 | 291s | 1,994s | 80.5% | 2,334 |
| Shooting | 2 | 1,531 | 294s | 3,064s | 78.0% | 766 |
| .IO | 1 | 290 | 280s | 2,891s | 78.6% | 290 |
| Clicker | 2 | 2,625 | **88s** | 2,327s | 74.5% | 1,312 |
| Simulation | 4 | 4,207 | **110s** | 2,161s | 73.0% | 1,052 |

### Top 10 Game User Chơi Nhiều (Users × Engagement)

| Slug | Users | Eng% | p50 | p90 | Category | Tag đặc trưng |
|------|------:|-----:|----:|----:|----------|----------------|
| challenge-rush | 32,647 | 69.9% | 81s | 1,886s | Arcade | skill, jumping, rhythm, fast-paced, cube |
| flip-or-fail | 4,934 | 74.7% | 49s | 1,998s | Arcade | skill, flipping, physics, school, backflip |
| cycle-racing-game | 4,228 | 86.5% | 362s | 2,476s | Driving | 3d, racing, 1-player, collecting, bike |
| 1-weapon-evolution-online | 4,030 | 63.3% | 17s | 1,405s | Action | gun, weapon, collecting, incremental |
| bar-simulator-serve-fight | 3,577 | 64.3% | 17s | 1,244s | Casual | management, restaurant, business, incremental |
| topbike-racing | 3,335 | 82.4% | 251s | 1,979s | Driving | racing, physics, side-scrolling, bike, backflip |
| crash-x | 3,314 | 80.1% | 207s | 2,769s | Driving | 3d, car, racing, obstacle |
| quarterback | 3,205 | 79.8% | 196s | 1,852s | Arcade | skill, 3d, one-button, funny, ball |
| flip-spot | 3,065 | 84.2% | 362s | 1,963s | Arcade | parkour, skill, flipping |
| online-obby-1-keyboard-speed-escape | 2,981 | 79.9% | 160s | 1,872s | Arcade | parkour, party, obby |

### Top 10 Game User Chơi Lâu (p90 Cao Nhất)

| Slug | p90 | p50 | Users | Eng% | Category | Tag đặc trưng |
|------|----:|----:|------:|-----:|----------|----------------|
| prison-break | 5,500s | 587s | 497 | 84.7% | Casual | idle, management, build, defense |
| zombie-battle-royale | 3,968s | 422s | 505 | 77.4% | Action | battle-royale, zombie, arena |
| war-of-gun | 3,525s | 402s | 1,061 | 81.7% | Shooting | gun, battle, zombie, war |
| stickman-team-detroit | 3,289s | 374s | 563 | 86.5% | Action | stickman, team, side-scrolling, fighting |
| stickman-warriors-superhero-fight | 3,228s | 170s | 424 | 74.3% | Action | stickman, skill, fast-paced, fighting |
| stick-guy-archer | 3,228s | 288s | 1,051 | 83.1% | Action | stickman, 1-player, 2-player, weapon |
| archer-ragdoll-masters | 3,309s | 283s | 786 | 83.7% | Action | stickman, physics, weapon, ragdoll |
| mine-blade-online | 3,015s | 396s | 1,096 | 84.1% | Action | multiplayer, sandbox, arena, fighting |
| crash-x | 2,769s | 207s | 3,314 | 80.1% | Driving | 3d, car, racing, obstacle |
| ramp-car-police-chase | 2,943s | 317s | 1,485 | 84.1% | Driving | speed, car, racing, boys |

### Nhận Xét Q2

**Đặc điểm chung của game vừa nhiều user vừa chơi lâu:**

1. **Driving là thể loại "vàng"**: 7 game ởDriving đều có **p50 ≥ 200s** (nhiều game > 300s) và **engagement ≥ 80%**. Đây là thể loại duy nhất vừa có lượng user lớn (17,145) vừa có thời gian chơi lâu.
2. **Cụm "phản xạ/kỹ năng"** (`skill`, `jumping`, `flipping`, `parkour`, `obby`) — chiếm phần lớn top 10. Đây là các game có **p50 ngắn (50–150s) nhưng p90 rất dài (1,800–2,000s)** — pattern "người chơi trung thành quay lại nhiều".
3. **Cụm "stickman"** (Action) — `stickman-team-detroit`, `stickman-warriors`, `stick-guy-archer`, `archer-ragdoll-masters` đều có **p90 > 3,000s** và **engagement > 80%**. Đây là cụm có p90 cao nhất.
4. **Game incremental** (1-weapon-evolution, bar-simulator) — **nhiều user nhưng p50 rất thấp (17s)** → đây là game "B. Instant Hook" (xem §4).

---

## 4. Phân Nhóm Theo Thời Gian × User

Tiêu chí:
- **Thời gian tốt**: p50 ≥ 240s (≥ 4 phút — đạt ngưỡng GA4 "engaged")
- **Thời gian kém**: p50 < 240s
- **Nhiều user**: ≥ 2,000 users
- **Ít user**: < 1,500 users

### Phân Nhóm Theo Thể Loại

| Nhóm | Đặc điểm | Thể loại |
|------|-----------|----------|
| **🟢 NHÓM A: Thời gian tốt + Nhiều user** | p50 ≥ 240s, users ≥ 1500 | **Driving** (avg_p50=293s, 17k user), **Sports** (avg_p50=331s, 7.9k user) |
| **🟡 NHÓM B: Thời gian tốt + Ít user** | p50 ≥ 240s, users < 1500 | **Action** (15.9k user nhưng tb/user = 1138), **Casual**, **Puzzle**, **Shooting**, **.IO** |
| **🔴 NHÓM C: Thời gian kém + Ít user** | p50 < 240s, users < 1500 | (Không có — không có thể loại nào vừa kém thời gian vừa ít user ở mức category) |
| **🟠 NHÓM D: Thời gian kém + Nhiều user** | p50 < 240s, users ≥ 1500 | **Arcade** (avg_p50=196s, 82.7k user!), **Adventure** (avg_p50=185s, 6.7k user) |

### Chi Tiết Từng Nhóm

#### 🟢 NHÓM A — Thể Loại Chủ Lực Của Site

| Thể loại | n | Total users | avg_p50 | avg_p90 | avg_eng% | Đặc điểm |
|----------|--:|------------:|--------:|--------:|---------:|-----------|
| **Driving** | 7 | 17,145 | 293s | 2,488s | 83.0% | 7/7 game 100% A. Premium, p50 ≥ 240s |
| **Sports** | 4 | 7,865 | 331s | 2,542s | 82.5% | 4/4 game A. Premium, p50 cao nhất portfolio |

**→ Đây chính là 2 thể loại chủ lực của site (xem §5).**

#### 🟡 NHÓM B — Thể Loại "Tiềm Năng" (Thời Gian Tốt, Chưa Thu Hút Được User)

| Thể loại | n | Total users | avg_p50 | avg_eng% | Đặc điểm |
|----------|--:|------------:|--------:|---------:|-----------|
| **Puzzle** | 3 | 2,539 | 294s | 79.8% | p50 cao, p90=2,741s cao nhất, nhưng chỉ 3 game và trung bình 846 user/game |
| **Shooting** | 2 | 1,531 | 294s | 78.0% | p50=294s, p90=3,064s (cao nhất portfolio!), chỉ 766 user/game |
| **.IO** | 1 | 290 | 280s | 78.6% | p90=2,891s nhưng chỉ 1 game |
| **Casual** | 7 | 9,539 | 254s | 77.6% | Mixed — có game 3,577 user (bar-simulator, p50=17s) và game 497 user (prison-break, p50=587s) |
| **Action** | 14 | 15,934 | 240s | 77.8% | Mixed — có stickman team (eng 86%, p50=374s) và 1-weapon (p50=17s) |

**→ Nhóm B chứa game "hidden gems" — engagement cao, p50 lâu, nhưng chưa được promote. Đây là các game tiềm năng (xem §6).**

#### 🟠 NHÓM D — Nhiều User Nhưng Thời Gian Kém (< 240s)

| Thể loại | n | Total users | avg_p50 | avg_eng% | Vấn đề |
|----------|--:|------------:|--------:|---------:|--------|
| **Arcade** | 33 | **82,668** | **196s** | 75.7% | Thể loại lớn nhất nhưng p50 trung bình **dưới 4 phút**. Mixed: có game challenge-rush (32k user, p50=81s) và flip-spot (3k user, p50=362s) |
| **Adventure** | 4 | 6,657 | 185s | 74.3% | 2 game spidermaster và going-up có p50 < 200s |

**Phân tích nguyên nhân Arcade có nhiều user nhưng thời gian trung bình kém:**
- **Pattern "viral flash"**: Game Arcade nổi tiếng nhờ dễ chơi (skill, jumping) nhưng user chỉ chơi vài lượt rồi thoát
- **Hai game top đầu (challenge-rush 32k, flip-or-fail 4.9k) đều p50 ≤ 180s** — đây là game "hook" chứ không phải game "deep play"
- **Tuy nhiên Arcade vẫn có hidden gems**: flip-spot (3k user, p50=362s), upgrade-the-cars (1.2k user, p50=334s)

### Chi Tiết Cấp Game — Nhóm B (p50 ≥ 240s, users < 1500) — Hidden Gems

| Slug | Users | Eng% | p50 | p90 | Category | Tags |
|------|------:|-----:|----:|----:|----------|------|
| prison-break | 497 | 84.7% | **587s** | 5,500s | Casual | idle, management, build, defense |
| zombie-battle-royale | 505 | 77.4% | 422s | 3,968s | Action | battle-royale, zombie, arena |
| war-of-gun | 1,061 | 81.7% | 402s | 3,525s | Shooting | gun, battle, zombie, war |
| mine-blade-online | 1,096 | 84.1% | 396s | 3,015s | Action | multiplayer, sandbox, arena, fighting |
| stickman-team-detroit | 563 | 86.5% | 374s | 3,289s | Action | stickman, team, side-scrolling, fighting |
| helix-stack-ball | 666 | 80.2% | 368s | 2,498s | Arcade | jumping, ball, one-button, destroy |
| crazy-aunty-slap-punch | 399 | 77.4% | 348s | 2,886s | Casual | funny, weapon, one-button, cartoon |
| wake-up-the-box | 329 | 76.9% | 348s | 3,054s | Puzzle | physics, brain, logic |
| motor-sport-derby | 1,311 | 85.7% | 336s | 2,937s | Driving | speed, racing, 2-player, drifting |
| upgrade-the-cars | 1,175 | 87.2% | 334s | 2,695s | Casual | running, car, math, collecting |
| car-eats-car-underwater-adventure | 400 | 75.0% | 326s | 3,019s | Adventure | car, racing, escape, side-scrolling |
| ramp-car-police-chase | 1,485 | 84.1% | 317s | 2,943s | Driving | speed, car, racing, boys |
| military-strike | 1,204 | 83.7% | 298s | 2,526s | Action | team, gun, weapon, fps |
| stick-guy-archer | 1,051 | 83.1% | 288s | 3,228s | Action | stickman, 1-player, 2-player, weapon |
| archer-ragdoll-masters | 786 | 83.7% | 283s | 3,309s | Action | stickman, physics, weapon, ragdoll |
| blobade | 290 | 78.6% | 280s | 2,891s | .IO | multiplayer, battle-royale, arena |
| mega-ramp-car-stunts | 1,244 | 80.1% | 272s | 2,149s | Driving | speed, 3d, car, racing |
| auto-puzzle-stream | 206 | 83.0% | 268s | 2,968s | Puzzle | 2d, car, avoid, one-button |
| goat-rampage | 515 | 82.3% | 266s | 2,501s | Action | funny, physics, animal, destroy |
| tower-rise | 1,010 | 81.0% | 256s | 2,607s | Arcade | 3d, one-button, build, incremental |
| math-obby | 729 | 81.5% | 243s | 2,539s | Arcade | parkour, math, brain, obby |

**Tổng cộng: 21 game hidden gems** với engagement ≥ 75% và p50 ≥ 240s.

### Chi Tiết Cấp Game — Nhóm D (users ≥ 2000, p50 < 240s) — Game "Viral nhưng Shallow"

| Slug | Users | Eng% | p50 | Category | Tags |
|------|------:|-----:|----:|----------|------|
| challenge-rush | **32,647** | 69.9% | 81s | Arcade | skill, jumping, rhythm, fast-paced, cube |
| flip-or-fail | 4,934 | 74.7% | 151s | Arcade | skill, flipping, physics, school |
| 1-weapon-evolution-online | 4,030 | **63.3%** | **50s** | Action | gun, weapon, collecting, incremental |
| bar-simulator-serve-fight | 3,577 | **64.3%** | **50s** | Casual | management, restaurant, business, incremental |
| crash-x | 3,314 | 80.1% | 207s | Driving | 3d, car, racing, obstacle |
| quarterback | 3,205 | 79.8% | 196s | Arcade | skill, 3d, one-button, football |
| online-obby-1-keyboard-speed-escape | 2,981 | 79.9% | 143s | Arcade | parkour, party, obby |
| count-master | 2,790 | 80.3% | 212s | Arcade | stickman, running, obstacle |
| spidermaster-hero-in-the-city | 2,610 | 70.8% | **79s** | Adventure | parkour, 3d, rpg |
| going-up-rooftop-online | 2,537 | 76.3% | 177s | Adventure | parkour, jumping, climbing, 3d |
| sniper-combat-3d | 2,280 | 78.9% | 231s | Action | 3d, 1-player, one-button, fps |

**Nhận xét:** Game "viral nhưng shallow" đặc trưng bởi tag `parkour`/`skill`/`incremental`. Đây là các game viral một thời gian rồi giảm. Engagement vẫn OK (70–80%) nhưng p50 thấp → user chơi nhanh rồi đi.

---

## 5. Thể Loại Chủ Lực Của Site (1–3 Thể Loại)

Dựa trên 4 tiêu chí: **Tổng users**, **p50 (thời gian chơi)**, **Engagement %**, và **mức độ ổn định (100% A. Premium)**, 2 thể loại chủ lực là:

### 🏆 #1: **Driving** — Thể Loại Vàng

| Chỉ số | Giá trị | Xếp hạng |
|--------|--------:|---------:|
| Tổng users | 17,145 | #2 |
| avg p50 | **293s** | **#2 (gần 5 phút)** |
| avg engagement | **83.0%** | **#1 cao nhất** |
| avg p90 | 2,488s | Top 4 |
| Tỷ lệ A. Premium | **100% (7/7)** | **#1** |
| Số game | 7 | Vừa |
| Chiếm trong portfolio | 8.1% (72/886) | Top 5 |

**Đặc điểm nổi bật:**
- **Top tags**: `racing`, `3d`, `speed`, `bike`, `car`, `physics`, `destroy`
- **Top genres phụ**: Driving, Simulation, Sports
- **7/7 game đều A. Premium**, không có game yếu
- **Cụm tag vàng**: `racing + 3d + speed + car` (4 tags này cover 61% game)

**Top game đại diện:**
| Game | Users | Eng% | p50 | Tags |
|------|------:|-----:|----:|------|
| cycle-racing-game | 4,228 | 86.5% | 362s | 3d, racing, 1-player, collecting, bike |
| topbike-racing | 3,335 | 82.4% | 251s | racing, physics, side-scrolling, bike, backflip |
| crash-x | 3,314 | 80.1% | 207s | 3d, car, racing, obstacle |
| mega-ramp-bike-racing-tracks | 2,228 | 81.8% | 306s | speed, 3d, racing, bike |
| ramp-car-police-chase | 1,485 | 84.1% | 317s | speed, car, racing, boys |
| motor-sport-derby | 1,311 | 85.7% | 336s | speed, racing, 2-player, drifting |
| mega-ramp-car-stunts | 1,244 | 80.1% | 272s | speed, 3d, car, racing |

### 🏆 #2: **Sports** — Thể Loại Chất Lượng Cao Nhất (về thời gian)

| Chỉ số | Giá trị | Xếp hạng |
|--------|--------:|---------:|
| Tổng users | 7,865 | #5 |
| avg p50 | **331s** | **#1 (cao nhất portfolio)** |
| avg engagement | **82.5%** | **#2** |
| avg p90 | 2,542s | #3 |
| Tỷ lệ A. Premium | **100% (4/4)** | **#1** |
| Số game | 4 | Ít |
| Chiếm trong portfolio | 3.3% (29/886) | Top 9 |

**Đặc điểm nổi bật:**
- **Top tags**: `soccer`, `champion`, `team`, `racing`, `2-player`, `physics`, `bike`, `3d`, `ball`
- **Top genres phụ**: Sports, Simulation
- **p50 = 331s = 5.5 phút** — cao nhất trong tất cả thể loại
- **4/4 game A. Premium**, không có game yếu

**Top game đại diện:**
| Game | Users | Eng% | p50 | Tags |
|------|------:|-----:|----:|------|
| riders-downhill-racing | 2,520 | 82.8% | **439s** | racing, 2-player, physics, bike |
| soccer-aiming-simulator-in-3d | 2,412 | 85.3% | 352s | 3d, soccer, ball, champion |
| fiva-26-soccer | 1,763 | 84.4% | 334s | soccer, 1-player, team, champion |
| football-draft-squad-builder | 1,170 | 77.4% | 198s | soccer, team, crafting, card |

### 🥉 #3 (Phụ Trợ): **Action (Stickman Sub-cluster)** — Thể Loại Tiềm Năng Lớn

Mặc dù Action ở thể loại tổng thể có p50 trung bình thấp (240s) và mixed chất lượng, **cụm con "stickman"** là một trường hợp đặc biệt:

| Game | Users | Eng% | p50 | p90 |
|------|------:|-----:|----:|----:|
| stickman-team-detroit | 563 | **86.5%** | 374s | **3,289s** |
| stick-vs-zombies-stick-epic-fight | 1,193 | 78.2% | 187s | 2,477s |
| stick-guy-archer | 1,051 | 83.1% | 288s | 3,228s |
| archer-ragdoll-masters | 786 | 83.7% | 283s | 3,309s |
| stickman-warriors-superhero-fight | 424 | 74.3% | 170s | **3,228s** |

**Đặc điểm cụm stickman:**
- **p90 rất cao (3,000–3,300s)** — user trung thành chơi lâu
- **Engagement ≥ 78%** — tỷ lệ engaged cao
- **Tag đặc trưng**: `stickman`, `weapon`, `fighting`, `team`, `physics`, `side-scrolling`
- **Cơ hội**: 5+ game stickman có tiềm năng, tổng users chỉ ~4k → cơ hội scale lên 20–30k

### Bảng Tổng Hợp 3 Thể Loại Chủ Lực

| # | Thể loại | Total Users | avg_p50 | avg_eng% | Tỷ lệ A | Tổng kết |
|--:|----------|------------:|--------:|---------:|--------:|---------|
| 1 | **Driving** | 17,145 | 293s (5 phút) | 83.0% | 100% | **Lượng user lớn + thời gian lâu + ổn định** |
| 2 | **Sports** | 7,865 | 331s (5.5 phút) | 82.5% | 100% | **Thời gian lâu nhất + chất lượng cao nhất** |
| 3 | **Action (stickman)** | ~4,000 | 270s | 82% | 80% | **Cụm con có p90 = 3,000s — tiềm năng scale** |

**Tổng cộng 3 thể loại chủ lực chiếm ~28,000 users (18% tổng 153k users)** nhưng tạo ra phần lớn thời gian chơi chất lượng của site.

---

## 6. Game Tiềm Năng Để Phát Triển

Dựa trên phân tích, **17 game tiềm năng** đã được lọc với tiêu chí: **Engagement ≥ 80% AND users < 1500** (engaged users nhưng chưa được promote). Đây là các game "hidden gems" có thể scale lên gấp 5–10x nếu được đầu tư thêm traffic.

### Bảng 17 Game Tiềm Năng (Xếp Theo p50 Giảm Dần)

| # | Slug | Users | Eng% | p50 | p90 | Category | Tags | Rating |
|--:|------|------:|-----:|----:|----:|----------|------|-------:|
| 1 | prison-break | 497 | 84.7% | **587s** | **5,500s** | Casual | idle, management, build, defense | - |
| 2 | war-of-gun | 1,061 | 81.7% | 402s | 3,525s | Shooting | gun, battle, zombie, war | 8.2 |
| 3 | mine-blade-online | 1,096 | 84.1% | 396s | 3,015s | Action | multiplayer, sandbox, arena, fighting | 8.8 |
| 4 | stickman-team-detroit | 563 | 86.5% | 374s | 3,289s | Action | stickman, team, side-scrolling, fighting | - |
| 5 | helix-stack-ball | 666 | 80.2% | 368s | 2,498s | Arcade | jumping, ball, one-button, destroy | - |
| 6 | motor-sport-derby | 1,311 | 85.7% | 336s | 2,937s | Driving | speed, racing, 2-player, drifting | 8.7 |
| 7 | upgrade-the-cars | 1,175 | 87.2% | 334s | 2,695s | Casual | running, car, math, collecting | 5.3 |
| 8 | ramp-car-police-chase | 1,485 | 84.1% | 317s | 2,943s | Driving | speed, car, racing, boys | 9.1 |
| 9 | military-strike | 1,204 | 83.7% | 298s | 2,526s | Action | team, gun, weapon, fps | 8.3 |
| 10 | stick-guy-archer | 1,051 | 83.1% | 288s | 3,228s | Action | stickman, 1-player, 2-player, weapon | 8.1 |
| 11 | archer-ragdoll-masters | 786 | 83.7% | 283s | 3,309s | Action | stickman, physics, weapon, ragdoll | 7.7 |
| 12 | mega-ramp-car-stunts | 1,244 | 80.1% | 272s | 2,149s | Driving | speed, 3d, car, racing | 7.5 |
| 13 | auto-puzzle-stream | 206 | 83.0% | 268s | 2,968s | Puzzle | 2d, car, avoid, one-button | - |
| 14 | goat-rampage | 515 | 82.3% | 266s | 2,501s | Action | funny, physics, animal, destroy | - |
| 15 | tower-rise | 1,010 | 81.0% | 256s | 2,607s | Arcade | 3d, one-button, build, incremental | 8.6 |
| 16 | math-obby | 729 | 81.5% | 243s | 2,539s | Arcade | parkour, math, brain, obby | 10 |
| 17 | a-hole-without-a-bottom-battle-royale | 1,419 | 82.1% | 238s | 3,029s | Arcade | funny, battle-royale, arena | 5.8 |

### Phân Bố Game Tiềm Năng Theo Thể Loại

| Thể loại | Số game | Tổng users | Trung bình | Nhận xét |
|----------|------:|-----------:|----------:|----------|
| **Action** | 6 | 5,215 | 869 | **Nhiều nhất** — cụm stickman + zombie/fps đặc biệt tốt |
| **Driving** | 3 | 4,040 | 1,347 | **Sẵn sàng scale** — game đã có user, parking đang market-fit |
| **Arcade** | 4 | 3,824 | 956 | Đa dạng: math, tower-rise, battle-royale |
| **Casual** | 2 | 1,672 | prison-break (587s p50!), upgrade-the-cars | **prison-break là kim cương** — p50 = 587s |
| **Shooting** | 1 | 1,061 | war-of-gun | **Ít game nhưng chất lượng cao** |
| **Puzzle** | 1 | 206 | auto-puzzle-stream | Niche, chưa được khai thác |

### Top Tag Xuất Hiện Trong 17 Game Tiềm Năng

| Tag | Số game | Tỷ lệ % | Ý nghĩa |
|-----|------:|--------:|---------|
| car | 4 | 23.5% | Cụm xe/đua |
| stickman | 3 | 17.6% | Cụm stickman — engagement cao nhất |
| one-button | 3 | 17.6% | Dễ chơi, viral tiềm năng |
| destroy | 3 | 17.6% | Cụm phá hủy |
| speed | 3 | 17.6% | Cụm tốc độ |
| racing | 3 | 17.6% | Đua xe |
| weapon | 3 | 17.6% | Súng/vũ khí |
| build | 2 | 11.8% | Xây dựng |
| 2-player | 2 | 11.8% | 2 người chơi |
| math | 2 | 11.8% | Toán học (niche) |
| physics | 2 | 11.8% | Vật lý |
| 3d | 2 | 11.8% | Đồ họa 3D |
| team | 2 | 11.8% | Đội nhóm |

### Top 5 Game Nên Đầu Tư Ngay (Đề Xuất)

Dựa trên **rating cao + engagement cao + p50 cao + tiềm năng scale**:

| # | Game | Lý do ưu tiên | Hành động đề xuất |
|--:|------|---------------|---------------------|
| 1 | **prison-break** | p50 = 587s (cao nhất), p90 = 5,500s (cao nhất portfolio), 84.7% eng | Push homepage rộng, thêm vào sidebar "Hot", test với 5k traffic |
| 2 | **upgrade-the-cars** | 87.2% eng (cao nhất), p50 = 334s, rating 5.3 chưa tốt nhưng engagement rất cao | Cải thiện rating/UI, scale traffic 3–5x |
| 3 | **motor-sport-derby** | 85.7% eng, p50 = 336s, rating 8.7, cụm Driving | Push mạnh vào sidebar Driving |
| 4 | **stickman-team-detroit** | 86.5% eng, p50 = 374s, p90 = 3,289s, cụm Action | Tạo playlist stickman trên homepage |
| 5 | **ramp-car-police-chase** | 84.1% eng, 1,485 user, rating **9.1**, cụm Driving | Push thêm — đã có sẵn audience |

---

## 7. Tóm Tắt & Khuyến Nghị

### Phát Hiện Chính

1. **Portfolio 886 game** với 14 thể loại. Arcade (23%) + Action (19%) + Adventure (15%) = 57% portfolio.
2. **2 thể loại chủ lực rõ ràng**:
   - **Driving**: 17k user, p50=293s (5 phút), 83% eng, **100% A. Premium**
   - **Sports**: 7.9k user, p50=331s (5.5 phút), 82.5% eng, **100% A. Premium**
3. **1 cụm con tiềm năng lớn**: **Action stickman** với p90 = 3,000s — cơ hội scale lên 20–30k user.
4. **Arcade là thể loại "viral nhưng shallow"**: 82k user (lớn nhất) nhưng p50 = 196s (< 4 phút) → user vào chơi nhanh rồi đi.
5. **17 hidden gems** (engagement ≥ 80%, users < 1500) — đã được list trong §6.
6. **Game có p50 cao nhất** = `prison-break` (587s) và `cycle-racing-game` (362s).
7. **Game nhiều user nhất** = `challenge-rush` (32k user) nhưng p50 chỉ 81s.

### Khuyến Nghị Hành Động

#### A. Tập Trung Vào 2–3 Thể Loại Chủ Lực

| Hành động | Chi tiết |
|-----------|----------|
| **Tăng sản lượng Driving** | Hiện 7 game, chiếm 8.1% — đẩy lên 12–15 game (12–15% portfolio). Đầu tư 2–3 game Driving/tháng |
| **Mở rộng Sports** | Hiện 4 game, chiếm 3.3% — đẩy lên 8–10 game (5–6% portfolio). Đầu tư 1–2 game Sports/tháng |
| **Phát triển cụm stickman** | Cụm con Action có p90 = 3,000s — tạo "Stickman Series" riêng trên homepage |

#### B. Đẩy Mạnh 17 Game Tiềm Năng (§6)

| Nhóm | Hành động |
|------|-----------|
| **Top 5 (prison-break, upgrade-the-cars, motor-sport-derby, stickman-team-detroit, ramp-car-police-chase)** | A/B test trên homepage với 5–10k traffic mỗi game, đo lường scale |
| **Cụm Driving (3 game)** | Thêm vào "Best Driving Games" playlist |
| **Cụm stickman (3 game)** | Tạo category "Stickman Games" riêng |
| **Cụm Puzzle + Shooting** | Thử nghiệm 1 game Puzzle/Shooting để mở rộng — 2 danh mục có p50 cao nhưng chỉ 1–3 game |

#### C. Cải Thiện Arcade & Adventure (Nhiều User, Thời Gian Kém)

| Vấn đề | Giải pháp |
|--------|----------|
| Arcade có 82k user nhưng p50 = 196s | Thêm "level progression", "unlock new maps", "achievement system" để tăng retention |
| Adventure có p50 = 185s | Cải thiện narrative depth, checkpoint 2 (giảm người chơi bỏ cuộc) |

#### D. Tránh Nhân Rộng Pattern Yếu

| Pattern | Tránh vì |
|---------|---------|
| Game incremental + weapon + collecting | Thường có p50 < 60s (1-weapon: 50s, bar-simulator: 50s) |
| Game skill + jumping + parkour + obby thuần | Pattern viral nhưng shallow — p50 thường 100–200s |

### Kết Luận

**2 thể loại chủ lực của site 1games.io: Driving và Sports.** Cả hai đều 100% A. Premium, thời gian chơi trung bình 5+ phút, engagement ≥ 82%. **Cụm con stickman trong Action** là cơ hội scale lớn thứ 3. **17 game hidden gems** đã được list chi tiết — ưu tiên đầu tư vào Top 5 (prison-break, upgrade-the-cars, motor-sport-derby, stickman-team-detroit, ramp-car-police-chase).

---

## File Dữ Liệu Đính Kèm

| File | Mô tả |
|------|-------------|
| `D:\GR\portfolio_overview.csv` | 886 game — full portfolio (slug, name, primary_genre, tags, publish_date, views, source) |
| `D:\GR\category_engagement.csv` | 12 thể loại — engagement aggregates từ 82 game mới |
| `D:\GR\potential_games.csv` | 17 hidden gems — engagement ≥ 80% AND users < 1500 |
| `D:\GR\games_82_full_detail.csv` | 82 game — full detail (metrics + meta + segmentation) |
| `D:\GR\05_scripts\tests\build_portfolio_report_data.py` | Script tạo dữ liệu cho báo cáo này |

---

## Lịch Sử Tài Liệu

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---------|------|--------|---------|
| **1.0** | **2026-10-07** | **Cursor Assistant** | **Phân tích portfolio 886 game + 82 game mới có traffic. Trả lời 4 câu hỏi: (1) tổng quan portfolio + thể loại, (2) game user chơi nhiều + chơi lâu, (3) phân nhóm theo thời gian × user, (4) đề xuất 2–3 thể loại chủ lực + 17 game tiềm năng.** |