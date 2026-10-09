# Phân Khúc Người Dùng zapgames.io — Câu Chuyện

**Site:** zapgames.io
**Khoảng thời gian:** 28 ngày kết thúc ngày 1 tháng 10, 2026
**Số user phân tích:** 58,511 (user trưởng thành — có ≥ 2 ngày active trong 28 ngày qua, dùng làm proxy cho "mature user")
**Phương pháp:** K-Means clustering trên 25 đặc trưng hành vi
**Đối tượng đọc:** sản phẩm, marketing, nội dung, ban lãnh đạo
**Ngày:** 8 tháng 10, 2026

---

## Tóm tắt một câu

Cứ 100 user trưởng thành của zapgames.io trong 28 ngày qua:
**29 người là lõi trung thành — cộng đồng thực sự giữ cho site sống · 42 người là người chơi rộng — vào chơi nhiều game, chơi sâu, nhưng không quay lại thường xuyên · 29 người là người chơi trung thành một game — vào thử một hai lần rồi biến mất.**

---

## Chúng tôi đã làm gì, nói đơn giản

Chúng tôi lấy tất cả user trên zapgames.io có **ít nhất 2 ngày hoạt động** trong 28 ngày
qua. (Lưu ý khác biệt với 1games: bảng `gm_clients` chỉ giữ lịch sử 7-8 ngày gần nhất,
nên chúng tôi không thể lọc user "có lịch sử ≥28 ngày" như segmentation của 1games
đã làm. Lọc "≥2 active_days" là proxy tốt nhất hiện có cho tệp mature.)

Với mỗi user, chúng tôi đo 25 con số bao gồm:

- họ dùng site bao nhiêu
- họ chơi game nào
- họ quay lại thường xuyên cỡ nào
- họ có search, lướt category, hay vào thẳng game không
- họ thích loại game nào (tags, categories)

Sau đó chúng tôi để một thuật toán phân cụm tìm nhóm tự nhiên.
Nó tìm ra **ba nhóm**.

---

## Ba phân khúc

### 🟢 Lõi trung thành (Power user) — 29% user (16,854 người)

**Họ là ai:** lõi trung thành của zapgames. Họ quay lại thường xuyên, chơi
nhiều game khác nhau, biết rõ mình muốn gì. **29% user nhưng tạo ra 61% số
session, 56% page view, và 73.5% tổng thời gian chơi.** Đây là nhóm **một
user bằng vài user thường**.

| | |
|---|---|
| Page view (28 ngày) | 63 |
| Phiên (28 ngày) | 17 |
| Số game khác nhau đã chơi | 13 |
| Tỷ lệ engagement | 68% |
| Độ dài phiên trung bình | 25 phút |
| Lần cuối truy cập | 5 ngày trước |
| Thể loại hàng đầu | sports, arcade, action |

**Game yêu thích của nhóm:** Veck.io, Frontwars.io, Golf Hit, Basketball Hit,
Bowmasters Archery — tất cả đều là game cạnh tranh, multiplayer.

**Ý nghĩa:** đây là nhóm mà zapgames được xây cho. Họ chơi **25 phút mỗi
phiên** (gấp đôi 1games Power user), quay lại thường xuyên (5 ngày từ lần
cuối). Họ cần được **giữ chân** thông qua: cập nhật nội dung, thử thách mới,
giải đấu, leaderboard.

---

### 🟡 Người chơi trung thành một game (Casual single-game browser) — 29% user (17,098 người)

**Họ là ai:** người vào zapgames, **chơi một game (thường là game "nặng" như
GTA 5 Online hoặc Veck.io), rồi không quay lại**. 58% tổng page view của họ
là cùng một game. Trung bình 13 ngày từ lần truy cập gần nhất. Nhóm "vào một
lần cho biết" hoặc "đã chán game".

| | |
|---|---|
| Page view (28 ngày) | 8 |
| Phiên (28 ngày) | 4 |
| Số game khác nhau đã chơi | **1,9** |
| Tỷ lệ engagement | 58% |
| Độ dài phiên trung bình | 7 phút |
| Lần cuối truy cập | 13 ngày trước |
| Thể loại hàng đầu | action, sports, arcade |

