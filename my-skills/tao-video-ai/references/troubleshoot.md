# Sổ Tay Xử Lý Lỗi Video AI Thực Chiến (Troubleshooting & Remediation)
Kinh nghiệm khắc phục dị tật mô hình (Kling 3.0, Higgsfield, Stream 4.5, Runway Gen-3, Sora)

---

## 1. Bản Đồ Xử Lý Nhanh Các Lỗi Thường Gặp (Quick Fix Matrix)

| Hiện Tượng Lỗi | Nguyên Nhân Gốc | Giải Pháp Khắc Phục Triệt Để |
| :--- | :--- | :--- |
| **Logo hoặc chữ trên hộp bị méo / sai chính tả** | Mô hình khuếch tán sinh chữ tự do thay vì giữ nguyên hình khối | 1. Dùng tính năng **Element Pin / Regional Lock** (Kling 3.0, Higgsfield).<br>2. Cắt riêng ảnh cận cảnh vùng Logo (Macro Crop) làm Image Reference bổ sung.<br>3. Giảm Motion Strength xuống mức 2–3. |
| **Chi tiết vỉ thuốc, viên kẹo bị biến dạng thành chất lỏng/chảy xệ** | Prompt mô tả hành động mở hộp quá nhanh, vượt giới hạn vật lý | 1. Tách cảnh mở hộp thành 2 shot: Shot A (hộp đóng) $\rightarrow$ Cut $\rightarrow$ Shot B (vỉ đã mở sẵn).<br>2. Thêm negative prompt: `melting plastic, morphing geometry, liquefied objects`. |
| **Bàn tay cầm hộp bị thừa ngón / dị dạng ngón tay** | AI video gặp khó khăn khi render bàn tay tương tác vật thể | 1. Dùng prompt cụ thể: `delicate Asian hand with 5 perfectly formed fingers, wearing clean white cotton handling gloves`.<br>2. Thay cảnh cầm tay bằng cảnh hộp tự trượt trên bục quay xoay đĩa (Turntable). |
| **Màu sắc bao bì bị lệch (Xanh navy biến thành xanh lá / tím)** | Prompt ánh sáng quá phức tạp làm sai cân bằng trắng | 1. Bổ sung mã màu cụ thể: `#0F2537 medical navy blue box with #D4AF37 matte gold foil stamping`.<br>2. Thêm negative: `color shifts, neon purple tint, green cast`. |
| **Video bị giật cục, camera rung lắc dữ dội** | Không gán thuật toán camera motion hoặc prompt chứa từ khóa động từ mạnh | 1. Thêm cụm từ khóa chống rung: `smooth fluid gimbal stabilizer, steady camera track, zero jitter`.<br>2. Chọn camera preset: `Orbit` hoặc `Dolly In` thay vì để máy quay tự do. |
| **Mặt nhân vật KOC hoặc bé bị đờ đẫn hoặc biến dạng** | Tốc độ chuyển động khuôn mặt quá cao | 1. Giữ biểu cảm tĩnh hơn trong 3 giây đầu: `smiling gently, warm soft glance`.<br>2. Dùng negative prompt: `deformed eyes, asymmetrical pupils, frozen creepy smile`. |

---

## 2. Kỹ Thuật "Element Pin" & Multi-Image Reference (Kling 3.0 / Higgsfield)

### Khi nào cần dùng Element Pin?
Khi sản phẩm có logo thương hiệu bắt buộc phải chuẩn xác 100% từng nét chữ (như chữ *NANO GROWTH*, cờ Nhật Bản, nhãn phụ tiếng Việt).
- **Bước 1**: Tải ảnh sản phẩm gốc lên hệ thống.
- **Bước 2**: Dùng công cụ Brush tô vùng Logo & Tên thương hiệu.
- **Bước 3**: Chọn chế độ `Pin to Object` / `Element Persistence: 100%`.
- **Bước 4**: AI sẽ cho phép camera di chuyển xung quanh vật thể nhưng giữ nguyên vẹn điểm ảnh của vùng đã ghim, loại trừ 100% hiện tượng nhảy chữ hoặc biến dạng logo.

---

## 3. Chiến Lược "Ảnh Cận Cảnh Cứu Nguy" (Macro Crop Fallback)
Khi AI sinh ra viên nhai không giống viên nhai cacao thật mà giống viên thuốc tây màu trắng:
1. Chụp hoặc cắt một bức ảnh cận cảnh độ phân giải cao chỉ chứa 2 viên nhai cacao trên nền đĩa gốm.
2. Nạp ảnh này vào ô `Reference Image 2 (Texture Reference)` với trọng số (Weight) = 0.85.
3. Prompt kèm theo:
   ```text
   Match the texture and rich cocoa brown color of Reference Image 2 exactly. No white pharmaceutical pills.
   ```

---

## 4. Xử Lý Khi Higgsfield API Timeout Hoặc Quá Tải
Nếu hệ thống API của Higgsfield hoặc máy chủ video AI bị nghẽn:
1. Script `upload-higgsfield.py` được lập trình cơ chế **Fallback 3 Tầng**:
   - **Tầng 1**: Thử kết nối Higgsfield API với retry 3 lần kèm backoff (5s, 10s, 20s).
   - **Tầng 2**: Nếu API không khả dụng $\rightarrow$ Tự động xuất file kịch bản `higgsfield_payload.json` đã chuẩn hóa 100% các trường dữ liệu và mở link Web UI để người dùng paste 1-click.
   - **Tầng 3**: Đồng thời kích hoạt **Autonomous Video Engine** tích hợp sẵn (sử dụng Pillow + FFmpeg trên máy) để tự động xuất xưởng ngay lập tức file video MP4 15-25s hoàn chỉnh theo cấu trúc 4-shot (pan, zoom, orbit Ken Burns, banner thương hiệu, chuyển cảnh crossfade mượt mà) để tiến độ công việc không bao giờ bị đình trệ!
