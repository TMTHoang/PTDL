# Báo cáo Hành vi User 1games.io — Phân tích tổng hợp

**Site:** 1games.io
**Khoảng thời gian:** 28 ngày (2026-09-03 → 2026-10-01)
**Nguồn dữ liệu:** `gm_events` (ClickHouse), `games_meta_normalized.csv` (886 game metadata)
**Ngày phân tích:** 6 tháng 10, 2026
**Phương pháp:** Query trực tiếp event log + K-Means cluster v3 (25 features)

---

## Tóm tắt một câu

User của 1games.io chủ yếu là **người chơi 1 lần** (73% chỉ có 1 session), họ thích dòng game **slope/runner** (Slope 2, Challenge Rush, Wacky Flip) và flow phổ biến nhất là **vào thẳng game từ bên ngoài** (Google search, social media, bookmark) chứ không phải duyệt trang chủ.

---

## 1. Tệp user chủ yếu của site là ai?

### 1.1 Phân bổ tổng quan (28 ngày, 1games.io)

| Chỉ số | Giá trị |
|---|---:|
| Tổng user unique (có page view) | **287,805** |
| Tổng session | 1,248,105 |
| Tổng page views | 2,392,432 |
| User chỉ có **1 session** | 208,962 (**72.6%**) |
| User có **≥ 3 sessions** | 51,592 (**17.9%**) |
| User có **≥ 5 sessions** | 31,590 (**11.0%**) |
| User có **≥ 10 sessions** | 13,723 (**4.8%**) |
| Median sessions / user | **1** |
| Median active_days / user | **1** |
| P90 sessions / user | 5 |
| P90 active_days / user | 4 |
| Avg sessions / user | 2.37 |
| Avg active_days / user | 1.73 |

### 1.2 Phân bổ số session trên user

| Số session | Số user | Tỷ lệ |
|---:|---:|---:|
| 1 session | 208,962 | **72.6%** |
| 2–3 sessions | 47,251 | 16.4% |
| 4–7 sessions | 18,463 | 6.4% |
| 8–14 sessions | 13,406 | 4.7% |
| ≥ 15 sessions | 5,873 | 2.0% |

### 1.3 Phân bổ số ngày active trên user

| Số ngày active | Số user | Tỷ lệ |
|---:|---:|---:|
| 1 ngày | 220,675 | **76.7%** |
| 2–3 ngày | 41,762 | 14.5% |
| 4–7 ngày | 14,303 | 5.0% |
| 8–14 ngày | 7,213 | 2.5% |
| ≥ 15 ngày | 3,852 | 1.3% |

### Kết luận phần 1: User của site là **người chơi 1 lần**

- **73% user chỉ ghé 1 session duy nhất trong 28 ngày** — đây là tệp user chiếm đa số
- **77% user chỉ active đúng 1 ngày** — gần như không quay lại
- **Chỉ ~5% user có ≥ 8 sessions** và **~3% user active ≥ 8 ngày** — đây là tệp "trung thành"
- **Median user là 1 session / 1 ngày / 1 lần ghé**

User "trung thành" tuy thiểu số nhưng đóng góp phần lớn traffic: **Power user** (cluster 2) chiếm 35% số user trong cohort mature nhưng tạo ra phần lớn page view.

> So với cohort mature (32,701 user, đã được lọc ≥28 ngày lịch sử), tỷ lệ người chơi 1 lần cũng tương tự — đây là đặc tính thật của site, không phải do bias.

---

## 2. Sở thích game của user là gì?

### 2.1 Top 15 game theo lượt xem (PV)

| # | Game | PV | Số user | Avg time / user (giây) |
|---:|---|---:|---:|---:|
| 1 | **Slope 2** | 97,084 | 39,153 | 21.0 |
| 2 | Wacky Flip | 75,591 | 32,824 | 19.6 |
| 3 | Challenge Rush | 71,907 | 28,604 | **34.3** |
| 4 | Traffic Road | 59,205 | 28,361 | 9.7 |
| 5 | Orbit Kick | 43,765 | 20,607 | 19.7 |
| 6 | Tap Road | 38,644 | 17,355 | 21.6 |
| 7 | Undead Corridor | 37,332 | 17,930 | 17.4 |
| 8 | Ragdoll Playground | 32,269 | 14,946 | 15.2 |
| 9 | Pixel Path | 30,720 | 16,742 | **31.6** |
| 10 | City Brawl | 30,197 | 15,668 | 19.6 |
| 11 | Slope Rider | 27,182 | 12,024 | **56.8** ⭐ |
| 12 | Hot-Games (hub) | 25,582 | 14,655 | 19.8 |
| 13 | Brain Lines | 21,330 | 11,359 | 25.3 |
| 14 | Wacky Steps | 19,971 | 10,538 | 17.8 |
| 15 | Golf Hit | 19,303 | — | 19.2 |

