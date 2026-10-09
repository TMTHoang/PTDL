# Phân tích danh mục ZapGames.io

**Ngày:** 2026-10-09
**Nguồn dữ liệu:** `D:\GR\zapgames_all.csv` (1.046 trò chơi, metadata đầy đủ) + ClickHouse `gm_page_facts` (khoảng 28 ngày 2026-09-10 → 2026-10-08)
**Phạm vi:** Top 20% danh mục theo `users_with_as_top` (209 / 1.046 trò chơi) — phân khúc này mang lại 80.7% người dùng và 81.3% lượt xem trang.

> **Lưu ý phương pháp luận (v3):** Chỉ số tương tác được tính trên `gm_page_facts`, hệ thống ghi nhận khoảng 26% lưu lượng v2 đầy đủ. Các tỷ lệ (eng%, phân phối p50/p90) có giá trị để so sánh giữa các trò chơi trong phạm vi báo cáo này; số liệu tuyệt đối sẽ thấp hơn baseline v2. Bộ lọc bot được áp dụng ở upstream và không thực hiện tại đây.

## 1. Tóm tắt điều hành

**ZapGames.io có danh mục 1.046 trò chơi — 20% số trò chơi (theo lượng người dùng) chiếm phần lớn lưu lượng.**

| Chỉ tiêu | Giá trị |
|---|---|
| Tổng số trò chơi trong danh mục | 1.046 |
| Tổng users-with-this-game-as-top | 57.876 |
| Tổng lượt xem trang | 1.904.119 |
| Phân khúc top-20% (được phân tích) | 209 trò chơi (19%) |
| Top-20% thị phần người dùng | 80.7% |
| Top-20% thị phần lượt xem trang | 81.3% |
| eng% trung vị trong phân khúc | 51.2% |
| Phiên p50 trung vị | 12.4s |
| Phiên p90 trung vị | 135.9s |

**Phân bố tier (eng% × độ phủ):**

| Tier | Định nghĩa | Số trò chơi | Tỷ trọng |
|---|---|---:|---:|
| T1_Star | eng% cao + độ phủ cao | 58 | 27% |
| T2_Niche_Loyal | eng% cao + độ phủ thấp | 58 | 27% |
| T3_Discovery | eng% thấp + độ phủ cao | 45 | 21% |
| T4_Underperformer | eng% thấp + độ phủ thấp | 48 | 22% |

**Ba phát hiện lớn:**

1. **Độ phủ (reach) tập trung rất cao.** 20% danh mục sở hữu ~81% người dùng. Quy luật Pareto là có thật: hàng trăm trò chơi chỉ có dưới 20 người dùng mỗi trò và đóng góp dưới 1% lưu lượng.
2. **Tương tác (engagement) *bình thường* trong top 20%.** eng% trung vị ở mức ~51% — không có "bí mật" nào cả. Điều phân biệt ngôi sao với niche là *độ phủ*, không phải chất lượng tương tác.
3. **Các trò Discovery Hub là một hiện tượng riêng.** Một số trang nhỏ (được kéo bởi traffic tìm kiếm đến các tựa game nổi tiếng như gta-5-online, rocket-league) có `users_eng` rất lớn nhưng `eng%` rất thấp — đây là các *trang đổ bộ (landing pages)* chứ không phải *trò chơi giữ chân người chơi*.

## 2. Hồ sơ danh mục — Thể loại & Tag

### 2.1 Phân bố thể loại (theo users-with-as-top)

