# Cảnh minh hoạ chân thật, màu tự nhiên (sửa đổi Tool 3 + Tool 6)

**Ngày:** 28/11/2026
**Người quyết định:** chủ dự án (Vinakiwata)

## Vì sao
Theo nhận xét của chủ dự án, hình "chưa chân thật". Ví dụ đúng ý: sông phải là một khung cảnh có núi, có cây và một dòng sông uốn lượn; biển phải là bãi biển. Trước đây cả bộ hình chỉ dùng 4 màu nhận diện, nên cảnh trông giống sơ đồ hơn là phong cảnh.

## Phương án đã cân nhắc
1. **Giữ 4 màu, tạo sắc độ bằng đậm nhạt.** Giữ được chất riêng của kênh, nhưng khó nhận ra đâu là sông, đâu là biển.
2. **Màu tự nhiên cho cảnh, vẫn vẽ phẳng.** Chủ dự án **chọn** phương án này sau khi xem bản nháp hai phương án.

Về phạm vi, chủ dự án chọn **chỉ áp dụng cho cảnh minh hoạ**. Icon (cốc, giọt, mũi tên, nút, chuông…), chữ và nút vẫn giữ 4 màu nhận diện.

## Thiết kế
- **Bộ nhận diện kênh và brief:** thêm `brand.scene_colors`, gồm 20 màu tự nhiên: trời, núi, đồi, cây, thân cây, đất, sông, biển (3 mức), cát (2 mức), đá (3 mức), dung nham. Câu `style` mô tả rõ luật mới.
- **Storyboard:**
  - Thêm loại asset `kind: scene`.
  - Thêm `scene_palette` (phải nằm trong `brand.scene_colors`).
  - Thêm `text_plate`: tấm nền tối đặt sau mọi chữ nằm trên cảnh.
- **Luật màu:**
  - DSN-A06 và ANI-A03: chỉ asset `scene` được dùng màu cảnh, tối đa 16 màu mỗi cảnh. Icon, chữ, nút và nền khung vẫn chỉ dùng 4 màu nhận diện, tối đa 4 màu mỗi hình.
  - DSN-A05 (tương phản): nếu chữ nằm trên cảnh thì đo với **mọi** màu của cảnh, lấy trường hợp xấu nhất, có tính tấm nền nếu có. Thiếu tấm nền thì chữ vàng hoặc trắng trên trời sáng sẽ trượt.
- **Cảnh vẽ lại** (vẽ phẳng, có chiều sâu bằng các lớp xa → gần):
  - A-SONG: núi, đồi cây, sông uốn lượn.
  - A-CUA-SONG (mới): sông từ núi đổ ra bãi biển.
  - A-BIEN: bãi biển.
  - A-SUOI: sườn núi có 3 dòng suối.
  - A-NEN-MUA (mới): đồi dưới trời mưa.
  - A-DA: tảng đá thật có rêu và vết nứt.
  - A-DAY-BIEN: đáy biển có núi lửa và miệng phun nhiệt.
  - A-BAN-DO-SONG: bản đồ màu tự nhiên.
  - A-SANG-BIEN (mới): lớp sáng nhấp nháy trên vùng biển của bản đồ.
  - A-SONG-ICON (mới): giữ hình sông phẳng cũ cho chuỗi tóm tắt ở S05.
- **Bố cục:** cảnh chiếm cả khung (`box 0,0,100,100`). Phần tử minh hoạ đặt theo vị trí thật trong cảnh: hơi nước bốc lên từ mặt biển, muối nằm dưới mặt nước, khoáng chất bay ra từ miệng núi lửa.

## Để lại cho Tool 07
- Vẽ `text_plate` thành tấm bo góc sau chữ, mỗi bên rộng hơn chữ 0,4 em.
- Lớp cảnh nằm dưới cùng; các phần tử khác chồng lên theo thứ tự trong storyboard.