**Game yêu thích của nhóm:** **GTA 5 Online** (5.8% có nó là top game),
Veck.io (5.6%), Golf Hit, Frontwars.io, 2v2.io. Đây là những **game "anchor"
của zapgames** — user tìm đến từ Google, chơi một lần, rồi đi.

**Ý nghĩa:** 1games có nhóm tương tự nhưng zapgames phiên bản này **"trung
thành một game" hơn** — top game share 58% so với 54% ở 1games. Cơ hội lớn:
**gợi ý "Game tương tự GTA 5 Online" ngay sau khi họ thoát game** có thể
kéo họ vào game thứ 2 trong cùng session, biến họ thành Lõi trung thành.

---

### 🔵 Người chơi rộng (Broad explorer) — 42% user (24,559 người)

**Họ là ai:** nhóm lớn nhất và cũng thú vị nhất. Họ **chơi rất nhiều game
khác nhau** (trung bình 9.6 game), mỗi phiên **dài tới 14 phút** (gấp đôi
Casual single-game), tỷ lệ engagement **83% (cao nhất trong 3 nhóm)**. Nhưng
lần cuối truy cập trung bình là 12 ngày trước — họ **không quay lại thường
xuyên**.

| | |
|---|---|
| Page view (28 ngày) | 29 |
| Phiên (28 ngày) | 5 |
| Số game khác nhau đã chơi | **9,6** |
| Tỷ lệ engagement | **83%** |
| Độ dài phiên trung bình | 14 phút |
| Lần cuối truy cập | 12 ngày trước |
| Thể loại hàng đầu | sports, action, arcade |

**Game yêu thích của nhóm:** Veck.io, Golf Hit, Frontwars.io, Basketball Hit,
Bowmasters Archery — **trùng gần hết với Lõi trung thành**. Điểm khác biệt:
họ chơi rộng nhưng **không quay lại sớm**.

**Ý nghĩa:** đây là **nhóm có engagement cao nhưng frequency thấp** —
cơ hội lớn nhất. Họ yêu thích zapgames (chơi sâu 14 phút, 9.6 game khác
nhau), nhưng họ quên. **Email nhắc "tuần trước bạn đã chơi X, hôm nay có
Y mới"** có thể kéo họ về.

---

## So sánh nhanh ba phân khúc

| | Lõi trung thành 🟢 | Trung thành 1 game 🟡 | Chơi rộng 🔵 |
|---|---:|---:|---:|
| % user | 29% | 29% | 42% |
| Page view (trung bình) | 63 | 8 | 29 |
| Phiên (trung bình) | 17 | 4 | 5 |
| Số game khác nhau | 13 | 1,9 | 9,6 |
| Tỷ lệ engagement | 68% | 58% | **83%** |
| Độ dài phiên trung bình | 25 phút | 7 phút | 14 phút |
| Lần cuối truy cập | 5 ngày trước | 13 ngày trước | 12 ngày trước |
| Có quay lại trong 7 ngày qua? | có (66%) | hiếm (10%) | hiếm (8%) |
| Có "game yêu thích" rõ ràng? | có (29%) | **có (58%)** | không (19%) |
| Độ đa dạng tag (chơi nhiều thể loại) | 53 tag | 11 tag | 42 tag |
| Đọc / lướt game? | có (8% home share) | hiếm | có (11% category browse) |
| Có search? | không | không | không |
| **% session** | **61%** | 13% | 26% |
| **% page view** | **56%** | 7% | 37% |
| **% tổng engagement time** | **73.5%** | 6% | 20% |

---

## So sánh với phân khúc 1games

Phân khúc của zapgames có **cấu trúc khác** so với 1games vì hai site phục
vụ hai loại user khác nhau:

| | 1games (32,701 user mature) | zapgames (58,511 user mature) |
|---|---|---|
| **Cách chia** | Khách chơi thử / Vào rồi thoát / Power user | Lõi trung thành / Trung thành 1 game / Chơi rộng |
| **Cluster kích thước** | 43% / 22% / 35% | 29% / 29% / 42% |
| **Bounce cluster (0 game)** | **22%** | **3,8%** (chỉ trong Trung thành 1 game) |
| **Median user (mature)** | 1 session, 0 game (Bounce) hoặc 1-2 game (Casual) | 4 session, 2 game (Trung thành 1 game) |
| **Power user avg session** | 13 phút | **25 phút** |
| **Power user ratio (%session)** | n/a cụ thể | **61%** |