| Thể loại | Trò chơi | Users (top) | Lượt xem trang | % users | % PV |
|---|---:|---:|---:|---:|---:|
| action | 175 | 17.300 | 547.760 | 29.9% | 28.8% |
| sports | 148 | 15.208 | 505.161 | 26.3% | 26.5% |
| arcade | 252 | 9.850 | 332.739 | 17.0% | 17.5% |
| multiplayer | 80 | 4.498 | 181.536 | 7.8% | 9.5% |
| simulation | 133 | 3.772 | 116.257 | 6.5% | 6.1% |
| casual | 92 | 2.857 | 90.582 | 4.9% | 4.8% |
| horror | 64 | 1.863 | 50.457 | 3.2% | 2.6% |
| puzzle | 67 | 1.219 | 35.705 | 2.1% | 1.9% |
| rpg | 9 | 598 | 21.256 | 1.0% | 1.1% |
| zap-games | 5 | 294 | 7.936 | 0.5% | 0.4% |
| strategy | 17 | 237 | 8.616 | 0.4% | 0.5% |
| education | 4 | 180 | 6.114 | 0.3% | 0.3% |

**Cách đọc:** Danh mục bị chi phối bởi **arcade (24.1%), action (16.7%), sports (14.1%), simulation (12.7%)** — cộng lại chiếm 67.6% catalog. Xét theo users, **action dẫn đầu (nhiều khả năng vì các tựa action như veck-io, frontwarsio, gta-5-online, undead-invasion đều nằm ở top)**. Multiplayer chiếm 7.6% số trò chơi nhưng chỉ ~3-4% người dùng (một vài game io. viral đang kéo lệch số đếm catalog).

### 2.2 Top 30 Tag (theo users-with-as-top)

| Tag | Trò chơi | Users (top) |
|---|---:|---:|
| 3D | 656 | 53.689 |
| Challenge | 578 | 52.618 |
| Skill | 254 | 40.350 |
| Survival | 274 | 39.100 |
| Fast Paced | 262 | 38.029 |
| Competition | 223 | 36.354 |
| Car | 200 | 35.123 |
| Physics | 181 | 34.003 |
| Speed | 198 | 33.566 |
| PvP | 179 | 31.741 |
| Driving | 173 | 31.327 |
| 2D | 221 | 26.995 |
| Shooting | 144 | 25.373 |
| Obstacle | 164 | 24.896 |
| Ball | 127 | 24.604 |
| Scary | 129 | 23.289 |
| Stunt | 96 | 21.694 |
| Collecting | 130 | 19.641 |
| Incremental | 97 | 19.605 |
| Combat | 116 | 18.064 |
| Soccer | 72 | 17.838 |
| Racing | 76 | 17.565 |
| io | 75 | 17.561 |
| Vehicle | 83 | 17.361 |
| Platformer | 93 | 16.275 |
| Design | 74 | 15.027 |
| Football | 55 | 14.997 |
| Ragdoll Physics | 52 | 14.473 |
| Gun | 68 | 14.073 |
| Run | 62 | 13.464 |

**Tag xuất hiện đồng thời (top 3 gắn nhiều nhất):** `3D` (63% trò chơi), `Challenge` (55%), `Survival` (26%). Danh mục thiên về **3D-first, challenge-driven, survival-friendly** — đặc trưng kiểu io./crazygames.

## 3. Top 20 trò chơi — theo users_eng (độ phủ)

