# Storyboard — Vì sao nước biển lại mặn?

> Sinh tự động từ `storyboard.yaml` bằng `python -m vp design view`. Ảnh phác thảo: `storyboard.png`, `frames/`.

- **Bảng màu:** #0B3D91, #FFD23F, #FFFFFF, #1B1B1F
- **Font:** Be Vietnam Pro / Be Vietnam Pro
- **Phong cách:** Minh hoạ phẳng (flat), nét tròn, bóng đổ nhẹ, tối đa 4 màu mỗi khung

## Thư viện asset

| Mã | Loại | Mô tả | Màu |
|---|---|---|---|
| A-SONG | illustration | Dòng sông uốn lượn nhìn từ trên cao, dải trắng có 2-3 vạch sóng xanh đậm bên trong, chảy từ trái sang phải | #FFFFFF, #0B3D91 |
| A-BIEN | illustration | Mặt biển dạng dải sóng tròn nhiều lớp màu xanh đậm, viền ngọn sóng trắng, chiếm phần dưới khung | #0B3D91, #FFFFFF |
| A-COC-SONG | icon | Cốc thuỷ tinh viền trắng, nước trong, giữa có biểu tượng giọt nước trắng; nhãn nhỏ "sông" dưới đáy cốc | #FFFFFF |
| A-COC-BIEN | icon | Cốc thuỷ tinh viền trắng, nước xanh đậm, giữa có 3 hạt muối hình lập phương trắng; nhãn nhỏ "biển" dưới đáy cốc | #FFFFFF, #0B3D91 |
| A-HOI | icon | Dấu chấm hỏi lớn bo tròn, đặc, màu vàng, bóng đổ nhẹ | #FFD23F |
| A-MAY | illustration | Đám mây phẳng 3 khối tròn chồng nhau, màu trắng, đáy phẳng | #FFFFFF |
| A-GIOT-MUA | icon | Giọt mưa hình giọt nước trắng, có điểm sáng nhỏ; nhiều giọt dùng chung asset này | #FFFFFF |
| A-GIOT-MUA-CHUA | icon | Giọt mưa trắng có viền vàng dày và 2 bọt nhỏ vàng bên trong — biểu thị nước mưa hơi chua (axit nhẹ) | #FFFFFF, #FFD23F |
| A-PHANTU-KHI | diagram | Cụm 5-6 phân tử khí: mỗi phân tử là 1 chấm tròn giữa nối 2 chấm nhỏ hai bên (kiểu CO2), màu trắng, bay lơ lửng | #FFFFFF |
| A-DA | illustration | Khối đá tảng bo tròn nằm nghiêng, thân xanh đậm, viền và vết nứt màu trắng, nhìn ngang | #0B3D91, #FFFFFF |
| A-HAT-MUOI | icon | Cụm hạt muối li ti hình lập phương trắng, vài hạt to hơn có điểm sáng, dùng để bong khỏi đá và trôi theo nước | #FFFFFF |
| A-SUOI | diagram | Ba dòng suối mảnh màu trắng từ trên trái chảy xuống, nhập thành một dòng sông rộng dần sang phải | #FFFFFF |
| A-KINH-LUP | icon | Kính lúp tay cầm vàng, mắt kính tròn trong suốt viền vàng dày; bên trong phóng to dòng nước có đúng 3 hạt muối thưa | #FFD23F, #FFFFFF |
| A-BAN-DO-SONG | diagram | Bản đồ phẳng nhìn từ trên: đất tối bên trái, 5 con sông trắng từ nhiều phía cùng đổ vào vùng biển xanh đậm bên phải; trên mỗi sông có chuỗi chấm trắng nhỏ chạy về biển | #1B1B1F, #FFFFFF, #0B3D91 |
| A-MAT-TROI | illustration | Mặt trời tròn vàng với 8 tia ngắn bo tròn | #FFD23F |
| A-HOI-NUOC | diagram | Các chấm hơi nước trắng nhỏ bay lên theo 3 mũi tên chấm chấm hướng lên; không có hạt muối nào trong luồng bay lên | #FFFFFF |
| A-MUOI-O-LAI | icon | Hàng hạt muối lập phương trắng nằm lại dưới mặt nước biển, lấp lánh nhẹ | #FFFFFF |
| A-VONG-TUAN-HOAN | diagram | Vòng tròn 4 chặng nối bằng mũi tên vàng cong chạy theo chiều kim đồng hồ: mưa (giọt trắng) → đá → sông → biển → mây; mỗi chặng là icon trắng đơn giản | #FFD23F, #FFFFFF |
| A-DAY-BIEN | diagram | Mặt cắt đáy biển: nước xanh đậm phía trên, đáy tối; giữa là núi lửa nhỏ có miệng phát sáng vàng, bên phải một khe nứt toả các vệt nhiệt vàng (chưa có khoáng chất — xem A-KHOANG-CHAT) | #0B3D91, #1B1B1F, #FFD23F, #FFFFFF |
| A-KHOANG-CHAT | diagram | Chuỗi chấm khoáng chất trắng nhỏ bay lên từ miệng núi lửa và khe nứt, toả dần vào làn nước | #FFFFFF |
| A-MUI-TEN | icon | Mũi tên ngang dày bo tròn màu vàng, chỉ sang phải | #FFD23F |
| A-NUT-DANG-KY | ui | Nút bo tròn lớn màu vàng, chữ "ĐĂNG KÝ" màu tối đậm ở giữa, tự thiết kế — không dùng logo YouTube | #FFD23F, #1B1B1F |
| A-CHUONG | icon | Chuông thông báo trắng phẳng, có 2 vạch rung nhỏ hai bên | #FFFFFF |

