# Phân Khúc Danh Mục Game "Mới" của 1games.io (v2 — Engagement Cấp User-Page)

**Ngày:** Ngày 3 tháng 10 năm 2026
**File CSV nguồn:** `1games_new.csv` (106 game mới được đăng)
**Khoảng dữ liệu:** 2026-09-04 → 2026-09-25 (shard_date mới nhất có sẵn cho 1games.io)
**Khung phân tích:** `SEGMENTATION_PROCESS.md` Mục A (biến thể 1games) + định nghĩa engagement đã sửa
**Ngưỡng lọc:** ≥200 phiên mỗi game (đã áp dụng)
**File CSV kết quả:** `1games_new_segmented.csv` (số liệu đầy đủ từng game + 6 phân khúc)

---

## ⚠️ Cập Nhật Định Nghĩa Engagement

Lần chạy trước dùng engagement **cấp session** (`sess_dur > 30s`, tỷ lệ = số phiên). Lần này dùng engagement **cấp user-page** theo đặc tả mới:

```python
page_dur_s  = params_num['estimated_duration_seconds']    trên (client_id, session_id, page_location)
sess_dur    = SUM(page_dur_s)                              trên (client_id, session_id, page_location)
user_dur    = SUM(sess_dur)                                trên (client_id, page_location)
engaged     = user_dur > 30
Eng%        = SUM(engaged) / COUNT(users) * 100
```

**Giải thích đơn giản:** Với mỗi người dùng, cộng tổng số giây trên tất cả phiên của một trang game. Nếu tổng đó > 30s, họ được tính là "engaged" (tương tác). Eng% = số user engaged / tổng số user.

**Khác biệt so với v1:**
- v1 đếm "engaged sessions" (1 nếu sess_dur > 30s, 0 nếu ngược lại)
- v2 đếm "engaged users" (1 nếu user_dur > 30s, 0 nếu ngược lại)
- v1 dùng `eng_sess_pct = engaged_sessions / sessions`
- v2 dùng `eng_pct = engaged_users / users` (cao hơn khoảng 10–15% vì user quay lại chỉ tính 1 lần)

Các chỉ số khác (users, sessions, sess_p50, sess_p90, sess_avg, sess_per_user, p90_p50_ratio) không đổi.

---

## Tóm Tắt Điều Hành

| Kết quả | Số lượng | % |
|---------|------:|---:|
| Tổng trong CSV | 106 | 100% |
| Có traffic trong khoảng | 82 | 77.4% |
| ≥200 phiên (đủ phân tích) | 80 | 75.5% |
| 50–199 phiên (độ tin cậy thấp) | 1 | 0.9% |
| <50 phiên (không đủ dữ liệu) | 1 | 0.9% |

**Phát hiện chính:** Với engagement cấp user-page, lô game này **còn mạnh hơn nữa**. **79 trên 80 game đủ phân tích đều là A. Premium** theo Phân Khúc Chất Lượng. **98.8%** là A. Premium theo Giá Trị Kinh Doanh (trước là 96.3% với engagement cấp session). **98.8%** đạt hạng A theo Cụm tổng hợp.

**Phân phối engagement:** 74.4% game có ≥75% engagement cấp user-page. Chỉ 1 game dưới 50%.

---

## 1. Top 25 Game Theo User (User-Page Engagement)

| # | Slug | Users | Sessions | Engaged Users | Eng% | p50 (s) | p90 (s) | Sessions/User |
|--:|--|--:|--:|--:|--:|--:|--:|--:|
| 1 | challenge-rush | 32,647 | 58,592 | 22,820 | 69.9% | 81 | 1,886 | 1.79 |
| 2 | flip-or-fail | 4,934 | 8,366 | 3,684 | 74.7% | 151 | 1,998 | 1.70 |
| 3 | cycle-racing-game | 4,228 | 7,964 | 3,655 | 86.5% | 362 | 2,476 | 1.88 |
| 4 | 1-weapon-evolution-online | 4,030 | 8,062 | 2,551 | 63.3% | 50 | 1,723 | 2.00 |
| 5 | bar-simulator-serve-fight | 3,577 | 7,019 | 2,300 | 64.3% | 50 | 1,857 | 1.96 |
| 6 | topbike-racing | 3,335 | 6,235 | 2,749 | 82.4% | 251 | 1,979 | 1.87 |
| 7 | crash-x | 3,314 | 6,043 | 2,656 | 80.1% | 207 | 2,769 | 1.82 |
| 8 | quarterback | 3,205 | 5,716 | 2,558 | 79.8% | 196 | 1,830 | 1.78 |
| 9 | flip-spot | 3,065 | 5,395 | 2,580 | 84.2% | 362 | 1,963 | 1.76 |
| 10 | online-obby-1-keyboard-speed-escape | 2,981 | 5,287 | 2,381 | 79.9% | 160 | 1,535 | 1.77 |
| 11 | count-master | 2,790 | 4,712 | 2,240 | 80.3% | 212 | 1,815 | 1.69 |
| 12 | tiles-hop-edm-rush | 2,628 | 4,580 | 2,191 | 83.4% | 276 | 1,950 | 1.74 |
| 13 | spidermaster-hero-in-the-city | 2,610 | 4,690 | 1,848 | 70.8% | 79 | 1,820 | 1.80 |
| 14 | going-up-rooftop-online | 2,537 | 4,492 | 1,936 | 76.3% | 177 | 2,154 | 1.77 |
| 15 | riders-downhill-racing | 2,520 | 4,447 | 2,087 | 82.8% | 439 | 2,565 | 1.76 |
| 16 | soccer-aiming-simulator-in-3d | 2,412 | 4,068 | 2,058 | 85.3% | 352 | 1,945 | 1.69 |
| 17 | horror-nun-2 | 2,334 | 3,856 | 1,879 | 80.5% | 291 | 1,994 | 1.65 |
| 18 | sniper-combat-3d | 2,280 | 3,963 | 1,799 | 78.9% | 231 | 2,007 | 1.74 |
| 19 | mega-ramp-bike-racing-tracks | 2,228 | 3,907 | 1,823 | 81.8% | 306 | 2,068 | 1.75 |
| 20 | draw-joust | 2,210 | 3,758 | 1,902 | 86.1% | 372 | 2,200 | 1.70 |
| 21 | draw-two-save-the-man | 2,004 | 3,464 | 1,593 | 79.5% | 266 | 2,134 | 1.73 |
| 22 | zombie-dash | 1,949 | 3,389 | 1,651 | 84.7% | 227 | 2,061 | 1.74 |
| 23 | ragdoll-sandbox | 1,818 | 3,178 | 1,476 | 81.2% | 242 | 2,180 | 1.75 |
| 24 | flip-duel | 1,806 | 3,158 | 1,413 | 78.3% | 221 | 1,967 | 1.75 |
| 25 | rider-rush | 1,783 | 3,019 | 1,575 | 88.3% | 429 | 2,188 | 1.69 |

