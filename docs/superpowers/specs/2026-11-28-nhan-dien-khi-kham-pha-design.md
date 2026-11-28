# Bộ nhận diện "Khỉ Khám Phá" và linh vật trong mỗi clip

**Ngày:** 28/11/2026
**Người quyết định:** chủ dự án (Vinakiwata)

## Vì sao
Kênh muốn duy trì lâu dài thì người xem phải nhận ra kênh ngay. Chủ dự án đưa vào một ảnh tổng của bộ nhận diện, gồm logo, 3 avatar, ảnh bìa, 7 biểu cảm, khẩu hiệu và 5 màu. Yêu cầu có hai phần:
1. Đưa bộ nhận diện vào mỗi clip.
2. Xuất từng file để upload lên YouTube và TikTok.

## Quyết định của chủ dự án
- **Đổi toàn bộ kênh** sang Khỉ Khám Phá: tên, khẩu hiệu, bảng màu. Hồ sơ kênh mới là `channels/khi-kham-pha/channel.yaml`.
- **Vị trí của Khỉ:** phản ứng ở các điểm nhấn và có mặt ở cảnh kết. Chủ dự án **không chọn** logo góc màn hình và intro.
- **Dùng PNG gốc** của Khỉ, không vẽ lại bằng SVG.

## Thiết kế
- **Kho bộ nhận diện** (`channels/khi-kham-pha/brand/`):
  - `goc/bo_nhan_dien.png`: ảnh tổng gốc.
  - `xuat.py`: script tách file, chạy lại được.
  - `xuat/`: file upload, kèm hướng dẫn.
    - Avatar YouTube 800×800.
    - Avatar TikTok 800 và 200.
    - Ảnh bìa YouTube 2560×1440, nội dung nằm gọn trong vùng an toàn 1546×423.
    - Hình mờ video 150×150.
    - Logo nền trong suốt.
    - 7 sticker 512 px.
  - `mascot/`: các PNG mà video dùng.
- **Màu:**
  - Bảng màu kênh: #0078E0, #FFC907, #FFFFFF, #5E270E, #FD8305, #669F2D. Năm màu lấy mẫu từ ảnh, cộng thêm trắng.
  - Chữ trắng trên #0078E0 chỉ đạt 4,41:1, nên **mọi chữ đặt trên tấm nền nâu gỗ** (`text_plate.always`), giống bảng tên trong logo.
  - DSN-A05 đo tương phản qua tấm nền.
- **Linh vật trong dây chuyền:**
  - `brand.mascot` liệt kê từng biểu cảm kèm lúc nào dùng. Storyboard dùng asset `kind: mascot` + `expression`.
  - `vp animation sync` chép PNG từ kho của kênh vào dự án, giữ nguyên lớp và ghi chú đã có.
  - DSN-A11 (`storyboard_mascot`): Khỉ phản ứng 2–3 lần ngoài cảnh kết. Cùng một Khỉ kéo dài qua các khung nối tiếp chỉ tính 1 lần. Cảnh kết bắt buộc có Khỉ. Biểu cảm phải có trong bộ nhận diện.
  - ANI-A07 (`mascot_png`): PNG RGBA nền trong suốt, trùng byte với bản gốc của kênh, không phóng to quá cỡ file khi lên hình.
  - Các kiểm tra SVG bỏ qua linh vật.
- **Video mẫu:**
  - Khỉ thắc mắc thay dấu hỏi ở câu hỏi mở đầu.
  - Khỉ ngạc nhiên lúc lộ đáp án "nước bay đi, muối ở lại".
  - Khỉ ôm Trái Đất ở đoạn "hàng triệu năm".
  - Cảnh kết: logo, Khỉ vui mừng, nút đăng ký, chuông, chữ "Cùng Khỉ nhé!" trên nền xanh trời.
  - Lời đọc giữ nguyên nên không phải tạo lại giọng.

## Giới hạn và rủi ro
- **Độ phân giải:** mọi file được cắt từ một ảnh 1536×1024. Mỗi biểu cảm gốc chỉ khoảng 150–200 px, avatar khoảng 257 px. Vì vậy Khỉ chỉ đặt ở cỡ ≤ 44% chiều cao khung. Nên thay bằng ảnh gốc độ phân giải cao.
- **Phong cách:** Khỉ vẽ chi tiết, cảnh vẽ phẳng. Hai phong cách tách bạch nhờ viền trắng kiểu sticker; đây là chủ ý thương hiệu.
- **Pháp lý:** tên file gốc cho thấy ảnh tạo bằng ChatGPT, nên phải gắn nhãn nội dung AI khi đăng (Luật AI 134/2025/QH15). Brief đã ghi điều này trong constraints.