## S01 · Móc

### S01-01 — Sông đổ ra biển là nước ngọt. Vậy mà nước biển lại mặn chát. Muối từ đâu ra?

**S01-01-a** · span [0, 0.39] · vào: `cut` · camera: `pan_right` · nền #1B1B1F
*Mục đích:* Thấy dòng sông nước ngọt đổ ra biển — vế đầu của nghịch lý

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| ⭐ e1 | A-SONG | -5,35,70,30 | draw @0 1s | flow |  |
| e2 | A-BIEN | 55,25,50,75 | fade @0.1 0.5s | bob |  |

*Ghi chú:* Dòng sông chảy liên tục vào biển, điểm hợp lưu ở khoảng 60% chiều ngang.

**S01-01-b** · span [0.39, 1] · vào: `zoom_through` · camera: `static` · nền #0B3D91
*Mục đích:* Đặt hai cốc cạnh nhau — sông ngọt, biển mặn — rồi bật câu hỏi

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| e1 | A-COC-SONG | 18,30,20,40 | pop @0 0.4s |  |  |
| e2 | A-COC-BIEN | 62,30,20,40 | pop @0.15 0.4s |  |  |
| ⭐ e3 | A-HOI | 44,28,12,36 | pop @0.6 0.35s | bob |  |
| e4 | chữ "Sông ngọt → Biển mặn?" (title, 96px, #FFD23F) | 15,74,70,14 | fade @0.38 0.3s |  |  |

🔊 pop ← e3.enter

*Ghi chú:* Zoom xuyên qua mặt biển của khung trước để vào khung hai cốc. Cốc biển hơi nghiêng để thấy hạt muối.

### S01-02 — *(im lặng)*

**S01-02-a** · span [0, 1] · vào: `match_cut` · camera: `zoom_in` · nền #0B3D91
*Mục đích:* Giữ câu hỏi thêm 1 giây cho người xem tự đoán

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| e1 | A-COC-SONG | 18,30,20,40 |  |  |  |
| e2 | A-COC-BIEN | 62,30,20,40 |  |  |  |
| ⭐ e3 | A-HOI | 44,28,12,36 |  | wiggle |  |
| e4 | chữ "Sông ngọt → Biển mặn?" (title, 96px, #FFD23F) | 15,74,70,14 |  |  | fade @1 0.3s |

*Ghi chú:* Nối tiếp liền mạch với S01-01-b (không thấy vết cắt); chỉ dấu hỏi lắc và camera tiến nhẹ.

## S02 · Mưa hoà tan muối trong đá

### S02-01 — Khi rơi qua bầu trời, nước mưa hoà tan khí cacbonic và trở nên hơi chua.

**S02-01-a** · span [0, 1] · vào: `crossfade` · camera: `pan_down` · nền #0B3D91
*Mục đích:* Giọt mưa hút khí từ không khí và trở nên hơi chua

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| e1 | A-MAY | 30,6,40,22 | fade @0 0.4s |  |  |
| ⭐ e2 | A-GIOT-MUA | 45,32,10,18 | drop @0.05 0.6s |  |  |
| e3 | A-PHANTU-KHI | 20,35,22,25 | slide_right @0.35 0.7s |  | scale_out @0.6 0.3s |
| e4 | A-GIOT-MUA-CHUA | 45,32,10,18 | morph @0.62 0.4s | pulse |  |
| e5 | chữ "axit nhẹ" (label, 64px, #FFD23F) | 58,40,25,10 | fade @0.56 0.3s |  |  |

*Ghi chú:* Phân tử khí bay vào trong giọt mưa rồi biến mất; giọt mưa trắng biến hình (morph) thành giọt viền vàng đúng lúc nói "hơi chua".

### S02-02 — Nước mưa chua nhẹ ấy chảy trên đá, bào mòn và hoà tan những hạt khoáng chất li ti, trong đó có muối.

**S02-02-a** · span [0, 0.35] · vào: `push_up` · camera: `static` · nền #1B1B1F
*Mục đích:* Giọt mưa chua rơi xuống và chảy trên mặt đá

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| ⭐ e1 | A-DA | 20,40,60,50 | slide_up @0 0.5s |  |  |
| e2 | A-GIOT-MUA-CHUA | 40,8,8,14 | drop @0.1 0.6s | flow |  |

*Ghi chú:* Nhiều giọt mưa chua (cùng asset) rơi liên tục và chảy thành vệt dọc sườn đá.

**S02-02-b** · span [0.35, 1] · vào: `match_cut` · camera: `zoom_in` · nền #1B1B1F
*Mục đích:* Cận cảnh — nước làm bong hạt li ti khỏi đá, trong đó có muối

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| e1 | A-DA | -10,30,120,80 |  |  |  |
| ⭐ e2 | A-HAT-MUOI | 40,38,22,18 | grow @0.15 0.8s | shimmer |  |
| e3 | chữ "muối" (label, 72px, #FFD23F) | 64,30,16,11 | pop @0.6 0.3s |  |  |

🔊 lách tách nhẹ ← e2.enter

*Ghi chú:* Zoom vào vết nứt trên đá; hạt li ti bong ra theo dòng nước, vài hạt sáng lên thành hình lập phương muối khi nói "trong đó có muối".

### S02-03 — *(im lặng)*

**S02-03-a** · span [0, 1] · vào: `match_cut` · camera: `pan_right` · nền #1B1B1F
*Mục đích:* Hạt muối theo dòng nước trôi đi — chuẩn bị sang chặng sông

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| e1 | A-DA | -10,30,120,80 |  |  |  |
| ⭐ e2 | A-HAT-MUOI | 40,38,22,18 | slide_right @0 1s |  |  |

🔊 nước chảy róc rách ← e2.enter

*Ghi chú:* Camera và hạt muối cùng trôi sang phải, nối hướng chảy sang cảnh sông.

## S03 · Sông chở muối ra biển

### S03-01 — Nước mưa gom về suối, về sông, mang theo lượng muối rất nhỏ, nhỏ đến mức ta không nếm ra.

**S03-01-a** · span [0, 0.35] · vào: `crossfade` · camera: `zoom_out` · nền #1B1B1F
*Mục đích:* Nước mưa gom thành suối rồi thành sông

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| ⭐ e1 | A-SUOI | 5,10,90,80 | draw @0 1.4s | flow |  |

**S03-01-b** · span [0.35, 1] · vào: `match_cut` · camera: `static` · nền #1B1B1F
*Mục đích:* Kính lúp cho thấy sông chỉ mang rất ít muối

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| e1 | A-SONG | 0,35,100,35 |  | flow |  |
| ⭐ e2 | A-KINH-LUP | 35,20,30,55 | scale_in @0 0.5s |  |  |
| e3 | chữ "rất ít muối" (label, 64px, #FFD23F) | 66,22,28,10 | fade @0.2 0.3s |  |  |

*Ghi chú:* Trong mắt kính chỉ có đúng 3 hạt muối thưa thớt, phần còn lại là nước trong.

### S03-02 — Sông luôn được mưa bổ sung nước ngọt mới, nên vẫn ngọt. Còn biển thì nhận muối từ tất cả các dòng sông.

**S03-02-a** · span [0, 0.52] · vào: `cut` · camera: `static` · nền #1B1B1F
*Mục đích:* Mưa liên tục bổ sung nước ngọt nên sông vẫn ngọt

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| e1 | A-SONG | 0,55,100,28 |  | flow |  |
| e2 | A-MAY | 32,4,36,18 | slide_down @0 0.5s |  |  |
| ⭐ e3 | A-GIOT-MUA | 38,22,24,34 | drop @0.1 0.6s | flow |  |
| e4 | chữ "nước ngọt mới" (label, 64px, #FFFFFF) | 60,82,34,10 | fade @0.28 0.3s |  |  |

**S03-02-b** · span [0.52, 1] · vào: `zoom_through` · camera: `zoom_out` · nền #1B1B1F
*Mục đích:* Mọi con sông cùng đổ muối về một vùng biển

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| e1 | A-BAN-DO-SONG | 0,0,100,100 | fade @0 0.5s | flow |  |
| ⭐ e2 | A-BIEN | 62,15,38,70 |  | pulse |  |
| e3 | chữ "Muối dồn về biển" (label, 64px, #FFD23F) | 6,82,60,10 | fade @0.1 0.3s |  |  |

*Ghi chú:* Camera lùi từ một dòng sông ra toàn bản đồ; chuỗi chấm trắng trên mọi sông chạy về biển, biển sáng nhẹ khi nói "tất cả các dòng sông".

## S04 · Bốc hơi giữ muối lại

### S04-01 — Dưới nắng, nước biển bốc hơi bay lên thành mây. Nhưng muối thì không bay theo, nó ở lại.

**S04-01-a** · span [0, 1] · vào: `crossfade` · camera: `static` · nền #0B3D91
*Mục đích:* Nước bốc hơi bay lên thành mây, muối ở lại trong biển

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| e1 | A-MAT-TROI | 8,6,16,28 | scale_in @0 0.5s | rotate |  |
| e2 | A-BIEN | 0,60,100,40 |  | bob |  |
| ⭐ e3 | A-HOI-NUOC | 40,25,20,38 | slide_up @0.1 1s | flow |  |
| e4 | A-MAY | 38,6,26,16 | pop @0.45 0.4s |  |  |
| e5 | A-MUOI-O-LAI | 30,74,40,12 | fade @0.6 0.4s | shimmer |  |
| e6 | chữ "Nước bay đi, muối ở lại" (label, 64px, #FFD23F) | 62,32,33,18 | fade @0.5 0.3s |  |  |

🔊 pop nhẹ ← e4.enter

*Ghi chú:* Mũi tên hơi nước chỉ mang chấm trắng (nước) bay lên; hàng muối dưới biển sáng lên đúng lúc nói "muối thì không bay theo".

### S04-02 — *(im lặng)*

**S04-02-a** · span [0, 1] · vào: `match_cut` · camera: `static` · nền #0B3D91
*Mục đích:* Nhịp nghỉ — muối lấp lánh ở lại, mây trôi về đất liền

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| e1 | A-MAT-TROI | 8,6,16,28 |  | rotate |  |
| e2 | A-BIEN | 0,60,100,40 |  | bob |  |
| e4 | A-MAY | 38,6,26,16 |  |  | slide_left @0.2 0.8s |
| ⭐ e5 | A-MUOI-O-LAI | 30,74,40,12 |  | shimmer |  |
| e6 | chữ "Nước bay đi, muối ở lại" (label, 64px, #FFD23F) | 62,32,33,18 |  |  | fade @1 0.3s |

🔊 whoosh nhẹ ← e4.exit

*Ghi chú:* Mây trôi sang trái (về phía đất liền ở bên trái theo quy ước hướng) để mở vòng tuần hoàn.

### S04-03 — Mây lại mưa xuống đất, vòng lặp ấy kéo dài hàng triệu năm, muối trong biển tích dần đến độ mặn như hôm nay.

**S04-03-a** · span [0, 0.22] · vào: `push_left` · camera: `static` · nền #1B1B1F
*Mục đích:* Mây mưa xuống đất liền — vòng lặp bắt đầu lại

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| ⭐ e1 | A-MAY | 30,8,40,22 | slide_left @0 0.5s |  |  |
| e2 | A-GIOT-MUA | 32,32,36,20 | drop @0.2 0.5s | flow |  |
| e3 | A-DA | 25,62,50,30 |  |  |  |

**S04-03-b** · span [0.22, 1] · vào: `crossfade` · camera: `zoom_out` · nền #1B1B1F
*Mục đích:* Vòng tuần hoàn quay qua hàng triệu năm, muối tích dần tới độ mặn hôm nay

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| ⭐ e1 | A-VONG-TUAN-HOAN | 30,10,40,72 | draw @0 1s | rotate |  |
| e2 | chữ "hàng triệu / năm" (title, 80px, #FFD23F) | 5,36,25,22 | typewriter @0.15 1s |  |  |
| e3 | A-COC-BIEN | 74,35,14,32 | scale_in @0.6 0.5s | pulse |  |

*Ghi chú:* Chữ "hàng triệu năm" gõ ra như bộ đếm; cốc nước biển bên phải hiện dần nhiều hạt muối hơn rồi dừng ở mức hiện nay (không tăng tiếp).

### S04-04 — Thêm một nguồn nữa, núi lửa và các khe nứt nóng dưới đáy biển cũng thả khoáng chất vào nước.

**S04-04-a** · span [0, 1] · vào: `zoom_through` · camera: `zoom_in` · nền #0B3D91
*Mục đích:* Nguồn phụ — núi lửa và khe nứt nóng dưới đáy biển thả khoáng chất

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| ⭐ e1 | A-DAY-BIEN | 0,0,100,100 | fade @0 0.5s | pulse |  |
| e3 | A-KHOANG-CHAT | 30,30,45,40 | slide_up @0.7 0.8s | flow |  |
| e2 | chữ "Nguồn thêm: đáy biển" (label, 64px, #FFD23F) | 6,8,44,10 | fade @0.1 0.3s |  |  |

*Ghi chú:* Miệng núi lửa và khe nứt phát sáng nhịp chậm; chấm khoáng chất (e3) bay lên đúng lúc nói "thả khoáng chất vào nước".

## S05 · Chốt và kêu gọi

### S05-01 — Tóm lại, mưa hoà tan muối từ đá, sông chở muối ra biển, nước bốc hơi còn muối ở lại.

**S05-01-a** · span [0, 1] · vào: `crossfade` · camera: `static` · nền #0B3D91
*Mục đích:* Tóm ba mắt xích thành một chuỗi nhìn một lần là nhớ

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| e1 | A-GIOT-MUA-CHUA | 8,30,16,30 | pop @0.1 0.35s |  |  |
| e2 | A-MUI-TEN | 27,40,10,10 | draw @0.35 0.3s |  |  |
| e3 | A-SONG | 40,32,20,26 | pop @0.4 0.35s |  |  |
| e4 | A-MUI-TEN | 63,40,10,10 | draw @0.6 0.3s |  |  |
| ⭐ e5 | A-MAT-TROI | 76,30,16,30 | pop @0.65 0.35s |  |  |
| e6 | chữ "Mưa" (label, 64px, #FFFFFF) | 8,64,16,10 | fade @0.1 0.3s |  |  |
| e7 | chữ "Sông" (label, 64px, #FFFFFF) | 42,64,16,10 | fade @0.4 0.3s |  |  |
| e8 | chữ "Bốc hơi" (label, 64px, #FFFFFF) | 74,64,20,10 | fade @0.65 0.3s |  |  |

*Ghi chú:* Ba biểu tượng hiện lần lượt đúng từng vế câu; mũi tên vẽ nối giữa. Mặt trời tượng trưng chặng bốc hơi trên biển.

### S05-02 — Đăng ký kênh để mỗi tuần cùng mình khám phá thêm một hiện tượng khoa học nhé!

**S05-02-a** · span [0, 1] · vào: `crossfade` · camera: `static` · nền #0B3D91
*Mục đích:* Mời đăng ký kênh

| Phần tử | Nội dung | Hộp (x,y,w,h %) | Vào | Lặp | Ra |
|---|---|---|---|---|---|
| ⭐ e1 | A-NUT-DANG-KY | 35,38,30,18 | pop @0.15 0.4s | pulse |  |
| e2 | A-CHUONG | 67,38,8,18 | pop @0.3 0.3s | wiggle |  |
| e3 | chữ "Mỗi tuần một hiện tượng" (label, 64px, #FFFFFF) | 25,64,50,10 | fade @0.3 0.3s |  |  |

🔊 click ← e1.enter