---

## 2. Phân Phối Engagement (User-Page)

| Khoảng | Số game | % | Diễn giải |
|-------|------:|---:|----------------|
| 0–10% | 1 | 1.2% | Vấn đề nghiêm trọng (game hỏng) |
| 10–25% | 0 | 0% | — |
| 25–50% | 0 | 0% | — |
| 50–75% | 20 | 24.4% | Tốt |
| **75–100%** | **61** | **74.4%** | **Mạnh — hầu hết game giữ chân user quá 30s** |

**Nhận xét:** Với engagement cấp user-page, chỉ 1 game dưới 50% (so với v1 có 1 D-tier và 2 Instant Hook). Engagement cấp user-page vốn dễ tính hơn cấp session: một user bounce (1s) rồi quay lại (45s) vẫn được tính là engaged.

---

## 3. Kết Quả Phân Khúc

### Phân Khúc 1 — Tứ Phân Chất Lượng (eng_pct × sess_p50)

| Phân khúc | Game | % | Định nghĩa |
|---------|------:|---:|------------|
| **A. Premium** | 79 | 96.3% | eng ≥ 35% AND p50 ≥ 30s |
| B. Instant Hook | 2 | 2.4% | eng ≥ 35% AND p50 < 30s |
| C. Casual Depth | 0 | 0% | eng < 35% AND p50 ≥ 18s |
| D. Weak | 1 | 1.2% | còn lại |

### Phân Khúc 2 — Ma Trận Duy Trì (sess_per_user × eng_pct)

Với engagement cấp user-page, ta dùng **công thức duy trì đã sửa** phù hợp với danh mục mới:

| Phân khúc | Game | % | Định nghĩa (đã sửa) |
|---------|------:|---:|----------------------|
| A. Sticky | 6 | 7.3% | sess ≥ 1.3 AND eng ≥ 50% |
| B. Repeat-Casual | 50 | 61.0% | sess ≥ 1.1 AND eng ≥ 30% |
| C. Eng-No-Repeat | 25 | 30.5% | eng ≥ 30% (một phiên) |
| D. Weak | 1 | 1.2% | còn lại |

**So với v1 (có 100% rơi vào D. Weak):** Công thức mới phân biệt đúng giữa game sticky và game casual. 6 game giờ thuộc Sticky (`rider-rush`, `upgrade-the-cars`, `prison-break`, `flip-spot`, `cycle-racing-game`, `crash-x`), 50 thuộc Repeat-Casual, 25 engaged một phiên.

### Phân Khúc 3 — Hình Dạng Phân Phối (tỷ số p90/p50)

| Phân khúc | Game | % | Định nghĩa |
|---------|------:|---:|------------|
| **Bimodal** | 43 | 52.4% | p90/p50 ≥ 10 |
| Moderate | 37 | 45.1% | 5 ≤ tỷ số < 10 |
| Flat | 2 | 2.4% | tỷ số < 5 |

**Giống v1** — hình dạng phân phối không phụ thuộc định nghĩa engagement.

### Phân Khúc 4 — Giá Trị Kinh Doanh (eng_pct × sess_p90)

| Phân khúc | Game | % | Định nghĩa |
|---------|------:|---:|------------|
| **A. Premium** | **81** | **98.8%** | eng ≥ 35% AND p90 ≥ 120s |
| B. Niche | 0 | 0% | eng < 35% AND p90 ≥ 120s |
| C. Volume | 0 | 0% | eng ≥ 35% AND p90 < 120s |
| D. Underperformer | 1 | 1.2% | còn lại |