| # | Slug | Thể loại | Users (eng) | Sessions | Eng% | s_p50 | s_p90 | s_avg | PV (catalog) |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | gta-5-online | action | 71.785 | 77.455 | 16.9% | 6.2s | 51.5s | 24.7s | 10.088 |
| 2 | rocket-league | sports | 12.384 | 14.821 | 23.3% | 11.7s | 61.8s | 31.0s | 4.444 |
| 3 | veck-io | action | 9.088 | 23.564 | 54.5% | 17.8s | 190.4s | 82.1s | 107.955 |
| 4 | 2v2io | multiplayer | 8.462 | 19.139 | 48.6% | 17.5s | 155.2s | 68.3s | 52.739 |
| 5 | golf-hit | sports | 8.375 | 19.563 | 52.2% | 9.5s | 134.1s | 20655.1s | 61.027 |
| 6 | frontwarsio | action | 6.863 | 20.696 | 49.9% | 9.6s | 96.0s | 39.8s | 71.853 |
| 7 | san-andreas-crime | action | 5.131 | 5.453 | 23.8% | 11.0s | 70.3s | 32.2s | 2.285 |
| 8 | undead-invasion | action | 4.670 | 11.930 | 51.3% | 11.4s | 125.4s | 54.7s | 30.296 |
| 9 | bowmasters-archery-shooting | action | 4.429 | 10.522 | 60.6% | 17.0s | 283.5s | 101.7s | 45.851 |
| 10 | gacha-life | simulation | 4.257 | 4.709 | 17.9% | 6.7s | 51.2s | 24.8s | 1.187 |
| 11 | shell-shockers | action | 4.048 | 5.016 | 25.0% | 8.0s | 77.7s | 34.0s | 3.265 |
| 12 | gta-6 | action | 3.861 | 4.340 | 39.5% | 20.7s | 117.5s | 52.2s | 3.553 |
| 13 | evil-nun | horror | 3.773 | 5.669 | 55.9% | 29.8s | 166.5s | 68.8s | 4.685 |
| 14 | horus-coffee-machine | simulation | 3.663 | 4.014 | 7.6% | 3.9s | 22.2s | 11.8s | 822 |
| 15 | vice-town-stories | action | 3.599 | 4.105 | 25.8% | 8.6s | 90.8s | 39.0s | 2.906 |
| 16 | basketball-hit | sports | 3.467 | 8.787 | 53.0% | 10.6s | 136.5s | 111.4s | 47.016 |
| 17 | sonic-exe | horror | 3.150 | 3.759 | 16.9% | 5.4s | 48.5s | 24.5s | 1.186 |
| 18 | dress-to-impress | casual | 2.917 | 3.473 | 21.6% | 7.1s | 63.4s | 30.2s | 2.107 |
| 19 | color-tunnel | arcade | 2.827 | 4.851 | 28.4% | 9.5s | 58.6s | 29.1s | 6.911 |
| 20 | size-it-up | puzzle | 2.726 | 3.064 | 15.8% | 3.8s | 51.0s | 21.6s | 6.931 |

**Nhận xét:**
- **Veck Io thống trị** (9.088 người dùng tương tác, 23.564 phiên, 54.5% eng%, p50=17.8s, p90=190.4s) — một flagship đích thực.
- **GTA 5 Online là hiện tượng Discovery Hub** (71.785 users_eng, chỉ 16.9% eng% — gấp 4 lần trò kế tiếp về độ phủ nhưng tương tác thấp nhất). Người dùng đổ vào, xem qua, rời đi. Đây là nam châm traffic tìm kiếm chứ không phải trò chơi mà người ta chơi trên ZapGames.
- **Các trò thể thao (golf-hit, basketball-hit, airborne-bmx) tụ lại ở eng% cao (52-57%)** với độ phủ trung bình — những người chơi chắc tay.
- **p90 phiên trung bình dao động 50-300s** cho các trò action/multiplayer, so với 200-650s cho một số mô phỏng single-player (block-craft, minefunio).

## 4. Top 20 trò chơi có tương tác cao nhất — theo eng% (lọc: eng_users ≥ 50)