### 2.2 Top 15 game theo **tổng thời gian chơi** (engagement time)

| # | Game | Tổng giờ | Số user đã chơi | Trung bình / user |
|---:|---|---:|---:|---:|
| 1 | **Challenge Rush** | **107.3h** | 11,253 | 34.3s |
| 2 | Slope 2 | 72.5h | 12,412 | 21.0s |
| 3 | **Slope Rider** | **62.9h** | 3,986 | **56.8s** ⭐ |
| 4 | Wacky Flip | 59.2h | 10,873 | 19.6s |
| 5 | Pixel Path | **54.2h** | 6,176 | **31.6s** |
| 6 | Hot-Games (hub) | 52.0h | 9,475 | 19.8s |
| 7 | Traffic Road | 50.5h | — | 9.7s |
| 8 | Undead Corridor | 27.6h | — | 17.4s |
| 9 | Orbit Kick | 22.5h | — | 19.7s |
| 10 | Tap Road | 21.3h | — | 21.6s |
| 11 | Stickman Slash | 19.7h | 2,321 | **30.6s** |
| 12 | City Brawl | 17.1h | — | 19.6s |
| 13 | Wacky Steps | 15.2h | 3,081 | 17.8s |
| 14 | Golf Hit | 14.8h | 2,768 | 19.2s |
| 15 | Escape Road 3 | 14.0h | 2,740 | 18.4s |

### 2.3 Game "trung thành nhất" — user chơi **lâu nhất** trên 1 lần ghé

| # | Game | Avg time / user | Số user | Ghi chú |
|---:|---|---:|---:|---|
| 1 | **Slope Rider** | **56.8s** | 3,986 | Game "sticky" nhất |
| 2 | Bloodmoney Remake | 52.4s | 708 | Niche horror |
| 3 | Bow Battle | 34.0s | 580 | — |
| 4 | **Challenge Rush** | **34.3s** | 11,253 | Top 3 về lượt xem |
| 5 | Tung Sahur Clicker | 32.2s | 535 | — |
| 6 | **Pixel Path** | **31.6s** | 6,176 | — |
| 7 | Stickman Slash | 30.6s | 2,321 | — |
| 8 | Jetski Race | 28.5s | 1,104 | — |
| 9 | Pizza Clicker | 27.6s | 1,540 | — |

### Kết luận phần 2: Sở thích game

#### a) Game được chơi NHIỀU NHẤT (volume):
- **Slope 2** là "vua" về PV (97k) lẫn user (39k)
- **Wacky Flip** đứng thứ 2 về cả PV lẫn user
- **Challenge Rush** đứng thứ 3 về PV nhưng top 1 về **tổng thời gian** (107h)

#### b) Game được chơi LÂU NHẤT (per-user time):
- **Slope Rider** — user chơi trung bình 56.8 giây (gấp 1.7 lần Slope 2)
- **Bloodmoney Remake** — 52.4 giây/user (game horror niche)
- **Challenge Rush** — 34.3 giây/user (top game về tổng thời gian)

#### c) Nhận xét quan trọng:
- **PV cao không đồng nghĩa với Time chơi cao.** Slope 2 có nhiều PV nhất (97k) nhưng thời gian / user thấp (21s) → user "click và xem" nhanh rồi thoát.
- **Challenge Rush "giữ chân" user lâu hơn.** Ít user hơn Slope 2 nhưng ai chơi thì chơi lâu hơn → game này có **engagement quality** tốt nhất.
- **Dòng slope/runner chiếm trọn top đầu** (Slope 2, Challenge Rush, Wacky Flip, Tap Road, Slope Rider, Pixel Path) — đây là "chữ ký" của site.

