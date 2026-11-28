---
name: vp-hoat-anh
description: Dùng khi cần vẽ, sửa hoặc duyệt hình hoạt ảnh 2D (06_animation) cho video trong repo này — biến danh mục asset của storyboard thành file SVG phẳng theo bộ nhận diện, tách lớp cho chuyển động, dựng tờ xem trước.
---

# Hoạt ảnh 2D (06_animation)

1. `python -m vp gate projects/<dự án> timeline` phải báo MỞ.
2. `python -m vp animation init projects/<dự án>` tạo `06_animation/assets.yaml`, mỗi asset trong storyboard có một mục với `file: assets/<ID>.svg`, nguồn và giấy phép.
3. Vẽ hình bằng **script sinh SVG** ở `06_animation/_src/ve_hinh.py`. Không vẽ tay từng file, để sửa một chỗ là vẽ lại được cả bộ.
   - **Màu:**
     - Icon, chữ và nút chỉ dùng 4 màu của kênh, tối đa 4 màu mỗi hình. Muốn có sắc độ thì dùng `fill-opacity`.
     - Cảnh (`kind: scene`) vẽ như phong cảnh thật: sông có núi, cây và dòng sông uốn lượn; biển là bãi biển. Chỉ dùng màu trong `brand.scene_colors`, tối đa 16 màu mỗi cảnh.
     - Cảnh viết ở `_src/canh.py`, vẽ trên khung 960×540.
     - Hình trắng đặt trên trời phải đạt tương phản ≥ 3:1.
   - **Phong cách:** phẳng, nét tròn (`stroke-linecap`/`linejoin="round"`), bóng đổ nhẹ #1B1B1F 25% cho vật đứng riêng. Hình nào lặp lại (giọt, hạt muối, mây) thì dùng chung một hàm để giữ đồng bộ.
   - **Lớp:** mỗi chi tiết có chuyển động nằm trong `<g id="…">`, rồi khai báo trong `layers` của `assets.yaml`.
   - **Tỉ lệ `viewBox`:** phải gần với tỉ lệ ô `box` của storyboard (rộng 1920 × w%, cao 1080 × h%). Dải ngang phủ hết bề rộng khung thì dùng `preserveAspectRatio="none"`.
   - **Hình chồng lên nhau** (ví dụ khoáng chất trên đáy biển): quy đổi toạ độ theo `box` của cả hai rồi dựng ảnh chồng để kiểm.
   - **Chữ trong hình:** chỉ dùng font của brief.
4. Ghi `motion_defaults` trong `assets.yaml` cho các lượt storyboard không ghi `ease`. Không được để chuyển động tuyến tính cứng, trừ flow, rotate và typewriter.
5. `python -m vp animation preview projects/<dự án>` tạo `assets_preview.png`. **Tự mở xem** ở cả hai nền rồi đối chiếu từng hình với mô tả trong storyboard: đủ chi tiết, đúng số lượng, có nhãn.
6. `python -m vp animation lint projects/<dự án>` phải báo SẠCH.
6b. Ghép thử các khung theo đúng toạ độ storyboard: cảnh ở lớp dưới cùng, các phần tử chồng lên, chữ có tấm nền `text_plate`. Kiểm từng khung: vật có nằm đúng chỗ thật không (muối dưới mặt nước, hơi nước bốc từ mặt biển), có lớp nào bị che không.
7. Duyệt bằng skill `vp-kiem-duyet`, công đoạn `animation`. Sửa SVG thì cổng hết hiệu lực, phải dựng lại preview và duyệt lại.