| # | Slug | Thể loại | Eng% | Eng users | s_p50 | s_p90 | Tier |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | stickman-dragon-fight | action | 64.3% | 267 | 23.5s | 254.0s | T2_Niche_Loyal |
| 2 | obby-merge-a-nuke | multiplayer | 62.0% | 158 | 12.0s | 172.7s | T2_Niche_Loyal |
| 3 | sky-dart | sports | 61.7% | 303 | 15.1s | 195.1s | T2_Niche_Loyal |
| 4 | supermarket-simulator-store-manager | casual | 60.9% | 145 | 12.3s | 100.2s | T2_Niche_Loyal |
| 5 | bowmasters-archery-shooting | action | 60.6% | 2.682 | 17.0s | 283.5s | T1_Star |
| 6 | meelandio | multiplayer | 60.5% | 234 | 16.7s | 116.1s | T2_Niche_Loyal |
| 7 | basketball-orbit | sports | 60.2% | 238 | 16.3s | 234.4s | T2_Niche_Loyal |
| 8 | basketball-superstars | sports | 60.1% | 394 | 20.3s | 171.3s | T1_Star |
| 9 | table-tennis-game | sports | 60.1% | 200 | 28.9s | 406.9s | T2_Niche_Loyal |
| 10 | rally-racer-dirt | sports | 59.9% | 646 | 15.6s | 119.5s | T1_Star |
| 11 | car-chaos | sports | 59.7% | 1.175 | 14.6s | 130.6s | T1_Star |
| 12 | stickman-coin-flip | casual | 59.6% | 895 | 13.5s | 107.1s | T1_Star |
| 13 | orbit-kick | arcade | 59.5% | 278 | 18.9s | 152.9s | T2_Niche_Loyal |
| 14 | super-star-car | arcade | 59.5% | 119 | 15.3s | 104.5s | T2_Niche_Loyal |
| 15 | crashy-rush | arcade | 59.3% | 386 | 16.0s | 152.9s | T1_Star |
| 16 | wheelie-life | sports | 59.0% | 212 | 17.9s | 159.3s | T2_Niche_Loyal |
| 17 | drift-hunters | sports | 59.0% | 200 | 18.6s | 178.2s | T2_Niche_Loyal |
| 18 | track-dash | arcade | 58.8% | 481 | 10.1s | 170.7s | T1_Star |
| 19 | stickman-clash | action | 58.5% | 361 | 19.0s | 210.1s | T1_Star |
| 20 | soflo-wheelie-life | sports | 58.3% | 714 | 23.9s | 133.4s | T1_Star |

## 5. Viên ngọc ẩn — Tương tác cao, độ phủ thấp

Đây là những trò chơi mà người dùng *dính* (eng% ≥ 50%, s_p90 ≥ 100s) nhưng chưa lọt vào danh sách theo độ phủ. Ứng viên cho cross-promotion, đặt trên trang chủ, hoặc spotlight trong danh mục.

| # | Slug | Thể loại | Eng% | Eng users | s_p50 | s_p90 | Top PV (catalog) |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | tap-road-2 | arcade | 52.7% | 157 | 12.4s | 119.0s | 3.678 |
| 2 | meelandio | multiplayer | 60.5% | 234 | 16.7s | 116.1s | 1.823 |
| 3 | a-small-world-cup-2 | sports | 55.6% | 299 | 11.9s | 113.5s | 1.470 |
| 4 | basketball-stars | sports | 52.2% | 180 | 11.2s | 142.8s | 1.429 |
| 5 | capybara-mart | simulation | 51.2% | 234 | 8.8s | 119.8s | 1.398 |
| 6 | color-rush | arcade | 52.8% | 190 | 10.1s | 109.1s | 1.355 |
| 7 | escape-road | action | 55.5% | 238 | 9.9s | 153.1s | 1.269 |
| 8 | ragdoll-playground | action | 57.0% | 276 | 15.5s | 124.1s | 1.148 |
| 9 | supermarket-master | simulation | 52.3% | 182 | 10.3s | 107.5s | 1.037 |
| 10 | super-star-car | arcade | 59.5% | 119 | 15.3s | 104.5s | 1.034 |
| 11 | mr-racer-car-racing | arcade | 54.5% | 216 | 14.1s | 122.7s | 1.013 |
| 12 | smash-karts | sports | 51.7% | 196 | 17.8s | 117.9s | 987 |
| 13 | overtide-io | action | 51.2% | 221 | 15.5s | 159.7s | 953 |
| 14 | stickman-dragon-fight | action | 64.3% | 267 | 23.5s | 254.0s | 945 |
| 15 | crazy-shark | arcade | 54.2% | 283 | 15.4s | 172.3s | 906 |
| 16 | redcoats-io | multiplayer | 52.8% | 266 | 13.6s | 151.1s | 888 |
| 17 | basketball-bros | sports | 50.0% | 161 | 9.4s | 132.8s | 876 |
| 18 | bottle-hop | arcade | 53.8% | 199 | 8.6s | 170.0s | 869 |
| 19 | hazmob-fps-online-shooter | action | 53.6% | 207 | 10.4s | 128.7s | 823 |
| 20 | ragdoll-hit-stickman | action | 51.2% | 206 | 15.9s | 130.5s | 814 |

