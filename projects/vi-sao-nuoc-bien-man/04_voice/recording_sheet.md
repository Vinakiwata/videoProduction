# Phiếu thu âm — Vì sao nước biển lại mặn?

Thu trong phòng yên tĩnh, điện thoại cách miệng khoảng 20–30 cm, giữ cùng một khoảng cách và giọng cho mọi câu.
Mỗi câu lưu **một file riêng**, đặt tên đúng cột *Tên file* (đuôi .m4a / .wav / .mp3 đều được), rồi chép vào `04_voice/recordings/`. Đọc tự nhiên, để trống khoảng 0,5 giây trước và sau câu.

| Tên file | Câu cần đọc | Gợi ý thời lượng |
|---|---|---|
| `S01-01` | Sông đổ ra biển là nước ngọt. Vậy mà nước biển lại mặn chát. Muối từ đâu ra? | ~5.7s |
| `S02-01` | Khi rơi qua bầu trời, nước mưa hoà tan khí các-bon-níc và trở nên hơi chua. | ~5.0s |
| `S02-02` | Nước mưa chua nhẹ ấy chảy trên đá, bào mòn và hoà tan những hạt khoáng chất li ti, trong đó có muối. | ~7.2s |
| `S03-01` | Nước mưa gom về suối, về sông, mang theo lượng muối rất nhỏ, nhỏ đến mức ta không nếm ra. | ~6.3s |
| `S03-02` | Sông luôn được mưa bổ sung nước ngọt mới, nên vẫn ngọt. Còn biển thì nhận muối từ tất cả các dòng sông. | ~7.2s |
| `S04-01` | Dưới nắng, nước biển bốc hơi bay lên thành mây. Nhưng muối thì không bay theo, nó ở lại. | ~6.0s |
| `S04-03` | Mây lại mưa xuống đất, vòng lặp ấy kéo dài hàng triệu năm, muối trong biển tích dần đến độ mặn như hôm nay. | ~7.5s |
| `S04-04` | Thêm một nguồn nữa, núi lửa và các khe nứt nóng dưới đáy biển cũng thả khoáng chất vào nước. | ~6.3s |
| `S05-01` | Tóm lại, mưa hoà tan muối từ đá, sông chở muối ra biển, nước bốc hơi còn muối ở lại. | ~6.3s |
| `S05-02` | Đăng ký kênh để mỗi tuần cùng mình khám phá thêm một hiện tượng khoa học nhé! | ~5.4s |

Sau đó chạy: `python -m vp voice synth projects/<dự án> --engine recording`
