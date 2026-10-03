# Phân Khúc Người Dùng 1games.io — Câu Chuyện

**Site:** 1games.io
**Khoảng thời gian:** 28 ngày kết thúc ngày 1 tháng 10, 2026
**Số user phân tích:** 32,701 (user trưởng thành — có lịch sử ≥28 ngày)
**Phương pháp:** K-Means clustering trên 25 đặc trưng hành vi
**Đối tượng đọc:** sản phẩm, marketing, nội dung, ban lãnh đạo
**Ngày:** 2 tháng 10, 2026

---

## Tóm tắt một câu

Cứ 100 user trưởng thành của 1games.io trong 28 ngày qua:
**43 người vào chơi một hai game rồi biến mất · 22 người vào trang chủ rồi rời đi không chơi game nào · 35 người là lõi trung thành — cộng đồng thực sự giữ cho site sống.**

---

## Chúng tôi đã làm gì, nói đơn giản

Chúng tôi lấy tất cả user đã có mặt trên 1games.io ít nhất 28 ngày
(điều này quan trọng — để so sánh công bằng; nếu không user mới đến
sẽ bị tính nhầm là "không hoạt động"). Với mỗi user, chúng tôi đo 25
con số bao gồm:

- họ dùng site bao nhiêu
- họ chơi game nào
- họ quay lại thường xuyên cỡ nào
- họ có search, lướt category, hay vào thẳng game không
- họ thích loại game nào (tags, genres)

Sau đó chúng tôi để một thuật toán phân cụm tìm nhóm tự nhiên.
Nó tìm ra **ba nhóm**.

---

## Ba phân khúc

### 🟡 Khách chơi thử (Casual browser) — 43% user (14,052 người)

**Họ là ai:** người vào 1games, chơi một hoặc hai game, rồi bỏ đi.
Họ có game yêu thích — 54% tổng page view của họ là cùng một game
— nhưng không quay lại thường xuyên. Trung bình 25 ngày từ lần
truy cập gần nhất. Nhóm "thử một lần cho biết".

| | |
|---|---|
| Page view (28 ngày) | 6 |
| Phiên (28 ngày) | 2 |
| Số game khác nhau đã chơi | 2 |
| Tỷ lệ engagement | 64% |
| Độ dài phiên trung bình | 6,5 phút |
| Lần cuối truy cập | 25 ngày trước |
| Thể loại hàng đầu | arcade, action |

**Ý nghĩa:** 1games có rất nhiều user kiểu này nhưng họ không ở lại.
Họ có thể quay lại thêm một hai lần, nhưng phần lớn đã đi. **Đây là
câu hỏi về phễu chuyển đổi** — 1games có thể biến họ thành Power
user được không?

### 🔴 Vào rồi thoát (Bounce / nav-only) — 22% user (7,070 người)

**Họ là ai:** người vào 1games, nhìn trang chủ, rồi đi. Họ không
click vào bất kỳ game nào. 80% mọi thứ họ làm là ở trang chủ.

| | |
|---|---|
| Page view (28 ngày) | 1,3 |
| Phiên (28 ngày) | 1 |
| Số game khác nhau đã chơi | **0** |
| Tỷ lệ engagement | 12% |
| Độ dài phiên trung bình | 26 giây |
| Lưu lượng trên trang chủ | **80%** |
| Lần cuối truy cập | 28 ngày trước |

**Ý nghĩa:** họ vào, họ thấy, họ thoát. Đây là **vấn đề về khám
phá** — những user này không tìm được gì để chơi. Hoặc trang chủ
chưa đưa ra đúng game, hoặc đối tượng không khớp với site (sai user
× đúng site).

### 🟢 Power user — 35% user (11,579 người)

**Họ là ai:** lõi trung thành. Họ quay lại thường xuyên, chơi
nhiều game khác nhau, biết rõ mình muốn gì.

| | |
|---|---|
| Page view (28 ngày) | 48 |
| Phiên (28 ngày) | 15 |
| Số game khác nhau đã chơi | 9,8 |
| Tỷ lệ engagement | 69% |
| Độ dài phiên trung bình | 13 phút |
| Lần cuối truy cập | 10 ngày trước |
| Thể loại hàng đầu | arcade, action |

**Ý nghĩa:** đây là nhóm mà 1games được xây cho. Họ tạo ra phần
lớn page view (Power user = 35% user, nhưng tỷ trọng lưu lượng lớn
hơn nhiều). Họ có game yêu thích, nhưng không phải kiểu trung thành
một game — trung bình họ khám phá 9,8 game. **Đây là phân khúc cần
phát triển.**

---

## So sánh nhanh ba phân khúc

| | Khách chơi thử 🟡 | Vào rồi thoát 🔴 | Power user 🟢 |
|---|---:|---:|---:|
| % user | 43% | 22% | 35% |
| Page view (trung bình) | 6 | 1,3 | 48 |
| Phiên (trung bình) | 2 | 1 | 15 |
| Số game khác nhau | 2 | 0 | 10 |
| Tỷ lệ engagement | 64% | 12% | 69% |
| Độ dài phiên trung bình | 6,5 phút | 26 giây | 13 phút |
| Lần cuối truy cập | 25 ngày trước | 28 ngày trước | 10 ngày trước |
| Có quay lại trong 7 ngày qua? | hiếm | không | có (1+ phiên) |
| Có "game yêu thích" rõ ràng? | có (54%) | không | có (26%) |
| Độ đa dạng tag (chơi nhiều thể loại) | 12 tag | 0 | 37 tag |
| Đọc / lướt game? | hiếm | không | có |
| Có search? | hiếm | không | thỉnh thoảng |

