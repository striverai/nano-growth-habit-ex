---
name: tao-video-ai
description: Hệ thống sản xuất video AI Cấp 5 chuyên nghiệp cho TikTok, Reels và YouTube Shorts theo quy trình 7 bước chuẩn workflow KP3 / Higgsfield Stream 4.5. Tự động hóa trọn gói từ khâu khảo sát ảnh sản phẩm, lập kịch bản phân cảnh 4 hồi, điều phối camera motion physics (Orbit, Dolly In, Pan Slow, Key Zoom), ghim logo chống méo hình (Element Pin), đến xuất bản video 15-25s dọc 9:16 hoàn chỉnh kèm âm thanh ambient mà không cần can thiệp thủ công (chỉ cần duyệt cuối).
---

# Tao-Video-AI — Hệ Thống Sản Xuất Video AI Cấp 5 (KP3 / Higgsfield Stream 4.5)

## 1. Giới Thiệu & Triết Lý Vận Hành
`tao-video-ai` là kỹ năng cấp cao (Level 5 Skill) thiết kế cho Agent tự chủ trong việc sản xuất video ngắn chuyển đổi cao (15–25 giây) cho thương hiệu **Nano Growth Habit EX** (dinh dưỡng hỗ trợ tăng trưởng chuẩn Nhật Bản).

Quy trình vận hành theo triết lý **"Zero-Touch Execution" (Thực thi tự động hóa hoàn toàn)**: Agent tiếp nhận một chủ đề (topic) hoặc hình ảnh sản phẩm, tự động hoàn thiện toàn bộ chuỗi mắt xích từ kịch bản, prompt chuyển động, payload API đến file video MP4 chất lượng cao sẵn sàng cho người dùng duyệt.

---

## 2. Cấu Trúc Thư Mục Chuẩn Cấp 5

```
skills/tao-video-ai/
├── SKILL.md                     # Quy trình 7 bước chuẩn mực cho Agent lặp lại
├── product-photos/              # Thư mục lưu trữ ảnh gốc sản phẩm độ nét cao
├── scripts/
│   ├── list-images.py           # Quét, phân tích tỷ lệ và phân loại vai trò ảnh sản phẩm
│   ├── gen-prompt.py            # Gọi LLM sinh kịch bản 4 phân cảnh & prompt cho Stream 4.5
│   └── upload-higgsfield.py     # Wrapper Higgsfield API & Bộ Engine Render MP4 tự động
├── assets/
│   ├── brand-style.md           # Quy chuẩn phong cách hình ảnh (Luxury / Casual KOC / Minimal)
│   ├── camera-prompts.md        # 5 Prompt chuyển động camera thắng (Orbit, Dolly In, Pan, Zoom, Multishot)
│   └── negative-prompt.txt      # Bộ negative prompt độc quyền lọc sạch biến dạng & dị tật AI
├── references/
│   ├── koc-format.md            # Khung kịch bản KOC giữ chân người xem TikTok 2026
│   ├── cinematic-format.md      # Quy chuẩn cinematic mở hộp & cận cảnh kết cấu
│   └── troubleshoot.md          # Sổ tay xử lý lỗi thực chiến (Element Pin, Macro Crop)
└── output/                      # Thư mục lưu trữ Storyboard JSON/MD, Payload và Video MP4 hoàn thiện
```

---

## 3. Quy Trình 7 Bước Tự Chủ (The 7-Step Autonomous Workflow)

```
[BƯỚC 1: Khảo sát ảnh sản phẩm]  --> list-images.py quét product-photos/
               |
[BƯỚC 2: Định vị phong cách]     --> brand-style.md (Luxury / Casual / Minimal)
               |
[BƯỚC 3: Lập kịch bản 4 hồi]     --> koc-format.md & cinematic-format.md (15-25s)
               |
[BƯỚC 4: Sinh Camera Motion]     --> gen-prompt.py phối hợp 5 camera motions
               |
[BƯỚC 5: Kích hoạt Guardrails]   --> negative-prompt.txt + Element Pin chống méo
               |
[BƯỚC 6: Render & Ghép video]    --> upload-higgsfield.py (Autonomous Engine)
               |
[BƯỚC 7: QA/QC & Bàn giao]       --> Xuất video MP4 1080x1920 gửi người dùng duyệt
```

---

### Bước 1: Khảo Sát & Phân Loại Ảnh Sản Phẩm (Ingest & Asset Discovery)
- **Mục tiêu**: Nhận diện hình thể, tỷ lệ khung hình và chọn ra góc chụp sản phẩm tối ưu làm ảnh tham chiếu (Image Reference).
- **Thực thi lệnh**:
  ```bash
  python scripts/list-images.py
  # Hoặc xuất JSON:
  python scripts/list-images.py --json --output output/product_assets.json
  ```
- **Tiêu chuẩn đầu vào**:
  - Độ phân giải khuyến nghị: $\ge 768 \times 768$ pixels.
  - Phân loại rõ: Ảnh bao bì chính (Hero Box), Ảnh vỉ kim loại (Blister Pack), Ảnh viên nhai cacao (Tablet Texture).

---

### Bước 2: Xác Định Định Vị Phong Cách Hình Ảnh (Visual Tone Alignment)
- **Mục tiêu**: Chọn tone thị giác phù hợp với mục đích chiến dịch dựa trên `assets/brand-style.md`:
  - **Tone Luxury**: Không gian y khoa đẳng cấp, bục đá cẩm thạch trắng, viền vàng kim, ánh sáng studio 5600K.
  - **Tone Casual / KOC**: Không gian gia đình Japandi ấm áp, thước đo chiều cao gỗ, ánh sáng ban mai, mẹ và bé.
  - **Tone Minimal**: Thẩm mỹ Wabi-Sabi, phông nền be nhạt, đĩa gốm mộc, tập trung vào viên nhai cacao.