**Hai site có "lõi trung thành" mạnh tương đương** (29-35%) nhưng zapgames:

1. **Ít user "bounce" hơn nhiều** — chỉ 3.8% user mature không chơi game nào,
   so với 22% ở 1games. Lý do: zapgames mature users (active ≥ 2 ngày) gần như
   đã trải qua ít nhất một lần "chơi gì đó".
2. **Power user của zapgames "đậm" hơn** — 25 phút / session so với 13 phút.
   Có lẽ vì game .io / GTA của zapgames có session dài hơn so với Slope /
   runner của 1games.
3. **Zapgames có nhóm "Chơi rộng" riêng** — 42% user chơi ~10 game khác nhau
   trong 28 ngày. 1games không có nhóm tương tự với cùng quy mô.

---

## Câu chuyện mà dữ liệu kể

### 1. Zapgames có "lõi trung thành" rất mạnh — và cần bảo vệ

29% user trưởng thành (16.854 người) tạo ra **73.5% tổng thời gian chơi
của cả site**. Nếu 10% trong số họ giảm engagement vì một game bị xóa
hoặc chậm, zapgames mất ~7% engagement time. Power user = "rủi ro tập
trung" mà cũng là "lợi nhuận tập trung".

### 2. Nhóm "Trung thành một game" là phễu vào Power user

17.098 user (29% mature) chơi 1-2 game rồi biến mất. **Nếu 10% trong số
họ chuyển sang chơi 3+ game**, họ sẽ thành Lõi trung thành. Hai cách
hiệu quả nhất:
- **Widget "Game cùng cluster"** trên trang game (VD: chơi GTA 5 → hiện
  GTA 6, San Andreas, Vice Town)
- **Prompt "Game tương tự" ngay khi user thoát** (giảm 56% session
  "chỉ 1 game" — nếu 20% trong số họ click thêm, lưu lượng tăng rất mạnh)

### 3. Nhóm "Chơi rộng" là cơ hội giữ chân lớn nhất

42% user (24.559 người) chơi rất tốt khi họ ghé (14 phút, 9.6 game, 83%
engagement) nhưng **không quay lại thường xuyên** (12 ngày từ lần cuối).
Họ rõ ràng **thích zapgames** nhưng quên. Đây là use case hoàn hảo cho
**email/push nhắc dựa trên lịch sử chơi**.

### 4. Khác với 1games, zapgames không có nhóm "Bounce" đáng kể

1games có 22% user mature không chơi game nào. Zapgames chỉ 3.8%. Tại sao?
- Zapgames có **home page tốt hơn** (gợi ý game phong phú, có nhiều
  "anchor game" như GTA 5 Online)
- Zapgames có **nhiều entry point đa dạng hơn** (category browse chiếm
  11% PV ở nhóm "Chơi rộng" so với 7.8% ở Power user)
- Hoặc đơn giản: **đối tượng zapgames tự nhiên "tìm được game" nhanh hơn**

### 5. Anchor games quan trọng hơn bao giờ

Cả 3 phân khúc đều có **cùng 5 game hàng đầu** (Veck.io, Golf Hit,
Frontwars.io, Basketball Hit, Bowmasters Archery). Một game như **GTA 5
Online** chỉ đứng top 1 ở nhóm "Trung thành một game" (5.8% user có
nó là top game) — chứng tỏ GTA 5 Online là **game "first touch"** cho
rất nhiều user. Bảo vệ và cải thiện trải nghiệm của GTA 5 Online = bảo
vệ phễu vào.

---

## Phân tích này cho phép làm gì

Mỗi phân khúc gợi ý một chiến lược khác nhau:

