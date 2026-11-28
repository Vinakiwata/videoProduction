# Báo cáo kiểm duyệt — Timeline tổng

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `timeline` · checklist "Kiểm duyệt timeline tổng" v2
- **Bắt đầu:** 2026-11-28T10:43:37+07:00 · **Chốt:** 2026-11-28T10:43:52+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

7 mục: 6 đạt, 0 trượt, 0 lỗi kiểm tra, 1 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `05_timeline` | `dir:c1af891ff23d` |
| `04_voice/voice_manifest.yaml` | `82404499a83aa6f2` |
| `02_design/storyboard.yaml` | `82024fb70d2f43cf` |
| `01_script/script.yaml` | `c15dd0b128e4e0af` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| TML-A01 | Cấu trúc | Có timeline, phụ đề và manifest | Chặn | auto | ✅ Đạt | Có đủ: 05_timeline/timeline.yaml, 05_timeline/subtitles.srt, 05_timeline/manifest.json |
| TML-A02 | Đồng bộ | Timeline nhất quán — giọng khớp đo thật ±1 khung, khung hình phủ kín, cue nằm trong khung, thứ tự đúng kịch bản | Chặn | auto | ✅ Đạt | 13 đoạn, 18 khung, 79 cue, 6 SFX; tổng 1563 khung = 52.1s @ 30 fps; giọng khớp manifest ±1 khung. |
| TML-A03 | Phụ đề | Phụ đề ≤ 2 dòng, ≤ 42 ký tự/dòng, ≥ 1 giây, không chồng, chữ khớp lời | Chặn | auto | ✅ Đạt | 19 cụm phụ đề: ≤ 2 dòng, ≤ 42 ký tự/dòng, ≥ 1.0s, không chồng; chữ khớp lời kịch bản. |
| TML-A04 | Đồng bộ | Timeline dựng từ đúng kịch bản, storyboard, giọng, brief hiện tại | Chặn | auto | ✅ Đạt | Timeline khớp đầu vào hiện tại. |
| TML-C03 | Đồng bộ | Mọi hoạt ảnh và SFX rơi đúng khoảnh khắc có nghĩa của lời | Nghiêm trọng | Claude | ✅ Đạt | Đối chiếu cue với vị trí từ khoá (theo âm tiết). S04-01-a/e6 "Nước bay đi, muối ở lại" ở 0,50 câu, từ "Nhưng muối" ở ≈ 0,55: đúng lúc. S04-04-a/e3 khoáng chất ở 0,70, "thả khoáng chất" ở ≈ 0,75: đúng lúc. S02-01-a/e5 "axit nhẹ" ở 0,56 (lúc nói "hoà tan khí các bô ních"), sớm khoảng 1,5 giây trước chữ "chua". S02-02-b/e3 "muối" ở 0,74, sớm khoảng 1,3 giây trước "trong đó có muối". Hai nhãn sớm là chủ ý (cần đủ thời gian đọc, DSN-A07) và báo trước từ khoá. Không cue nào vào muộn hơn lời quá 0,5 giây. |
| TML-C05 | Âm thanh | Nhạc nền có đánh dấu giảm âm (ducking) khi có giọng, có nguồn và giấy phép | Nghiêm trọng | Claude | ➖ Không áp dụng | Rãnh music rỗng: công đoạn này chưa dùng nhạc nền. Nhạc (có giấy phép, ducking) sẽ được chọn và kiểm ở Tool mix (09). |
| TML-C07 | Nhịp | Nhịp thở giữa các câu tự nhiên — không hụt hơi, không lê thê | Nghiêm trọng | Claude | ✅ Đạt | params: breath 0,6 giây (cùng cảnh), breath_scene 0,9 giây, question_extra 0,1 giây. Ngắt giữa câu trong đoạn 0,45 giây (câu hỏi 0,55). 6 chỗ ngắt đoạn: S02-01, S03-01, S04-03, S05-01 = 0,6 giây; S03-02, S04-04 = 0,9 giây (sang cảnh). Đúng các giá trị chủ dự án đã nghe và xác nhận "ổn" ở giong_ban_3_toan_bai.mp3 (28/11). |