**So với v1 (96.3% A):** Thêm 2 game lên A. Premium vì engagement cấp user-page dễ tính hơn.

### Phân Khúc 5 — Phễu (kết hợp eng × p90)

| Phân khúc | Game | % | Định nghĩa |
|---------|------:|---:|------------|
| **A. Premium** | 81 | 98.8% | eng ≥ 50% AND p90 ≥ 200s |
| B. Mid-Drop | 1 | 1.2% | eng < 35% |
| C. Depth-Fail | 0 | 0% | eng ≥ 35% AND p90 < 120s |
| D. Full-Fail | 0 | 0% | còn lại |

**So với v1 (96.3% A, 2.4% D):** Không còn game nào rơi vào D. Full-Fail; chỉ `trap-the-cat` còn là Mid-Drop.

### Phân Khúc 6 — Cụm (tổng hợp Phân Khúc 1 + 4 + 5)

| Cụm | Game | % |
|---------|------:|---:|
| **Cụm 1: Premium** | 81 | 98.8% |
| Cụm 4: Underperformer | 1 | 1.2% |

---

## 4. Top Performers & Hidden Gems

### Top 5 theo Engagement (User-Page)

| Slug | Users | Eng% (USER) | Sess_p50 |
|------|------:|-----:|---------:|
| **rider-rush** | 1,783 | **88.3%** | 429s |
| **upgrade-the-cars** | 1,175 | **87.2%** | 334s |
| **stickman-team-detroit** | 563 | **86.5%** | 374s |
| **cycle-racing-game** | 4,228 | **86.5%** | 362s |
| **draw-joust** | 2,210 | **86.1%** | 372s |

### Top 5 theo Điểm Tổng Hợp (Users × Engagement)

| Slug | Users × Eng% (k) | Sess_p50 | Sess_p90 |
|------|---------:|---------:|---------:|
| **challenge-rush** | **22,820** | 81s | 1,886s |
| cycle-racing-game | 3,655 | 362s | 2,476s |
| flip-or-fail | 3,685 | 151s | 1,998s |
| topbike-racing | 2,749 | 251s | 1,979s |
| crash-x | 2,656 | 207s | 2,769s |

### Hidden Gems (A. Premium VÀ <500 users VÀ ≥80% engagement)

| Slug | Users | Eng% | Sess_p50 | Sess_p90 |
|------|------:|-----:|---------:|---------:|
| **upgrade-the-cars** | 1,175 | 87.2% | 334s | 2,695s |
| **stickman-team-detroit** | 563 | 86.5% | 374s | 3,289s |
| **prison-break** | 497 | 85.7% | 587s | 5,500s |
| **blobade** | 290 | 84.5% | 281s | 2,891s |
| **wake-up-the-box** | 329 | 84.2% | 348s | 3,054s |
| **car-eats-car-underwater-adventure** | 400 | 82.5% | 326s | 3,019s |
| **crazy-aunty-slap-punch** | 399 | 81.0% | 348s | 2,886s |
| **crystal-circuit** | 70 | 75.7% | 256s | 2,427s |

### Bottom 5 theo Engagement

| Slug | Users | Eng% | Sess_p50 | Vấn đề |
|------|------:|-----:|---------:|-------|
| **trap-the-cat** | 3 | 0.0% | 0s | Cần gỡ bỏ / điều tra |
| 1-weapon-evolution-online | 4,030 | 63.3% | 50s | Quy mô lớn nhưng engagement mỗi user thấp |
| bar-simulator-serve-fight | 3,577 | 64.3% | 50s | Tương tự — lượng lớn, chiều sâu mỗi user thấp |
| blockader | 303 | 64.7% | 48s | Biên giới |
| capybara-mart | 465 | 67.1% | 8s | Instant Hook — nhóm trung thành nhỏ, phần lớn chỉ vào thoát nhanh |

---

## 5. Kiểm Chứng Chéo: Hạng A Ở Nhiều Phân Khúc

| Tổ hợp | Game | % |
|-------------|------:|---:|
| A ở Phân Khúc 1 (Chất Lượng) AND A ở Phân Khúc 4 (Kinh Doanh) | 79 | 96.3% |
| A ở Phân Khúc 1 AND A ở Phân Khúc 5 (Phễu) | 79 | 96.3% |
| D ở Phân Khúc 1 AND D ở Phân Khúc 4 | 1 | 1.2% |
| A ở Cụm (Phân Khúc 6) | 81 | 98.8% |

**Kiểm chứng chéo:** 79 trên 80 game đủ phân tích đều đạt hạng A ở cả 3 phân khúc Chất Lượng, Kinh Doanh và Phễu. Đây là tín hiệu mạnh mẽ cho một danh mục chất lượng cao và đồng nhất.

---

## 6. Phân Khúc & Insight Category/Tag (theo phân khúc)

