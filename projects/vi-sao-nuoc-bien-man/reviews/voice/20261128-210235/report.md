# Báo cáo kiểm duyệt — Giọng đọc

- **Dự án:** vi-sao-nuoc-bien-man
- **Công đoạn:** `voice` · checklist "Kiểm duyệt giọng đọc" v3
- **Bắt đầu:** 2026-11-28T21:02:35+07:00 · **Chốt:** 2026-11-28T21:02:36+07:00

## Kết luận: ✅ ĐẠT — điểm chất lượng 100/100

10 mục: 10 đạt, 0 trượt, 0 lỗi kiểm tra, 0 không áp dụng.

## File đã niêm phong

| File | Mã băm |
|---|---|
| `04_voice` | `dir:f5a2e7a03987` |
| `01_script/script.yaml` | `29a4a3f1857290eb` |

## Toàn bộ checklist

| Mã | Nhóm | Mục | Mức | Chấm bởi | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|
| VOI-A01 | Cấu trúc | Có manifest giọng và file giọng đầy đủ | Chặn | auto | ✅ Đạt | Có đủ: 04_voice/voice_manifest.yaml, 04_voice/voice_full.wav |
| VOI-A02 | Kỹ thuật | Âm lượng giọng chuẩn và không vỡ tiếng | Chặn | auto | ✅ Đạt | Độ to -16.3 LUFS (mục tiêu -16±1.5), đỉnh thực -1.5 dBTP (tối đa -1). |
| VOI-A03 | Đồng bộ | Manifest khớp kịch bản hiện tại và file thật (văn bản đã đọc, mã băm, thời lượng đo) | Chặn | auto | ✅ Đạt | 10 đoạn giọng (vieneu-v3turbo (Mac, theo câu), Xuân Vĩnh, nâng tông +2.5 nửa cung), tổng lời 46.2s, tốc độ trung vị 4.41 âm tiết/giây; khớp kịch bản và file. |
| VOI-A04 | Chất lượng âm | Không dấu hiệu lỗi TTS — đỉnh ≤ −1 dBFS, lặng hai đầu ≤ 0,35s, lặng giữa câu ≤ 1s, tốc độ không lệch > 30% so với trung vị của chính giọng đó (và trong 2–6 âm tiết/giây) | Chặn | auto | ✅ Đạt | 10 đoạn: đỉnh ≤ -1.0 dBFS, lặng hai đầu ≤ 0.35s, lặng giữa câu ≤ 1.0s, tốc độ trong 2.0–6.0 âm tiết/giây, lệch ≤ 30% so với trung vị 4.48. |
| VOI-C01 | Độ chính xác | Đọc đúng 100% chữ trong kịch bản, không đọc sót, thừa hay sai | Chặn | Vinakiwata (chủ dự án, nghe) | ✅ Đạt | Chủ dự án nghe giong_khi_nghiem_tuc.mp3 (voice_full, 49,2 giây, Xuân Vĩnh +2,5 nửa cung, lời văn nghiêm túc) ngày 28/11/2026 16:19, phiếu nghe 1/3: 'Đúng hết' — đọc đủ và đúng từng chữ của 10 đoạn, không sót, thừa hay sai. VOI-A01 xác nhận spoken_text khớp kịch bản. Duyệt lại 28/11/2026 18:30 chỉ vì script.yaml đổi dòng visual của S05-02 (màn kết); đã so: lời đọc 10 đoạn trùng nguyên văn, 04_voice không đổi file nào, nên giữ nguyên kết quả nghe của chủ dự án. |
| VOI-C02 | Độ chính xác | Phát âm đúng tên riêng, số, viết tắt, từ nước ngoài | Chặn | Vinakiwata (chủ dự án, nghe) | ✅ Đạt | Chủ dự án nghe giong_khi_nghiem_tuc.mp3 (voice_full, 49,2 giây, Xuân Vĩnh +2,5 nửa cung, lời văn nghiêm túc), phiếu nghe 1/3: 'cacbonic' đọc đúng 'các bô ních' (meta.pronunciation). Lời không có số, viết tắt hay tên riêng nào khác. |
| VOI-C03 | Chất lượng âm | Không có tạp âm, tiếng lạ, méo, rè, bị cắt đầu/cuối câu | Chặn | Vinakiwata (chủ dự án, nghe) | ✅ Đạt | Chủ dự án nghe giong_khi_nghiem_tuc.mp3 (voice_full, 49,2 giây, Xuân Vĩnh +2,5 nửa cung, lời văn nghiêm túc), phiếu nghe 2/3: 'Sạch, không méo' — không tạp âm, không rè do nâng tông, không cắt đầu/cuối câu, kể cả câu cuối S05-02 đã làm chậm 8%. Máy đo: đỉnh ≤ −1 dBFS, lặng hai đầu ≤ 0,35 giây, −16 LUFS (VOI-A02/A03 đạt). |
| VOI-C04 | Chất lượng âm | Giọng đồng nhất giữa các đoạn (âm sắc, tốc độ, độ to) | Nghiêm trọng | Vinakiwata (chủ dự án, nghe) | ✅ Đạt | Chủ dự án nghe giong_khi_nghiem_tuc.mp3 (voice_full, 49,2 giây, Xuân Vĩnh +2,5 nửa cung, lời văn nghiêm túc), phiếu nghe 3/3: 'Đồng nhất, ổn'. Số đo hỗ trợ: cao độ trung vị 123 Hz, chênh giữa các đoạn 1,36 nửa cung (lần dí dỏm 2,5); tốc độ 3,9–4,9 âm tiết/giây sau khi cân (VOI-A04 đạt, lệch trung vị ≤ 30%); cùng một preset Xuân Vĩnh cho cả 10 đoạn. |
| VOI-C05 | Diễn cảm | Ngữ điệu đúng ý câu (câu hỏi lên giọng, nhấn từ khoá) | Nghiêm trọng | Vinakiwata (chủ dự án, nghe) | ✅ Đạt | Chủ dự án nghe giong_khi_nghiem_tuc.mp3 (voice_full, 49,2 giây, Xuân Vĩnh +2,5 nửa cung, lời văn nghiêm túc), phiếu nghe 3/3: ngữ điệu phù hợp lời văn nghiêm túc. Câu hỏi 'Muối trong biển từ đâu mà có?' kết bằng 'mà có?' rõ ý hỏi. Lần trước (bản dí dỏm) chủ dự án báo có đoạn chưa ổn; bản này đã viết lại lời và chọn lượt theo độ đồng nhất. |
| VOI-C07 | Pháp lý | Giọng nhân bản (nếu có) có sự đồng ý của chủ giọng | Chặn | Claude | ✅ Đạt | Không nhân bản giọng người thật: dùng giọng dựng sẵn 'Xuân Vĩnh' của VieNeu-TTS v3 Turbo, rồi nâng tông +2,5 nửa cung bằng xử lý tín hiệu (rubberband), không có mẫu giọng của ai. Không cần sự đồng ý của chủ giọng. Giọng AI sẽ được gắn nhãn khi xuất bản (constraints của brief). |