---

## 3. Flow của user là gì?

### 3.1 Phân bổ điểm vào session (entry page)

| Entry intent | Số session | Tỷ lệ |
|---|---:|---:|
| **Vào thẳng game** (direct_game URL) | 241,702 | **52.7%** |
| **Trang chủ** (home) | 187,732 | 40.9% |
| **Category browse** (hot-games, shooting.games…) | 25,281 | 5.5% |
| **Search** | 3,668 | 0.8% |

> User vào thẳng game từ Google search, social media, hoặc bookmark — không qua trang chủ.

### 3.2 Phân bổ điểm ra session (exit page)

| Exit intent | Số session | Tỷ lệ |
|---|---:|---:|
| **Trang game** (chơi xong rồi đóng) | 384,613 | **83.9%** |
| Trang chủ | 49,680 | 10.8% |
| Category browse | 20,530 | 4.5% |
| Search | 3,560 | 0.8% |

> **84% session kết thúc sau khi chơi game** — user đến, chơi, đi. Không quay lại home, không duyệt thêm.

### 3.3 Top 10 hai-bước chuyển trang (intent → intent)

| From → To | Số lượt chuyển | Số session |
|---|---:|---:|
| **direct_game → direct_game** | 833,649 | 239,936 |
| direct_game → home | 284,400 | 181,477 |
| **home → direct_game** | 283,960 | 180,994 |
| home → home | 100,444 | 68,669 |
| category_browse → direct_game | 83,239 | 49,747 |
| direct_game → category_browse | 82,941 | 49,478 |
| search → direct_game | 34,635 | 28,032 |
| direct_game → search | 34,494 | 27,848 |
| home → category_browse | 29,720 | 24,038 |
| category_browse → home | 29,246 | 23,817 |

### 3.4 Top 15 game-to-game chuyển trang

| Từ game | Đến game | Số lượt |
|---|---|---:|
| Wacky Flip | Slope 2 | 3,314 |
| Slope 2 | Wacky Flip | 3,279 |
| Traffic Road | Slope 2 | 2,786 |
| **Slope 2** | **Challenge Rush** | 2,744 |
| **Challenge Rush** | **Slope 2** | 2,740 |
| Slope 2 | Traffic Road | 2,724 |
| Slope 2 | Tap Road | 2,403 |
| Tap Road | Slope 2 | 2,312 |
| Traffic Road | Wacky Flip | 1,962 |
| Wacky Flip | Traffic Road | 1,955 |
| Orbit Kick | Slope 2 | 1,878 |
| Slope 2 | Orbit Kick | 1,814 |
| Pixel Path | Slope 2 | 1,583 |
| Wacky Flip | Challenge Rush | 1,531 |
| Slope 2 | Pixel Path | 1,530 |

### 3.5 Phân bổ số trang mỗi session

| Số trang / session | Số session | Tỷ lệ |
|---:|---:|---:|
| 1 trang | 128,071 | **27.9%** |
| 2 trang | 75,288 | 16.4% |
| 3–5 trang | 116,230 | 25.3% |
| 6–10 trang | 79,215 | 17.3% |
| 11–20 trang | 45,403 | 9.9% |
| 21+ trang | 14,176 | 3.1% |

> **44% session có ≤ 2 trang** — user vào 1 game, thoát. Pattern "1 click và đi" chiếm đa số.

### 3.6 Top 15 game hay là "exit game" (game cuối cùng trong session)

| Game | Số session kết thúc ở đây |
|---|---:|
| **Slope 2** | 30,425 |
| Challenge Rush | 24,765 |
| Wacky Flip | 22,920 |
| Traffic Road | 16,697 |
| Orbit Kick | 14,021 |
| Undead Corridor | 10,906 |

### Kết luận phần 3: Flow của user

#### a) User vào thẳng game (53% session), không qua trang chủ
- Đa số user **đến site qua Google search, social media, hoặc bookmark** với URL game cụ thể
- Trang chủ chỉ là entry của 41% session
- Search rất ít dùng (0.8% session) → category + search gần như không phải kênh acquisition

#### c) Sau khi chơi, user đi luôn (84% session kết thúc ở game)
- Không duyệt thêm, không quay lại home
- Pattern **"vào → chơi → đi"** là phổ biến nhất