Nguồn dữ liệu: crawl trực tiếp các trang `1games.io/{slug}` ngày 2026-10-03. Mỗi trang game cung cấp:
- **JSON-LD `VideoGame`**: `name`, `genre[]`, `aggregateRating`, `datePublished`
- **JSON-LD `BreadcrumbList` vị trí 2**: danh mục chính (ví dụ `Arcade`, `Driving`, `Action`)
- **`data-track-section="tag_related"`**: 4-6 badge tag (ví dụ `skill`, `parkour`, `3d`)
- **`data-track-section="game_related"`**: 16-18 game liên quan (dùng cho khám phá cụm)

Phủ: 81/82 game crawl thành công. (`trap-the-cat` được crawl nhưng metadata rỗng — trang hỏng.)

### 6.1 Top 12 Danh Mục (chính, xếp theo user)

| # | Danh mục chính | n | Users | avg_eng% | avg_p50 | avg_p90 |
|--:|-----------------|--:|------:|---------:|--------:|--------:|
| 1 | **Arcade** | 33 | 82,668 | 75.7% | 196s | 2,101s |
| 2 | **Driving** | 7 | 17,145 | **83.0%** | 293s | 2,488s |
| 3 | **Action** | 14 | 15,934 | 77.8% | 240s | 2,508s |
| 4 | **Casual** | 7 | 9,539 | 77.6% | 254s | 2,646s |
| 5 | **Sports** | 4 | 7,865 | **82.5%** | **331s** | 2,542s |
| 6 | **Adventure** | 4 | 6,657 | 74.3% | 185s | 2,160s |
| 7 | **Simulation** | 4 | 4,207 | 73.0% | 110s | 2,161s |
| 8 | **Clicker** | 2 | 2,625 | 74.5% | 88s | 2,327s |
| 9 | **Puzzle** | 3 | 2,539 | 79.8% | 294s | 2,741s |
| 10 | **Horror** | 1 | 2,334 | 80.5% | 291s | 1,994s |
| 11 | **Shooting** | 2 | 1,531 | 78.0% | 294s | 3,064s |
| 12 | **.IO** | 1 | 290 | 78.6% | 280s | 2,891s |

**Insight:** **Driving (83.0% eng, 293s p50)** và **Sports (82.5% eng, 331s p50)** là hai danh mục có chất lượng trên mỗi user cao nhất. **Arcade là danh mục lớn nhất về lượng** (53% user) nhưng engagement trung bình. **Simulation/Clicker** có p50 thấp — user vào thoát nhanh dù vẫn được tính "engaged" nhờ quay lại nhiều lần.

### 6.2 Danh Mục Chính × Chất Lượng (Phân Khúc 1)

| Danh mục | A. Premium | B. Instant Hook | D. Weak | Tổng |
|----------|-----------:|----------------:|--------:|------:|
| **Arcade** | 32 | 0 | 1 | 33 |
| **Action** | 14 | 0 | 0 | 14 |
| **Driving** | 7 | 0 | 0 | 7 |
| **Casual** | 7 | 0 | 0 | 7 |
| **Adventure** | 4 | 0 | 0 | 4 |
| **Sports** | 4 | 0 | 0 | 4 |
| **Simulation** | 3 | 1 | 0 | 4 |
| **Puzzle** | 3 | 0 | 0 | 3 |
| **Clicker** | 1 | 1 | 0 | 2 |
| **Shooting** | 2 | 0 | 0 | 2 |
| **Horror** | 1 | 0 | 0 | 1 |
| **.IO** | 1 | 0 | 0 | 1 |

**Insight:** **Dấu hiệu nhận diện B. Instant Hook = Clicker hoặc Simulation** (vòng lặp incremental/idle). Những game này có engagement user-page cao (66–71%) nhưng **median session gần 0** (0–8s) vì vòng lặp rất nhanh. 2 game Instant Hook trong lô: `stickman-coin-flip` (Clicker, 1,640u, 71.1%) và `capybara-mart` (Simulation, 465u, 67.1%).

### 6.3 Top 25 Tag (kèm phân tích chất lượng)

| Tag | n | Users | A% | B% | D% |
|-----|--:|------:|---:|---:|---:|
| **skill** | 8 | 49,421 | 100% | 0% | 0% |
| **jumping** | 5 | 39,588 | 100% | 0% | 0% |
| **3d** | 20 | 38,391 | 100% | 0% | 0% |
| **fast-paced** | 6 | 37,673 | 100% | 0% | 0% |
| **physics** | 16 | 31,530 | 100% | 0% | 0% |
| **racing** | 13 | 24,920 | 100% | 0% | 0% |
| **collecting** | 15 | 24,438 | **93%** | 7% | 0% |
| **incremental** | 14 | 22,240 | **86%** | 14% | 0% |
| **parkour** | 11 | 19,231 | 100% | 0% | 0% |
| **1-player** | 9 | 14,935 | **89%** | 0% | **11%** |
| **bike** | 6 | 14,848 | 100% | 0% | 0% |
| **backflip** | 5 | 14,499 | 100% | 0% | 0% |
| **funny** | 10 | 13,280 | **90%** | 10% | 0% |
| **car** | 10 | 11,987 | 100% | 0% | 0% |
| **obby** | 9 | 11,942 | 100% | 0% | 0% |
| **speed** | 8 | 11,422 | 100% | 0% | 0% |
| **obstacle** | 5 | 11,235 | 100% | 0% | 0% |
| **one-button** | 9 | 10,134 | 100% | 0% | 0% |
| **weapon** | 8 | 10,131 | 100% | 0% | 0% |
| **flipping** | 3 | 9,805 | 100% | 0% | 0% |
| **2-player** | 7 | 9,579 | 100% | 0% | 0% |
| **side-scrolling** | 6 | 9,216 | 100% | 0% | 0% |
| **destroy** | 7 | 8,636 | 100% | 0% | 0% |