## 6. Phân tích tier — Bốn góc phần tư cho thấy điều gì

Trục: **eng%** (trung vị trong phân khúc = 51.2%) chia tại 50%, **users_eng** (trung vị = 538) chia tại trung vị.

### 6.1 T1_Star (58 trò chơi)

**Flagship** — eng% cao + độ phủ cao. Đây là những trò chơi nên đứng đầu trang chủ, định hình thương hiệu và được ưu tiên ngân sách quảng bá.

Top 10 theo users_eng:

| Slug | Thể loại | Users_eng | Eng% | s_p50 | s_p90 |
|---|---|---:|---:|---:|---:|
| veck-io | action | 9.088 | 54.5% | 17.8s | 190.4s |
| golf-hit | sports | 8.375 | 52.2% | 9.5s | 134.1s |
| undead-invasion | action | 4.670 | 51.3% | 11.4s | 125.4s |
| bowmasters-archery-shooting | action | 4.429 | 60.6% | 17.0s | 283.5s |
| evil-nun | horror | 3.773 | 55.9% | 29.8s | 166.5s |
| basketball-hit | sports | 3.467 | 53.0% | 10.6s | 136.5s |
| ragdoll-hit | action | 2.120 | 56.0% | 16.2s | 171.5s |
| survival-race | sports | 2.092 | 53.1% | 15.5s | 162.6s |
| ragdoll-archers | action | 2.046 | 54.8% | 11.0s | 121.5s |
| car-chaos | sports | 1.967 | 59.7% | 14.6s | 130.6s |

### 6.2 T2_Niche_Loyal (58 trò chơi)

**Niche trung thành** — eng% cao, độ phủ thấp. Khán giả đã có nhưng nhỏ. Đây là các ứng viên *discovery*: cross-promote từ các ngôi sao T1, gợi ý trong widget trò chơi liên quan, gắn tag mạnh tay.

Top 10 theo users_eng:

| Slug | Thể loại | Users_eng | Eng% | s_p50 | s_p90 |
|---|---|---:|---:|---:|---:|
| a-small-world-cup-2 | sports | 538 | 55.6% | 11.9s | 113.5s |
| crazy-shark | arcade | 522 | 54.2% | 15.4s | 172.3s |
| redcoats-io | multiplayer | 504 | 52.8% | 13.6s | 151.1s |
| boeing-flight-simulator | simulation | 496 | 54.8% | 21.6s | 153.5s |
| sky-dart | sports | 491 | 61.7% | 15.1s | 195.1s |
| ragdoll-playground | action | 484 | 57.0% | 15.5s | 124.1s |
| cookie-clicker | casual | 474 | 57.2% | 12.7s | 131.2s |
| orbit-kick | arcade | 467 | 59.5% | 18.9s | 152.9s |
| capybara-mart | simulation | 457 | 51.2% | 8.8s | 119.8s |
| ramp-xtreme | sports | 450 | 53.8% | 14.9s | 160.0s |

### 6.3 T3_Discovery (45 trò chơi)