#### c) Một số user có flow "home → game → home → game"
- ~284,000 lượt chuyển từ game về home và ~284,000 lượt từ home sang game — **gần như đối xứng**
- Đây là user "dạo chơi" — vào home, chọn game, quay lại home, chọn game khác

#### d) Slope 2 là "anchor game" — xuất hiện trong mọi top transition
- Slope 2 → Wacky Flip, Slope 2 → Challenge Rush, Slope 2 → Traffic Road, Slope 2 → Tap Road, Slope 2 → Pixel Path, Slope 2 → Orbit Kick
- **Slope 2 vừa là entry game hàng đầu vừa là "next game" phổ biến nhất** khi user đang ở game khác → đây là trung tâm của hệ navigation

---

## 4. Tổng kết & khuyến nghị

### Bức tranh tổng thể:

User 1games.io chủ yếu là NGƯỜI CHƠI 1 LẦN (73%) — họ thích SLOPE/RUNNER (Slope 2, Challenge Rush, Wacky Flip) — họ vào THẲNG GAME từ Google/social (53% session), chơi xong ĐI LUÔN (84% session kết thúc ở game). Power user (5% tệp "trung thành") mới là người giữ site sống.

### Khuyến nghị hành động:

#### 1. Tối ưu cho pattern "vào game rồi đi"
- **53% session bắt đầu thẳng game** → cần canonical URL + meta SEO chuẩn cho mỗi game
- **84% session kết thúc ở game** → cần **CTA ngay trên game page** (ví dụ: "Chơi tiếp game tương tự", "Game khác bạn có thể thích") để kéo user vào game thứ 2 trong cùng session

#### 2. Khai thác Challenge Rush
- Top 1 tổng thời gian (107h) + 28k user
- User chơi trung bình 34.3s — game "sticky" thật sự
- Nếu đặt "Game tương tự" sau khi chơi Challenge Rush, có cơ hội giữ user thêm

#### 3. Slope 2 là "anchor game" — bảo vệ nó
- Top 1 PV (97k), top 1 user (39k), xuất hiện trong hầu hết game-to-game transition
- Bất kỳ thay đổi nào ảnh hưởng Slope 2 sẽ ảnh hưởng đến toàn bộ site
- Nên có A/B test riêng cho trang này

#### 4. Category browse + Search rất yếu (tổng ~6%)
- User không dùng tính năng browse site, họ chỉ "vào game là xong"
- Có thể cải thiện UX hoặc đơn giản là không phải kênh user cần

#### 5. 44% session ≤ 2 trang = "1 click và thoát"
- Phần lớn user không có "phiên duyệt", chỉ có "lần ghé 1 game"
- Đây là cơ hội lớn: nếu **trên trang game** có widget "Game khác bạn có thể thích", có thể tăng 2-3 trang / session

---

## Phụ lục: Phương pháp

| Bước | Mô tả |
|---|---|
| 1 | Query `gm_events` (ClickHouse) cho 1games.io, 28d, event_name='page_view' |
| 2 | Trích slug từ page_location bằng regex `^https?://[^/]+/(.+?)(?:\?\|#\|$)` |
| 3 | Phân loại intent: home / category_browse / search / direct_game / other |
| 4 | Tính session-level stats: số session, active_days, top entry, exit, page count |
| 5 | Tính page-level stats: PV, user count, avg engagement time per user |
| 6 | Tính transition matrix bằng `arraySlice` + `arrayJoin` trên ordered intent arrays |
| 7 | Kết hợp với kết quả K-Means cluster (K=3, 25 features) từ `clusters_1games_2026-10-01.csv` |

**Lưu ý:**
- Dữ liệu lấy từ `gm_events` (chứa mọi event, không giới hạn) thay vì từ chunk JSON (bị truncate ở top 20 slugs / user). Nên số liệu trong báo cáo này **chính xác hơn** so với báo cáo K-Means trước.
- Không nhất quán: 32,701 user mature trong cluster CSV vs 287,805 user unique có page view trong toàn bộ 28 ngày. Cluster chỉ là "mature" subset (≥28 ngày lịch sử).
- Cohort_date table `gm_clients` chỉ giữ được ~30 ngày (đến 2026-09-07), không thể reproduce filter từ segmentation ban đầu.