- **Bảng màu nhận diện bắt buộc**: Navy (`#0F2537`), Gold (`#D4AF37`), Cacao (`#6B4423`).

---

### Bước 3: Lập Cấu Trúc Kịch Bản 4 Hồi Chuẩn 15–25s (Narrative Pacing)
Áp dụng công thức giữ chân người xem từ `references/koc-format.md`:
- **Hồi 1 (0.0s – 4.0s) — Visual Hook**: Cắt cảnh ngắt quán tính lướt màn hình, snap zoom vào sản phẩm.
- **Hồi 2 (4.0s – 9.0s) — Detail Formula**: Cận cảnh Macro nhãn khoa học Alpha-GPC, Canxi nano vỏ trứng & CPP.
- **Hồi 3 (9.0s – 15.0s) — Sensory Action**: Trải nghiệm 2 viên nhai vị cacao thơm ngon, trẻ tự giác nhai mỗi tối.
- **Hồi 4 (15.0s – 20.0s) — Outro & CTA**: Khung hình hộp sản phẩm bên thước đo chiều cao, lời kêu gọi nhận lộ trình.

---

### Bước 4: Sinh Prompt Chuyển Động Camera Chuyên Sâu (Motion Prompt Generation)
- **Mục tiêu**: Phối hợp 5 kỹ thuật camera từ `assets/camera-prompts.md` (Key Zoom, Dolly In, Pan Slow, Orbit, Multishot) để tạo chuyển động máy quay mượt mà, không rung lắc.
- **Thực thi lệnh**:
  ```bash
  python scripts/gen-prompt.py --topic "Cơ chế tăng trưởng tự nhiên ban đêm với Alpha-GPC & Canxi Nano" --style luxury --duration 20
  ```
- **Đầu ra**: File `output/video_storyboard_latest.json` và `output/video_storyboard_latest.md` chứa đầy đủ prompt tiếng Anh, lời thoại tiếng Việt và chữ hiển thị trên màn hình.

---

### Bước 5: Kích Hoạt Negative Prompt & Element Pin (Quality Guardrails)
- **Mục tiêu**: Bảo đảm tính toàn vẹn thương hiệu, không méo logo, không sai màu sắc, không dị dạng bàn tay.
- **Quy tắc thực chiến từ `references/troubleshoot.md`**:
  - Luôn nạp toàn bộ nội dung `assets/negative-prompt.txt` vào tham số negative của model.
  - Khi đưa lên Higgsfield / Kling: Bật tính năng **Element Pin** lên vùng nhãn hiệu *Nano Growth*.
  - Giữ Motion Strength ở mức an toàn: `2–3` cho cảnh cận cảnh có chữ, `4–6` cho cảnh chuyển động không gian.

---

### Bước 6: Thực Thi Render & Tổng Hợp Video Tự Động (Multi-Channel Synthesis)
- **Mục tiêu**: Xuất bản video hoàn chỉnh thông qua cơ chế song song (Dual-Pipeline):
  1. **Luồng Cloud Studio**: Tạo file `output/higgsfield_payload.json` và cẩm nang `output/higgsfield_web_instructions.md` hỗ trợ copy-paste 1-click vào Web UI Higgsfield (Stream 4.5).
  2. **Luồng Autonomous Engine**: Tự động dùng FFmpeg và Pillow render ngay 4 phân cảnh, áp dụng chuyển động Ken Burns chuẩn xác, text overlay vùng an toàn TikTok và hòa âm ambient 432Hz $\rightarrow$ file MP4 hoàn thiện.
- **Thực thi lệnh**:
  ```bash
  python scripts/upload-higgsfield.py --render
  ```

---

### Bước 7: Kiểm Định Đầu Ra (QA/QC) & Bàn Giao Duyệt Cuối
- **Checklist kiểm định trước khi bàn giao**:
  - [x] Thời lượng video nằm trong khoảng 15 – 25 giây (chuẩn 20.0s).
  - [x] Khung hình định dạng dọc 9:16 (1080 x 1920 pixels, 30fps).
  - [x] Không có lỗi méo mó chữ hoặc biến dạng bao bì sản phẩm.
  - [x] Phụ đề và tiêu đề nằm trọn trong vùng an toàn (Safe Zone) của TikTok/Reels.
  - [x] Luồng âm thanh stereo mượt mà, kết thúc bằng fade-out êm dịu.
  - [x] File MP4 lưu tại `output/nano_growth_video_sample_20s.mp4`.

---

## 4. Hướng Dẫn Sử Dụng Nhanh Cho Agent (Agent Cheat-Sheet)

Khi người dùng yêu cầu: *"Tạo video AI cho chủ đề [X]"*:
1. `python scripts/list-images.py` $\rightarrow$ Xác nhận ảnh sản phẩm có sẵn.
2. `python scripts/gen-prompt.py --topic "[X]" --style luxury --duration 20` $\rightarrow$ Sinh kịch bản 4 phân cảnh.
3. `python scripts/upload-higgsfield.py --render` $\rightarrow$ Xuất bản video MP4 và gói cấu hình Higgsfield.
4. Trình bày video kèm kịch bản chi tiết để người dùng duyệt cuối.