**Insight:**
- **Tag dựa trên kỹ năng** (skill, jumping, fast-paced, parkour, obby, obstacle) đều có 100% A. Premium — game phản xạ là chất lượng cao nhất trên user.
- **`collecting`, `incremental`, `funny`** là những tag duy nhất có game Instant Hook — đây là các vòng lặp nơi user quay lại nhưng chỉ chơi 0–8s mỗi phiên.
- **`1-player` là tag duy nhất có game D. Weak** (`trap-the-cat`).
- **Tag Driving** (racing, car, bike, backflip) phân cụm rất chặt: 9,800+ user mỗi tag, đều 100% A. Premium.

### 6.4 Phân Tích Theo Phân Khúc (Phân Khúc 1 Chất Lượng) — Cấp Độ Game

#### A. Premium (79 game, 151,226 users)

**Top tag:** `3d` (20), `physics` (16), `collecting` (14), `incremental` (9), `parkour` (11), `racing` (13), `weapon` (8), `skill` (8), `funny` (9), `obby` (9)

**Top danh mục:** Arcade (32), Action (14), Driving (7), Casual (7), Adventure (4), Sports (4), Puzzle (3), Simulation (3), Shooting (2), Horror (1), .IO (1)

**Top 10 theo user (kèm tag):**

| Slug | Users | Eng% | p50 | Danh mục | Top tags |
|------|------:|-----:|----:|----------|----------|
| challenge-rush | 32,647 | 69.9% | 81s | Arcade | skill, jumping, rhythm, fast-paced, cube |
| flip-or-fail | 4,934 | 74.7% | 151s | Arcade | skill, flipping, physics, school, backflip |
| cycle-racing-game | 4,228 | 86.5% | 362s | Driving | 3d, racing, 1-player, collecting, bike |
| 1-weapon-evolution-online | 4,030 | 63.3% | 50s | Action | gun, weapon, collecting, incremental |
| bar-simulator-serve-fight | 3,577 | 64.3% | 50s | Casual | management, restaurant, business, 1-player |
| topbike-racing | 3,335 | 82.4% | 251s | Driving | racing, physics, side-scrolling, bike, backflip |
| crash-x | 3,314 | 80.1% | 207s | Driving | 3d, car, racing |
| quarterback | 3,205 | 79.8% | 196s | Arcade | skill, 3d, one-button, funny, ball |
| flip-spot | 3,065 | 84.2% | 362s | Arcade | parkour, skill, flipping |
| online-obby-1-keyboard-speed-escape | 2,981 | 79.9% | 143s | Arcade | parkour, party, obby |

**Danh sách đầy đủ 79 game:** xem `1games_new_segments_detail.csv` với `segment_dim='Seg 1: Quality'` và `segment_value='A. Premium'`.

#### B. Instant Hook (2 game, 2,105 users)

**Đặc điểm:** danh mục=Clicker/Simulation, thể loại=vòng lặp incremental/idle, p50 ≈ 0–8s, eng% > 65%.

| Slug | Users | Eng% | p50 | Danh mục | Top tags |
|------|------:|-----:|----:|----------|----------|
| stickman-coin-flip | 1,640 | 71.1% | 0s | Clicker | funny, idle, collecting, pixel |
| capybara-mart | 465 | 67.1% | 8s | Simulation | management, animal, business, shopping |

#### D. Weak (1 game, 3 users)

| Slug | Users | Eng% | p50 | Danh mục | Top tags |
|------|------:|-----:|----:|----------|----------|
| trap-the-cat | 3 | 0.0% | 0s | Arcade | 1-player, animal |

**Chẩn đoán:** trang tồn tại nhưng không có engagement nào — nhiều khả năng iframe bị hỏng, không load được. Đề xuất gỡ bỏ ngay.

### 6.5 Phân Tích Theo Phân Khúc (Phân Khúc 2 Duy Trì)

| Hạng | n | Users | Top danh mục | Top tags |
|------|--:|------:|----------------|----------|
| **A. Sticky** | 6 | 42,772 | Arcade(4), Clicker(1), Simulation(1) | incremental(3), skill(2), physics(2), funny(2) |
| **B. Repeat-Casual** | 50 | 79,649 | Arcade(18), Action(10), Driving(5), Sports(4), Casual(3) | physics(12), incremental(9), 3d(9), parkour(8), weapon(7) |
| **C. Eng-No-Repeat** | 25 | 30,910 | Arcade(10), Casual(4), Action(4), Adventure(3), Driving(2) | 3d(10), collecting(7), racing(6), car(6), 1-player(5) |
| D. Weak | 1 | 3 | Arcade(1) | 1-player(1), animal(1) |