| Phân khúc | % | Chiến lược |
|---|---|---|
| Trung thành 1 game 🟡 | 29% | **Widget "Game cùng cluster" trên trang game.** Chuyển đổi 10% thành Lõi trung thành = thêm 1.700 user ổn định. Mục tiêu: kéo dài session từ 1 → 2 game. |
| Chơi rộng 🔵 | 42% | **Email/push nhắc theo lịch sử.** "Tuần trước bạn chơi X, hôm nay có Y mới." Họ đã sẵn sàng, chỉ thiếu trigger. Mục tiêu: giảm 12 ngày thành 7 ngày giữa các lần ghé. |
| Lõi trung thành 🟢 | 29% | **Giữ chân + cập nhật nội dung.** Họ chơi 25 phút / session. Cần game mới, leaderboard, thử thách để không chán. Mục tiêu: duy trì 5 ngày giữa các lần ghé. |

Những chiến lược này chưa được triển khai. Chúng là đầu vào cho bước
tiếp theo (chiến lược gợi ý theo phân khúc).

---

## Những gì chúng tôi CHƯA làm

Để trung thực về giới hạn của phân tích:

- **Cohort filter khác 1games.** Bảng `gm_clients` chỉ giữ 7-8 ngày
  lịch sử gần nhất, nên chúng tôi không thể dùng filter "user trưởng
  thành (≥28 ngày lịch sử)" như 1games đã dùng. Chúng tôi dùng proxy
  "active_days ≥ 2 trong 28 ngày" — điều này có nghĩa zapgames cohort
  rộng hơn 1games cohort. So sánh trực tiếp giữa hai cohort cần
  thận trọng.

- **Chưa đo lường hiệu quả của hệ thống gợi ý.** Nói "widget game cùng
  cluster" mới chỉ là giả thuyết. Chúng tôi chưa chạy thử nghiệm.

- **Các cụm là tĩnh.** Một user "Trung thành 1 game" hôm nay có thể
  thành "Chơi rộng" tháng sau. Chúng tôi chưa theo dõi sự chuyển đổi.

- **Silhouette thấp hơn 1games (0.19 vs 0.37).** Zapgames có 3 cluster
  overlap nhiều hơn — đặc biệt giữa "Chơi rộng" và "Lõi trung thành".
  Có thể tăng K lên 4-5 để tách nhỏ hơn, nhưng silhouette giảm
  (0.17 cho K=4, 0.15 cho K=5) — nghĩa là K=3 vẫn là phân chia
  "sạch" nhất.

- **Một site, một khoảng thời gian.** Đây là zapgames.io, 28 ngày kết
  thúc 2026-10-01. Các cụm sẽ thay đổi theo thời gian và sẽ khác
  cho 1000games.io.

---

## Tìm dữ liệu ở đâu

| File | Nội dung |
|---|---|
| `d:\GR\User Segmentation\data\user_features_zapgames_2026-10-01.csv` | 58,511 user × 35 cột, features đầu vào |
| `d:\GR\User Segmentation\data\clusters_zapgames_2026-10-01.csv` | Bảng đầy đủ — 58,511 user, kèm cột `cluster_id` |
| `d:\GR\User Segmentation\data\zapgames_cluster_report.md` | Báo cáo số chi tiết theo từng cụm |
| `d:\GR\User Segmentation\data\zapgames_cluster_summary.md` | Tóm tắt ngắn |
| `d:\GR\03_data\processed\user_features\zapgames_chunks\` | 12 chunk JSON (PV + sessions) từ ClickHouse |
| `d:\GR\zap_step*.py` | Scripts chạy pipeline (giữ lại làm reference) |

---

**Ngày tạo:** 2026-10-08
**Phương pháp:** K-Means clustering (K=3, 25 đặc trưng, sklearn)
**Khoảng thời gian:** 2026-09-03 đến 2026-10-01 (28 ngày)
**Cohort:** user trưởng thành proxy (active_days ≥ 2 trong 28d)
**Site:** zapgames.io
**Silhouette:** 0.19 (K=3, sample 3,000 user)
**Coverage:** 58,511/58,511 user (100%) có `top_slugs` data trong chunks — phân tích tag/game đầy đủ 3 phân khúc (xem báo cáo `insights_games_tags_zapgames_VI.md`)