**Discovery Hub** — eng% thấp, độ phủ cao. Người dùng đổ vào đây nhưng không chơi sâu. Hoặc (a) trang là nam châm tìm kiếm (hiệu ứng gta-5-online) — giữ lại, đây là vàng SEO; hoặc (b) bản thân trò chơi nông / không giữ chân — cân nhắc hạ ưu tiên hoặc thay thế.

Top 10 theo users_eng:

| Slug | Thể loại | Users_eng | Eng% | s_p50 | s_p90 |
|---|---|---:|---:|---:|---:|
| gta-5-online | action | 71.785 | 16.9% | 6.2s | 51.5s |
| rocket-league | sports | 12.384 | 23.3% | 11.7s | 61.8s |
| 2v2io | multiplayer | 8.462 | 48.6% | 17.5s | 155.2s |
| frontwarsio | action | 6.863 | 49.9% | 9.6s | 96.0s |
| san-andreas-crime | action | 5.131 | 23.8% | 11.0s | 70.3s |
| gacha-life | simulation | 4.257 | 17.9% | 6.7s | 51.2s |
| shell-shockers | action | 4.048 | 25.0% | 8.0s | 77.7s |
| gta-6 | action | 3.861 | 39.5% | 20.7s | 117.5s |
| horus-coffee-machine | simulation | 3.663 | 7.6% | 3.9s | 22.2s |
| vice-town-stories | action | 3.599 | 25.8% | 8.6s | 90.8s |

### 6.4 T4_Underperformer (48 trò chơi)

**Kém hiệu quả** — cả hai chỉ số đều thấp. Cân nhắc: loại bỏ, thay thế, hoặc thử nghiệm thiết kế lại. Chúng đang chiếm chỗ trong danh mục mà không đóng góp độ phủ hay tương tác.

Top 10 theo users_eng:

| Slug | Thể loại | Users_eng | Eng% | s_p50 | s_p90 |
|---|---|---:|---:|---:|---:|
| arcade-glide | arcade | 534 | 49.2% | 9.0s | 123.5s |
| world-guessr | puzzle | 526 | 44.5% | 5.6s | 96.4s |
| pixel-path | action | 516 | 48.8% | 12.7s | 146.0s |
| war-the-knights | action | 500 | 35.4% | 11.2s | 109.4s |
| wave-race | arcade | 475 | 47.4% | 7.3s | 153.8s |
| ragdoll-drop | arcade | 471 | 48.8% | 7.0s | 170.9s |
| wheelie-master | sports | 460 | 45.9% | 13.9s | 129.8s |
| grow-a-garden | simulation | 454 | 41.2% | 13.7s | 123.0s |
| tag-game | multiplayer | 451 | 49.9% | 17.2s | 159.3s |
| granny | horror | 443 | 44.2% | 14.8s | 134.2s |

## 7. Khuyến nghị

### 7.1 Trang chủ & trang thể loại
- Dẫn đầu bằng **T1_Star** trong các mục theo thể loại — đây là những trò chơi người dùng sẽ thường muốn chơi tiếp theo.
- **Không nên** đặt **T3_Discovery Hub** ở vị trí biên tập — độ phủ cao của chúng đến từ tìm kiếm, không phải vì chúng là trò chơi hay trên ZapGames.

### 7.2 Cross-promotion
- **T2_Niche_Loyal** là những ứng viên tốt nhất cho widget "Người chơi thích X cũng thích Y". Tương tác đã có; lượng người chơi nhỏ nhưng trung thành.
- Cụ thể nên hiển thị các trò **T2** trên lối ra trang của các trò cùng thể loại (T1_Star cùng genre).

### 7.3 Dọn dẹp danh mục
- **48 trò chơi trong T4_Underperformer** đang kéo danh mục đi xuống. Cân nhắc loại bỏ, A/B thiết kế lại, hoặc thay bằng các trò upload mới.
- Đối với phần đuôi dài (1.046 − 209 = 837 trò chơi với dưới 50 người dùng mỗi trò), đánh giá xem giá trị SEO có vượt chi phí duy trì catalog hay không.