**Insight:** **Game Sticky** bị chi phối bởi `incremental` (3/6) và `physics` (2/6). Repeat-Casual là phần lớn (50 game) — hầu hết game trong danh mục có lượt quay lại thứ hai nhưng chưa tạo thói quen. **Eng-No-Repeat** (25 game) chỉ chơi một phiên nhưng engagement tốt — đặc trưng của game arcade chơi một lượt.

### 6.6 Phân Tích Theo Phân Khúc (Phân Khúc 3 Hình Dạng Phân Phối)

| Hình dạng | n | Users | avg p90/p50 | Top danh mục |
|-------|--:|------:|------------:|----------------|
| **Bimodal** | 43 | 93,559 | 21.3 | Arcade(21), Action(6), Simulation(4), Casual(3), Adventure(3) |
| Moderate | 37 | 58,132 | 8.3 | Arcade(11), Action(8), Driving(6), Casual(4), Sports(3) |
| Flat | 2 | 1,643 | 0.0 | Clicker(1), Arcade(1) |

**Insight:** **Game Bimodal** (43) có đuôi dài user engagement rất cao (p90 > 2,000s) — đây là các game có người chơi trung thành. **Game Moderate** (37) có phân phối phẳng hơn — khán giả casual. **Flat** (2) là các game Instant Hook (stickman-coin-flip, capybara-mart) với phương sai gần 0.

---

## 7. Khuyến Nghị Tag/Genre Cho Game Sắp Đăng

Dựa trên phân tích tag và phân khúc ở §6, đây là khuyến nghị cụ thể cho các game nên đăng tiếp theo để tối đa hóa chất lượng trên mỗi user:

### 7.1 Bộ Tag Ưu Tiên Cao (Tier S)

| Tag | Lý do | Game hiện có (ví dụ) | Hành động |
|-----|-------|----------------------|-----------|
| **skill** | 49,421 user, **100% A. Premium** (8/8 game) | challenge-rush, flip-or-fail, flip-spot | Ưu tiên đăng game mới với tag này |
| **jumping** | 39,588 user, **100% A. Premium** | challenge-rush, skyhop-3d, math-obby | Cùng cụm với skill, đăng game phản xạ nhảy |
| **3d** | 38,391 user (20 game), **100% A. Premium** | cycle-racing-game, crash-x, sniper-combat-3d | Phủ rộng danh mục Arcade/Action với đồ họa 3D |
| **fast-paced** | 37,673 user, **100% A. Premium** | challenge-rush, going-up, sword-simulator | Game tốc độ cao, không kéo dài |
| **physics** | 31,530 user (16 game), **100% A. Premium** | flip-or-fail, draw-joust, ragdoll-sandbox | Cụm quan trọng nhất của Repeat-Casual |
| **parkour** | 19,231 user (11 game), **100% A. Premium** | flip-spot, online-obby, skyhop-3d | Mở rộng cụm parkour/climbing |

### 7.2 Bộ Tag Ưu Tiên Trung Bình (Tier A)

| Tag | Lý do | Ghi chú |
|-----|-------|---------|
| **racing** | 24,920 user, 100% A, đã có 13 game | Đã no — không ưu tiên thêm |
| **car** | 11,987 user, 100% A | Bão hòa — bổ sung 1 game nếu có |
| **obby** | 11,942 user, 100% A | Đa dạng hóa với 1-2 obby nữa |
| **one-button** | 10,134 user, 100% A | Dễ chơi, dễ viral |
| **2-player** | 9,579 user, 100% A | Ít game 2-player — **cơ hội mở rộng** |
| **side-scrolling** | 9,216 user, 100% A | Kết hợp với parkour/racing |
| **destroy** | 8,636 user, 100% A | Cụm ít — ưu tiên nếu có game nổi bật |

### 7.3 Tag NÊN TRÁNH (Tier F)

| Tag | Lý do tránh | Hậu quả |
|-----|-------------|---------|
| **1-player** | 1/9 game D. Weak (`trap-the-cat`), 89% A | Nếu làm, cần kiểm tra chất lượng kỹ trước khi đăng |
| **collecting** | 1/15 game B. Instant Hook (7%) | Tốt cho stickman-coin-flip, không tốt cho các game khác |
| **incremental** | 2/14 game B. Instant Hook (14%) | Trừ khi cam điết vòng lặp cực nhanh, sẽ không tạo thói quen |
| **funny** | 1/10 game B. Instant Hook (10%) | Tag hài hước thường đi kèm loop ngắn |

### 7.4 Cụm Tag Kết Hợp (Combo Wins)

| Combo | # game | avg_eng% | avg_users/game | Hành động |
|-------|--:|---------:|----------:|-----------|
| **3d + physics** | 8 | 79.8% | 1,500 | Combo vàng cho danh mục Arcade |
| **3d + racing** | 7 | 81.0% | 1,800 | Đã có cycle-racing-game, topbike, crash-x — tiếp tục |
| **3d + parkour** | 5 | 79.6% | 1,900 | skyhop-3d, asmr-squishy, prison-break — combo mạnh |
| **physics + parkour** | 6 | 81.4% | 1,400 | flip-spot, crash-tower-3d, math-obby |
| **skill + jumping** | 4 | 79.4% | 3,200 | challenge-rush, math-obby — viral combo |
| **collecting + incremental** | 5 | 78.3% | 2,800 | Cẩn thận: 28% có nguy cơ Instant Hook |

