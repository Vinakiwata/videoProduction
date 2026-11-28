# Báo cáo kiểm duyệt — Timeline tổng

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `timeline` · checklist "Kiểm duyệt timeline tổng" v2
- **Bắt đầu:** 2026-11-28T16:23:55+07:00 · **Chốt:** 2026-11-28T16:23:56+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

7 mục: 6 đạt, 0 trượt, 0 lỗi kiểm tra, 1 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `05_timeline` | `dir:8f5a6a96238f` |
| `04_voice/voice_manifest.yaml` | `d39cfc5c3750a77c` |
| `02_design/storyboard.yaml` | `369ae12028c325bd` |
| `01_script/script.yaml` | `81fe36e768ec0aea` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| TML-A01 | Cấu trúc | Có timeline, phụ đề và manifest | Chặn | auto | ✅ Đạt | Có đủ: 05_timeline/timeline.yaml, 05_timeline/subtitles.srt, 05_timeline/manifest.json |
| TML-A02 | Đồng bộ | Timeline nhất quán — giọng khớp đo thật ±1 khung, khung hình phủ kín, cue nằm trong khung, thứ tự đúng kịch bản | Chặn | auto | ✅ Đạt | 13 đoạn, 18 khung, 83 cue, 6 SFX; tổng 1602 khung = 53.4s @ 30 fps; giọng khớp manifest ±1 khung. |
| TML-A03 | Phụ đề | Phụ đề ≤ 2 dòng, ≤ 42 ký tự/dòng, ≥ 1 giây, không chồng, chữ khớp lời | Chặn | auto | ✅ Đạt | 19 cụm phụ đề: ≤ 2 dòng, ≤ 42 ký tự/dòng, ≥ 1.0s, không chồng; chữ khớp lời kịch bản. |
| TML-A04 | Đồng bộ | Timeline dựng từ đúng kịch bản, storyboard, giọng, brief hiện tại | Chặn | auto | ✅ Đạt | Timeline khớp đầu vào hiện tại. |
| TML-C03 | Đồng bộ | Mọi hoạt ảnh và SFX rơi đúng khoảnh khắc có nghĩa của lời | Nghiêm trọng | Claude | ✅ Đạt | Timeline khoá theo giọng thật lời văn nghiêm túc: 1602 khung = 53,4 giây, 18 khung hình, 83 cue, 6 SFX. Đã đối chiếu 12 mốc với vị trí từ khoá trong lời (ước theo tỉ lệ âm tiết trong đoạn):<br>- Khỉ thắc mắc (khung 110) so với "từ đâu mà có": sớm 0,23 giây.<br>- Nhãn "axit nhẹ": lần dựng đầu sớm 2,1 giây; đã lùi trong storyboard (0,56 → 0,68), giờ sớm khoảng 1 giây.<br>- Nhãn "muối": sớm 1,1 giây. "rất ít muối": sớm 0,5 giây. "nước ngọt mới": sớm 0,8 giây. "Muối dồn về biển": sớm 1,2 giây so với "tất cả các dòng sông", nhưng hiện cùng lúc câu "Còn biển nhận muối" bắt đầu.<br>- "Nước bay đi, muối ở lại": muộn 0,13 giây so với "muối không bốc hơi"; Khỉ ngạc nhiên muộn 0,5 giây.<br>- "hàng triệu năm" (gõ chữ): sớm 0,9 giây; Khỉ ôm Trái Đất sớm 0,17 giây.<br>- "Nguồn thêm: đáy biển": đúng lúc "núi lửa". Khoáng chất bay lên: sớm 0,4 giây so với "khoáng chất".<br>Các nhãn vào sớm khoảng 1 giây là có chủ ý để kịp đọc. Không cue nào muộn hơn lời quá 0,5 giây.<br>SFX: pop khi Khỉ thắc mắc hiện; lách tách khi hạt muối bong khỏi đá; róc rách khi muối trôi; pop nhẹ khi mây hiện; whoosh khi mây trôi đi; click khi nút đăng ký hiện — đều đúng hành động. |
| TML-C05 | Âm thanh | Nhạc nền có đánh dấu giảm âm (ducking) khi có giọng, có nguồn và giấy phép | Nghiêm trọng | Claude | ➖ Không áp dụng | Rãnh music rỗng: công đoạn này chưa dùng nhạc nền. Nhạc (có giấy phép, ducking) sẽ được chọn và kiểm ở Tool mix (09). |
| TML-C07 | Nhịp | Nhịp thở giữa các câu tự nhiên — không hụt hơi, không lê thê | Nghiêm trọng | Claude | ✅ Đạt | params: breath 0,6 giây (cùng cảnh), breath_scene 0,9 giây, question_extra 0,1 giây. Ngắt giữa câu trong đoạn 0,45 giây (câu hỏi 0,55). 6 chỗ ngắt đoạn: S02-01, S03-01, S04-03, S05-01 = 0,6 giây; S03-02, S04-04 = 0,9 giây (sang cảnh). Đúng các giá trị chủ dự án đã nghe và xác nhận "ổn" ở giong_ban_3_toan_bai.mp3 (28/11). |
