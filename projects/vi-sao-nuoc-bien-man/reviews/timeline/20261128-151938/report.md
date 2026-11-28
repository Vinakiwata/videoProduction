# Báo cáo kiểm duyệt — Timeline tổng

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `timeline` · checklist "Kiểm duyệt timeline tổng" v2
- **Bắt đầu:** 2026-11-28T15:19:38+07:00 · **Chốt:** 2026-11-28T15:19:52+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

7 mục: 6 đạt, 0 trượt, 0 lỗi kiểm tra, 1 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `05_timeline` | `dir:b406f587d168` |
| `04_voice/voice_manifest.yaml` | `82404499a83aa6f2` |
| `02_design/storyboard.yaml` | `12397f0b17b24d7a` |
| `01_script/script.yaml` | `fcd113c10281807c` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| TML-A01 | Cấu trúc | Có timeline, phụ đề và manifest | Chặn | auto | ✅ Đạt | Có đủ: 05_timeline/timeline.yaml, 05_timeline/subtitles.srt, 05_timeline/manifest.json |
| TML-A02 | Đồng bộ | Timeline nhất quán — giọng khớp đo thật ±1 khung, khung hình phủ kín, cue nằm trong khung, thứ tự đúng kịch bản | Chặn | auto | ✅ Đạt | 13 đoạn, 18 khung, 83 cue, 6 SFX; tổng 1563 khung = 52.1s @ 30 fps; giọng khớp manifest ±1 khung. |
| TML-A03 | Phụ đề | Phụ đề ≤ 2 dòng, ≤ 42 ký tự/dòng, ≥ 1 giây, không chồng, chữ khớp lời | Chặn | auto | ✅ Đạt | 19 cụm phụ đề: ≤ 2 dòng, ≤ 42 ký tự/dòng, ≥ 1.0s, không chồng; chữ khớp lời kịch bản. |
| TML-A04 | Đồng bộ | Timeline dựng từ đúng kịch bản, storyboard, giọng, brief hiện tại | Chặn | auto | ✅ Đạt | Timeline khớp đầu vào hiện tại. |
| TML-C03 | Đồng bộ | Mọi hoạt ảnh và SFX rơi đúng khoảnh khắc có nghĩa của lời | Nghiêm trọng | Claude | ✅ Đạt | Timeline dựng lại: vẫn 1563 khung = 52,1 giây, 18 khung hình, 6 SFX; cue tăng từ 77 lên 83 vì thêm Khỉ và logo.<br>Mốc vào của Khỉ, đối chiếu với lời:<br>- S01-01-b khung 106 (3,5 giây): Khỉ thắc mắc vào đúng mốc cũ của dấu hỏi, khi câu hỏi 'vì sao…' được nêu.<br>- S04-01-a khung ≈ 904: Khỉ ngạc nhiên vào sau khi chữ 'Nước bay đi, muối ở lại' hiện ở 0,50, trùng 'Nhưng muối' ở ≈ 0,55.<br>- S04-03-b khung ≈ 1072: Khỉ ôm Trái Đất vào sau chữ 'hàng triệu năm' (0,15), trong lúc vòng tuần hoàn đang quay.<br>- S05-02-a: logo ở khung 1467 và Khỉ vui mừng ở khung ≈ 1475, mở đầu câu mời đăng ký.<br>Các cue cũ giữ nguyên mốc đã kiểm. Không cue nào vào muộn hơn lời quá 0,5 giây. |
| TML-C05 | Âm thanh | Nhạc nền có đánh dấu giảm âm (ducking) khi có giọng, có nguồn và giấy phép | Nghiêm trọng | Claude | ➖ Không áp dụng | Rãnh music rỗng: công đoạn này chưa dùng nhạc nền. Nhạc (có giấy phép, ducking) sẽ được chọn và kiểm ở Tool mix (09). |
| TML-C07 | Nhịp | Nhịp thở giữa các câu tự nhiên — không hụt hơi, không lê thê | Nghiêm trọng | Claude | ✅ Đạt | params: breath 0,6 giây (cùng cảnh), breath_scene 0,9 giây, question_extra 0,1 giây. Ngắt giữa câu trong đoạn 0,45 giây (câu hỏi 0,55). 6 chỗ ngắt đoạn: S02-01, S03-01, S04-03, S05-01 = 0,6 giây; S03-02, S04-04 = 0,9 giây (sang cảnh). Đúng các giá trị chủ dự án đã nghe và xác nhận "ổn" ở giong_ban_3_toan_bai.mp3 (28/11). |