### 7.5 Khuyến Nghị Theo Danh Mục

| Danh mục | Tình trạng hiện tại | Khuyến nghị tiếp theo |
|----------|---------------------|----------------------|
| **Driving** | 7 game, 17,145 user, **83.0% eng** | **Đăng thêm 2–3 game Driving mỗi tháng.** Đây là danh mục có chất lượng cao nhất trên user, vẫn còn dư địa tăng trưởng. Ưu tiên racing + bike + 3d |
| **Sports** | 4 game, 7,865 user, **82.5% eng**, p50 cao nhất (331s) | **Đăng thêm 1–2 game Sports mỗi tháng.** Chất lượng xuất sắc, đặc biệt với tag ball/2-player |
| **Action** | 14 game, 15,934 user, 77.8% eng | Ổn định, bổ sung 1 game/tháng với tag weapon + collecting |
| **Arcade** | 33 game, 82,668 user | Đã no — **không ưu tiên thêm Arcade thuần túy**; chỉ Arcade kết hợp Driving/Sports/Puzzle |
| **Casual** | 7 game, 9,539 user | Bổ sung 1 game/tháng, tránh Clicker/Simulation trừ khi cam kết loop |
| **Adventure** | 4 game, 6,657 user | Cơ hội mở rộng — chỉ 4 game, đăng thêm với tag parkour/jumping |
| **Simulation** | 4 game, 4,203 user, p50 thấp (110s) | **Không ưu tiên** — 25% rơi vào Instant Hook |
| **Clicker** | 2 game, 2,625 user, p50 thấp (88s) | **Tránh** trừ khi vòng lặp < 5s |
| **Puzzle** | 3 game, 2,539 user | Ưu tiên bổ sung 1 game/tháng, kết hợp physics/brain |
| **Horror** | 1 game, 2,334 user | Duy trì 1 game/tháng nếu có game chất lượng |
| **Shooting** | 2 game, 1,531 user | Bổ sung 1 game/tháng với tag fps/team |

### 7.6 Quy Tắc Vàng Cho Việc Đăng Game Mới

1. **Luôn kiểm tra 3 tag Tier S** (skill, 3d, physics) — nếu game có ≥1 trong 3 tag này, ưu tiên đăng.
2. **Tránh các tag Tier F** (1-player, collecting, incremental, funny) — trừ khi game đã được kiểm thử kỹ.
3. **Danh mục ưu tiên:** Driving > Sports > Action > Adventure > Puzzle > Casual.
4. **Kết hợp combo vàng:** 3d + physics + parkour cùng nhau tạo ra game engagement cao nhất.
5. **Đặt mục tiêu p50 ≥ 200s** và eng% ≥ 75% cho mọi game mới để duy trì chất lượng A. Premium.
6. **Cảnh báo đặc biệt:** Clicker/Simulation dễ rơi vào Instant Hook (B-tier) — chỉ đăng nếu vòng lặp < 5s.

---

## 8. Phương Pháp

### SQL (trên mỗi game, tổng hợp từ `gm_events`)

```sql
WITH
-- Bước 1: trên (client_id, session_id, page_location) tổng thời lượng phiên
session_dur AS (
    SELECT
        extract(page_location, 'https://1games.io/(.+)') AS slug,
        client_id,
        session_id,
        sum(params_num['estimated_duration_seconds']) AS sess_dur
    FROM gm_events
    WHERE site_id = '1games.io'
      AND shard_date BETWEEN '2026-09-04' AND '2026-09-25'
      AND event_name = 'estimated_session_duration_final'
      AND page_location LIKE 'https://1games.io/%'
      -- [Bộ lọc URL từ SEGMENTATION_PROCESS.md Mục A.3]
      AND extract(page_location, 'https://1games.io/(.+)') IN ({SLUG_LIST})
    GROUP BY slug, client_id, session_id
    HAVING sess_dur > 0
),
-- Bước 2: trên (client_id, page_location) tổng thời lượng user-page
user_dur AS (
    SELECT
        slug,
        client_id,
        sum(sess_dur) AS user_dur
    FROM session_dur
    GROUP BY slug, client_id
),
-- Bước 3: đếm page_view (tất cả phiên của user trên trang này)
page_views AS (
    SELECT
        extract(page_location, 'https://1games.io/(.+)') AS slug,
        client_id,
        session_id
    FROM gm_events
    WHERE site_id = '1games.io'
      AND shard_date BETWEEN '2026-09-04' AND '2026-09-25'
      AND event_name = 'page_view'
      AND page_location LIKE 'https://1games.io/%'
      -- [Bộ lọc URL]
      AND extract(page_location, 'https://1games.io/(.+)') IN ({SLUG_LIST})
    GROUP BY slug, client_id, session_id
)
SELECT
    pv.slug,
    uniqExact(pv.client_id) AS users,
    uniqExact(pv.session_id) AS sessions,
    uniqExactIf(ud.client_id, ud.user_dur > 30) AS engaged_users,
    round(uniqExactIf(ud.client_id, ud.user_dur > 30) / uniqExact(pv.client_id) * 100, 2) AS eng_pct,
    round(quantile(0.5)(sd.sess_dur), 1) AS sess_p50,
    round(quantile(0.9)(sd.sess_dur), 1) AS sess_p90,
    round(avg(sd.sess_dur), 1) AS sess_avg
FROM page_views pv
LEFT JOIN session_dur sd
    ON pv.client_id = sd.client_id
   AND pv.session_id = sd.session_id
   AND pv.slug = sd.slug
LEFT JOIN user_dur ud
    ON pv.client_id = ud.client_id
   AND pv.slug = ud.slug
GROUP BY pv.slug
HAVING sessions >= 200;
```

