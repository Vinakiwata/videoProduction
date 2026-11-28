# Báo cáo kiểm duyệt — Timeline tổng

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `timeline` · checklist "Kiểm duyệt timeline tổng" v2
- **Bắt đầu:** 2026-11-28T11:16:40+07:00 · **Chốt:** 2026-11-28T11:16:54+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

7 mục: 6 đạt, 0 trượt, 0 lỗi kiểm tra, 1 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `05_timeline` | `dir:1255811f8daa` |
| `04_voice/voice_manifest.yaml` | `82404499a83aa6f2` |
| `02_design/storyboard.yaml` | `239630144b5d47ca` |
| `01_script/script.yaml` | `c15dd0b128e4e0af` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| TML-A01 | Cấu trúc | Có timeline, phụ đề và manifest | Chặn | auto | ✅ Đạt | Có đủ: 05_timeline/timeline.yaml, 05_timeline/subtitles.srt, 05_timeline/manifest.json |
| TML-A02 | Đồng bộ | Timeline nhất quán — giọng khớp đo thật ±1 khung, khung hình phủ kín, cue nằm trong khung, thứ tự đúng kịch bản | Chặn | auto | ✅ Đạt | 13 đoạn, 18 khung, 77 cue, 6 SFX; tổng 1563 khung = 52.1s @ 30 fps; giọng khớp manifest ±1 khung. |
| TML-A03 | Phụ đề | Phụ đề ≤ 2 dòng, ≤ 42 ký tự/dòng, ≥ 1 giây, không chồng, chữ khớp lời | Chặn | auto | ✅ Đạt | 19 cụm phụ đề: ≤ 2 dòng, ≤ 42 ký tự/dòng, ≥ 1.0s, không chồng; chữ khớp lời kịch bản. |
| TML-A04 | Đồng bộ | Timeline dựng từ đúng kịch bản, storyboard, giọng, brief hiện tại | Chặn | auto | ✅ Đạt | Timeline khớp đầu vào hiện tại. |
| TML-C03 | Đồng bộ | Mọi hoạt ảnh và SFX rơi đúng khoảnh khắc có nghĩa của lời | Nghiêm trọng | Claude | ✅ Đạt | Timeline dựng lại vẫn 1563 khung = 52,1 giây, 18 khung hình, 6 SFX. So với bản đã duyệt, chỉ S01-01-a đổi: hai phần tử sông + biển gộp thành một cảnh cửa sông, vào bằng fade ở khung 0 (18 khung), thay cho draw sông + fade biển. Cảnh hiện ngay khi bắt đầu câu 'Sông đổ ra biển', đúng lúc. Các phần tử nền e0 (A-NEN-MUA) không có lượt vào nên không thêm cue. Các cue còn lại giữ nguyên mốc đã kiểm: 'Nước bay đi, muối ở lại' ở 0,50 câu so với 'Nhưng muối' ở ≈ 0,55; khoáng chất ở 0,70 so với 'thả khoáng chất' ở ≈ 0,75; 'axit nhẹ' và 'muối' vào sớm 1,3–1,5 giây có chủ ý để đủ thời gian đọc. Không cue nào vào muộn hơn lời quá 0,5 giây. |
| TML-C05 | Âm thanh | Nhạc nền có đánh dấu giảm âm (ducking) khi có giọng, có nguồn và giấy phép | Nghiêm trọng | Claude | ➖ Không áp dụng | Rãnh music rỗng: công đoạn này chưa dùng nhạc nền. Nhạc (có giấy phép, ducking) sẽ được chọn và kiểm ở Tool mix (09). |
| TML-C07 | Nhịp | Nhịp thở giữa các câu tự nhiên — không hụt hơi, không lê thê | Nghiêm trọng | Claude | ✅ Đạt | params: breath 0,6 giây (cùng cảnh), breath_scene 0,9 giây, question_extra 0,1 giây. Ngắt giữa câu trong đoạn 0,45 giây (câu hỏi 0,55). 6 chỗ ngắt đoạn: S02-01, S03-01, S04-03, S05-01 = 0,6 giây; S03-02, S04-04 = 0,9 giây (sang cảnh). Đúng các giá trị chủ dự án đã nghe và xác nhận "ổn" ở giong_ban_3_toan_bai.mp3 (28/11). |