### 7.4 Trọng tâm thu hút
- **3D, Challenge, Fast-Paced** là các tag dẫn đầu theo users. Trừ khi thử nghiệm một thể loại mới, các upload mới nên nghiêng về nhóm tag này (trong trường hợp thử nghiệm, Sports và Multiplayer là phương án kế tiếp).
- **Multiplayer** đang được đại diện quá mức trong số đếm catalog (7.6%) nhưng lại dưới hiệu suất về users (chỉ vài phần trăm) — đánh giá xem làn sóng "io." còn tác dụng hay người dùng đã chuyển sang chỗ khác.

## 8. Phương pháp luận & Lưu ý

**Nguồn dữ liệu**

- **Metadata danh mục** — `D:\GR\zapgames_all.csv` (1.046 dòng, bao phủ 100% name, genre, tags). Được re-crawl qua Wayback Machine cho các slug từ `zapgames.io/sitemap.xml`.
- **Chỉ số tương tác** — ClickHouse `gm_page_facts` (phương pháp luận v3 theo `D:\GR\engagement_workflow\docs\methodology_v3.md`). Khoảng 28 ngày 2026-09-10 → 2026-10-08.
- **Phân khúc top-20%** — sắp xếp theo `users_with_as_top` (số người dùng mà trò chơi này là trò chơi *top* của họ — proxy cho quy mô cộng đồng, không phải lưu lượng thô).

**Định nghĩa chỉ số tương tác**

- `users_eng` — số client duy nhất có ít nhất một measurement trên trang của trò chơi này.
- `eng_users` — tập con có tổng thời gian trên trang > 30 giây (định nghĩa người dùng có tương tác).
- `eng_pct` — `eng_users / users_eng × 100`.
- `s_p50`, `s_p90`, `s_avg` — phân vị thời lượng phiên, đo bằng giây.

**Lưu ý**

1. Phương pháp luận v3 chỉ bao phủ khoảng 26% so với v2 (theo `methodology_v3.md`). Số liệu tuyệt đối `users_eng` và `sessions` sẽ thấp hơn so với truy vấn v2 tương đương. Tỷ lệ và phân vị vẫn có giá trị.
2. Không áp dụng bộ lọc bot (không có cột `bot` trong v3). Bot đã được lọc ở upstream trong quá trình materialize `gm_page_facts`.
3. Khoảng 28 ngày được cố định từ 2026-09-10 đến 2026-10-08 — khoảng thời gian đầy đủ gần nhất của `gm_page_facts` tại thời điểm truy vấn.
4. `users_with_as_top` là proxy người dùng duy nhất từ crawl catalog, không phải cùng chỉ số với `users_eng` (cái sau là khoảng 28 ngày từ `gm_page_facts`). Chúng tương quan nhưng không giống nhau — dùng `users_with_as_top` để xếp hạng, dùng `users_eng` cho bối cảnh tương tác.
5. GTA 5 Online có trong danh mục zapgames (1.189 users_with_as_top) nhưng không phải trò chơi có thể chơi trên ZapGames — đây là một nam châm tìm kiếm. `users_eng` rất cao (71.785) nhưng `eng_pct` rất thấp (16.9%) là dấu hiệu nhận biết.

**Đầu ra**

- `D:\GR\zapgames_portfolio_report.md` — báo cáo này
- `D:\GR\zapgames_portfolio_supporting.csv` — toàn bộ top-209 với phân loại tier
- `D:\GR\zapgames_portfolio_genre.csv` — thống kê theo thể loại (toàn bộ 1.046 trò chơi)
- `D:\GR\zapgames_portfolio_tags.csv` — thống kê theo tag (top 60 tag)
- `D:\GR\zapgames_p50p90_engpct.csv` — đầu ra truy vấn thô (top 209 × 12 chỉ số)