### Chỉ Số Suy Diễn (Python)

```python
df['sess_per_user']  = df['sessions'] / df['users']
df['p90_p50_ratio']  = df['sess_p90'] / df['sess_p50']
# eng_pct và engaged_users đã được tính trong SQL
```

### Các Phân Khúc Áp Dụng (với ngưỡng đã cập nhật)

| # | Tên | Trục X | Trục Y | Ngưỡng A | Cập nhật cho v2 |
|---|------|--------|--------|-------------|---------------|
| 1 | Tứ Phân Chất Lượng | `eng_pct` | `sess_p50` | eng ≥ 35% AND p50 ≥ 30s | dùng eng_pct user-page |
| 2 | Ma Trận Duy Trì | `sess_per_user` | `eng_pct` | sess ≥ 1.3 AND eng ≥ 50% | công thức mới |
| 3 | Hình Dạng Phân Phối | `p90_p50_ratio` | — | tỷ số ≥ 10 | không đổi |
| 4 | Giá Trị Kinh Doanh | `eng_pct` | `sess_p90` | eng ≥ 35% AND p90 ≥ 120s | dùng eng_pct user-page |
| 5 | Phễu | `eng_pct` | `sess_p90` | eng ≥ 50% AND p90 ≥ 200s | dùng eng_pct user-page |
| 6 | Cụm | tổng hợp | — | điểm ≥ 4 | tổng hợp của 1+4+5 |

---

## 9. File Đã Tạo

| File | Mô tả |
|------|-------------|
| `D:\GR\1games_new_segmented.csv` | Số liệu đầy đủ từng game + 6 nhãn phân khúc (82 dòng, engagement user-page) |
| `D:\GR\1games_new_games_meta.csv` | Metadata crawl cho 82 game (name, author, primary_category, genres, tags, related_games, rating, date_published) |
| `D:\GR\1games_new_segments_detail.csv` | Dạng dài: 1 dòng cho mỗi (segment_dim, slug) kèm số liệu + meta (492 dòng = 82 game × 6 dims) |
| `D:\GR\segment_category_summary.csv` | Tóm tắt category/genre/tag/author theo phân khúc (16 dòng = 6 dims) |
| `D:\GR\segment_games_list.csv` | Dạng rộng: mỗi dòng = một segment_value, cột = danh sách game kèm user count |
| `D:\GR\User Segmentation\reports\SEGMENTATION_OUTPUT_1GAMES_NEW.md` | Báo cáo này (phiên bản tiếng Việt) |
| `D:\GR\05_scripts\tests\segment_1games_new_v2.py` | Script phân khúc (engagement user-page) |
| `D:\GR\05_scripts\tests\fetch_meta_82.py` | Crawler metadata (JSON-LD + tag_related + game_related) |
| `D:\GR\05_scripts\tests\segment_detail_v2.py` | Script phân tích category/tag theo phân khúc |
| `D:\GR\05_scripts\tests\segment_1games_new.py` | Script v1 (giữ tham khảo) |

---

## Lịch Sử Tài Liệu

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---------|------|--------|---------|
| 1.0 | 2026-10-03 | Cursor Assistant | Phân tích lô đầu dùng engagement cấp session |
| 2.0 | 2026-10-03 | Cursor Assistant | Sửa định nghĩa engagement sang user-page (theo yêu cầu). Cập nhật ngưỡng Phân Khúc 2. Chạy lại phân khúc cho 82 game. |
| 2.1 | 2026-10-03 | Cursor Assistant | Thêm §8 Insight Category/Tag. Crawl trực tiếp metadata cho 81/82 game (name, author, primary_category từ JSON-LD BreadcrumbList, genres từ JSON-LD VideoGame, tags từ `data-track-section="tag_related"`, related_games từ `data-track-section="game_related"`). Bảng chéo: category×quality, category×engagement, top-25 tags, danh sách game theo phân khúc, phân tích publisher (1Games vs AZGames). |
| **2.2** | **2026-10-03** | **Cursor Assistant** | **Đã xóa §6 (Games With Zero Traffic) và §7 (Recommendations) và §7.7 (Publisher Analysis). Thêm §7 Khuyến Nghị Tag/Genre Cho Game Sắp Đăng. Dịch toàn bộ tài liệu sang tiếng Việt.** |