---

## Câu chuyện mà dữ liệu kể

### 1. 1games đang làm tốt với nhóm mà nó phục vụ

Power user rất engaged: 13 phút mỗi phiên, 15 phiên trong 28 ngày,
khám phá 10 game khác nhau. Site đang làm tốt đúng việc nó cần làm.
**35% user trưởng thành là Power user.** Đó là một mức trần
engagement rất tốt.

### 2. Có một lỗ hổng ở đầu phễu

22% user trưởng thành (phân khúc "Vào rồi thoát") **không chơi game
nào**. Họ vào, thấy trang chủ, rồi đi. Những user này vẫn là user
trưởng thành (có ≥28 ngày lịch sử) — nghĩa là họ đã từng quay lại
1games ít nhất một lần. Trang chủ đã không chuyển đổi được họ. Đây
là vấn đề dễ sửa nhất trong dữ liệu: một trải nghiệm "bắt đầu từ
đây" tốt hơn có thể biến Vào rồi thoát thành Khách chơi thử.

### 3. Khách chơi thử là cơ hội lớn nhất

Với 43% họ là nhóm lớn nhất, nhưng lần truy cập gần nhất trung bình
là 25 ngày trước — phần lớn đã không hoạt động. Nếu chỉ 10% trong số
họ quay lại, lưu lượng từ phân khúc này sẽ tăng gấp 2–3 lần. Họ có
game yêu thích (54% page view là cùng một game), và điểm này rất có
ích: **tái kích hoạt có thể dựa trên game yêu thích, không cần
dựa trên khám phá.**

### 4. Phân khúc cũ đã bỏ sót phân khúc số 1 (Vào rồi thoát)

Một phiên bản phân tích trước chỉ nhìn vào mức độ sử dụng site, không
nhìn vào user làm gì khi ở trên site. Với chỉ feature về lưu lượng,
phân khúc Vào rồi thoát đã vô hình — họ trông giống một Khách chơi
thử nhỏ ở mức lưu lượng. Khi thêm các feature về ý định (tỷ trọng
trang chủ, tỷ trọng search, tỷ trọng vào thẳng game), phân khúc Vào
rồi thoát hiện ra. **Đây là khác biệt giữa đo lường lưu lượng và
đo lường hành vi.**

---

## Phân tích này cho phép làm gì

Mỗi phân khúc gợi ý một chiến lược khác nhau:

| Phân khúc | % | Chiến lược |
|---|---|---|
| Vào rồi thoát 🔴 | 22% | Cải thiện trang chủ. Đưa ra gợi ý tốt hơn, game hot, prompt "chơi cái này trước". Mục tiêu: biến ít nhất 10% thành Khách chơi thử. |
| Khách chơi thử 🟡 | 43% | Tái kích hoạt dựa trên game yêu thích. Push notification hoặc email giới thiệu game lần cuối họ chơi. Mục tiêu: đưa họ quay lại trong 14 ngày. |
| Power user 🟢 | 35% | Giữ chân họ. Họ đang làm đúng những gì ta muốn. Gợi ý game mới theo tag/genre ưa thích. Mục tiêu: duy trì retention 28 ngày. |

Những chiến lược này chưa được triển khai. Chúng là đầu vào cho
bước tiếp theo (chiến lược gợi ý theo phân khúc).

---

## Những gì chúng tôi CHƯA làm

Để trung thực về giới hạn của phân tích:

- **Chưa đo lường hiệu quả của hệ thống gợi ý.** Nói "cải thiện
  trang chủ cho Vào rồi thoát" mới chỉ là giả thuyết. Chúng tôi
  chưa chạy thử nghiệm để xem nó có tác dụng không.

- **Các cụm là tĩnh.** Một user Power user hôm nay có thể thành
  Khách chơi thử tháng sau. Chúng tôi chưa theo dõi sự chuyển đổi
  giữa các cụm.

- **Một site, một khoảng thời gian.** Đây là 1games.io, 28 ngày
  kết thúc ngày 1 tháng 10. Các cụm sẽ thay đổi theo thời gian và
  sẽ khác cho zapgames.io và 1000games.io.

- **K=3 là lựa chọn tốt nhất của thuật toán.** Chúng tôi đã thử
  3, 4, và 5 cụm; 3 thắng trên chỉ số chất lượng (silhouette).
  4 hoặc 5 cụm có thể tìm ra các phân khúc phụ có ý nghĩa, nhưng
  dữ liệu nói 3 cụm là phân chia sạch nhất.

---

## Tìm dữ liệu ở đâu

| File | Nội dung |
|---|---|
| `d:\GR\03_data\processed\user_features\clusters_1games_2026-10-01.csv` | Bảng đầy đủ — 32,701 user, mọi đặc trưng, kèm cột `cluster_id` |
| `d:\GR\03_data\processed\user_features\cluster_report.md` | Báo cáo số chi tiết theo từng cụm |
| `d:\GR\03_data\processed\user_features\cluster_summary.md` | Tóm tắt ngắn |
| `d:\GR\01_documentation\User_Segmentation_Methodology_v3.md` | Methodology kỹ thuật (cho data team) |

---

**Ngày tạo:** 2026-10-02
**Phương pháp:** K-Means clustering (K=3, 25 đặc trưng, sklearn)
**Khoảng thời gian:** 2026-09-03 đến 2026-10-01 (28 ngày)
**Cohort:** user trưởng thành (lần đầu xuất hiện ≥28 ngày trước khi kết thúc khoảng)
**Site:** 1games.io
