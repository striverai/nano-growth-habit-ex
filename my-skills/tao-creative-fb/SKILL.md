---
name: tao-creative-fb
description: Chuyên gia sản xuất FULL CONTENT (đồng thời CẢ ẢNH VÀ VĂN BẢN) cho Facebook Fanpage và Facebook Ads của thương hiệu Nano Growth Habit EX. Tự động hóa trọn gói từ khâu lên ý tưởng, tạo ảnh AI chuẩn phong cách Nhật Bản đến viết caption/copy sắc bén và đăng trực tiếp lên Facebook Page. Sử dụng khi người dùng muốn "tạo content cho ngày mai", "gen bài Page", "content free", "content organic" (Mode 1 - Content Free tự động đăng sau khi duyệt) hoặc khi người dùng yêu cầu "tạo creative ads", "gen ads", "cần creative cho chiến dịch" (Mode 2 - Creative Ads sản xuất 3 bộ ảnh + copy ghép cặp cho Ads Manager). Tuyệt đối không tạo văn bản rời rạc hay chỉ sinh ảnh đơn lẻ — mọi output luôn là một thể thống nhất gồm CẢ ẢNH ĐẸP VÀ BÀI VIẾT HOÀN CHỈNH.
---

# Tao-Creative-FB — Hệ Thống Sản Xuất Full Content Facebook (Ảnh + Văn Bản)

## 1. Tôn Chỉ & Nguyên Tắc Tối Thượng
1. **LUÔN ĐI THEO CẶP (ẢNH + VĂN BẢN)**:
   - Bài đăng Fanpage hoàn chỉnh = **1 Ảnh thiết kế chuẩn 1024x1024** + **1 Caption hoàn chỉnh (80–150 từ)**.
   - Creative Ads hoàn chỉnh = **1 Ảnh Ads (có khoảng trống đặt chữ)** + **1 Ad Copy chuyển đổi cao (80–150 từ)**.
   - Tuyệt đối không bao giờ trả về chỉ ảnh hoặc chỉ bài viết rời rạc.
2. **CHUẨN BRAND VOICE NANO GROWTH HABIT EX**:
   - Tinh thần chuẩn Nhật Bản: Đơn giản, thực tế, minh bạch, giàu năng lượng.
   - Câu ngắn gọn, dứt khoát, chia đoạn 2–3 câu/đoạn.
   - Luôn làm nổi bật định vị: *"Canxi chỉ là gạch vữa, Hormone tăng trưởng (GH) mới là thợ xây"* — Đánh thức chiều cao tự nhiên ban đêm với Alpha-GPC, canxi vỏ trứng kết hợp CPP êm bụng không lo táo bón, 2 viên nhai vị cacao con tự giác nhai mỗi tối.
   - **Tuyệt đối cấm**: Các từ ngữ sáo rỗng (*"synergy", "chuyển đổi số toàn diện", "tối ưu hóa trải nghiệm", "kính chào quý khách"*).

---

## 2. Hai Chế Độ Hoạt Động (Operating Modes)

```
                            [YÊU CẦU CỦA NGƯỜI DÙNG]
                                       |
                   +-------------------+-------------------+
                   |                                       |
        [MODE 1: CONTENT FREE]                  [MODE 2: CREATIVE ADS]
   (Trigger: bài Page, content free...)     (Trigger: gen ads, creative ads...)
                   |                                       |
         [Bước A: 3 Ý Tưởng]                      [Sản Xuất 3 BỘ CREATIVE]
                   |                               (Mỗi bộ = 1 Ảnh + 1 Copy)
         [Bước B: Gen Full Bộ]                             |
       (1 Ảnh Low + 1 Caption)               - Bộ 1: Pain Point (Nỗi đau)
                   |                         - Bộ 2: Solution (Giải pháp)
         [Bước C: Preview Duyệt]             - Bộ 3: Social Proof (Bằng chứng)
                   |                                       |
         [Bước D: Post Lên Page]                  [Đóng Gói Xuất Bản]
        ( /{page-id}/photos )                 (Cho Meta Ads Manager)
```

---

### MODE 1 — CONTENT FREE (Đăng Fanpage Hằng Ngày)

- **Mục tiêu**: Xây dựng nhận diện, củng cố niềm tin, duy trì tương tác tự nhiên với phụ huynh có con trong độ tuổi vàng 6–18 tuổi.
- **Triggers**: `"tạo content cho ngày mai"`, `"gen bài Page"`, `"content free"`, `"content organic"`, `"soạn bài fanpage"`.
- **Quy trình 4 bước chuẩn**:

#### Bước A: Đề xuất 3 Ý Tưởng Nội Dung (Ideation)
Đưa ra 3 góc tiếp cận khác nhau để người dùng lựa chọn:
1. **Ý tưởng 1 (Giáo dục / Bác bỏ ngộ nhận)**: Vạch trần sai lầm khi chỉ nhồi canxi mà quên mất hormone GH ban đêm.
2. **Ý tưởng 2 (Thói quen / Đồng cảm)**: Nỗi khổ ép con uống thuốc viên to thô kệch vs trải nghiệm 2 viên nhai cacao con tự giác.
3. **Ý tưởng 3 (Khoa học chuẩn Nhật)**: Cơ chế hoạt chất Alpha-GPC và CPP giữ canxi hòa tan, không nóng trong táo bón.

*Cấu trúc hiển thị:*
```text
Anh duyệt chọn 1 trong 3 ý tưởng dưới đây để em lên full bài nhé:
1. [Tiêu đề 1] — Góc nhìn: [Tóm tắt 1 câu]
2. [Tiêu đề 2] — Góc nhìn: [Tóm tắt 1 câu]
3. [Tiêu đề 3] — Góc nhìn: [Tóm tắt 1 câu]
```

#### Bước B: Tạo Full Content Cho Ý Tưởng Được Chọn
Sau khi người dùng chọn số 1, 2 hoặc 3:
1. Gọi `scripts/gen_image.py`:
   - Prompt bám sát template `assets/image-prompt-templates.md`.
   - Model: `gpt-image-1`, Size: `1024x1024`, Quality: `low` (tối ưu chi phí cho organic).
2. Gọi `scripts/gen_caption.py`:
   - Độ dài: ~80–150 từ.
   - Cấu trúc: Hook 3 giây đầu $\rightarrow$ Thân bài (2–3 đoạn ngắn) $\rightarrow$ Soft CTA thân thiện (hỏi han kinh nghiệm, nhắn tin tâm sự với Dược sĩ).

#### Bước C: Hiển Thị Preview
Hiển thị đầy đủ cả Ảnh (đường dẫn/preview) và nội dung Caption để người dùng đọc duyệt trực tiếp:
```text
🖼️ ẢNH BÀI ĐĂNG (1024x1024): [Đường dẫn file ảnh]
📝 CAPTION BÀI ĐĂNG:
[Toàn văn nội dung caption]

👉 Anh xem qua nội dung, nếu OK em sẽ đăng trực tiếp lên Facebook Page ngay nhé!
```

#### Bước D: Xuất Bản Lên Facebook Page
Khi người dùng gõ xác nhận ("OK", "Duyệt", "Đăng đi"):
- Gọi `scripts/post_facebook.py` đẩy đồng thời ảnh và caption lên Facebook Page qua endpoint `/{page-id}/photos` (tham số `url` hoặc file + `caption`).
- Nếu `DRY_RUN=true`, script sẽ lưu ảnh và caption vào thư mục `output/` local và xuất log mô phỏng thành công.

---

### MODE 2 — CREATIVE ADS (Sản Xuất Bộ Quảng Cáo Cho Ads Manager)

- **Mục tiêu**: Chuyển đổi trực tiếp, thu hút khách hàng tiềm năng để lại số điện thoại hoặc mua combo bứt phá chiều cao.
- **Triggers**: `"tạo creative ads"`, `"gen ads"`, `"cần creative cho chiến dịch"`, `"bộ quảng cáo mới"`.
- **Nguyên tắc**: KHÔNG tự động đăng lên Page. Sản xuất ngay **3 BỘ CREATIVE GHÉP CẶP ĐI LIỀN NHAU**:
  - **Bộ 1: Angle PAIN POINT (Đánh vào Nỗi đau)**:
    - *Ảnh*: Model `gpt-image-1`, quality `medium`, bố cục chừa khoảng trống 30% cho text overlay (ví dụ: góc đo chiều cao con thấp hơn bạn cùng lứa).
    - *Ad Copy*: Hook cảnh báo con lỡ độ tuổi vàng dậy thì + nỗi ám ảnh táo bón sỏi thận do dùng canxi vô cơ + giải pháp Nano Growth + Hard CTA (Ưu đãi mua 2 tặng 1).
  - **Bộ 2: Angle SOLUTION (Đột phá Giải pháp)**:
    - *Ảnh*: Hình ảnh lọ Nano Growth Habit EX chuẩn Nhật cùng ly sữa/cacao ấm áp, ánh sáng chất lượng cao.
    - *Ad Copy*: Hook "Canxi chỉ là gạch vữa, Hormone GH mới là thợ xây" + luận điểm Alpha-GPC + viên nhai con thích mê + Hard CTA.
  - **Bộ 3: Angle SOCIAL PROOF (Bằng chứng Thuyết phục)**:
    - *Ảnh*: Nụ cười rạng rỡ của mẹ và con bên thước đo chiều cao tăng trưởng vượt bậc, phong cách ảnh chụp đời thực tự nhiên.
    - *Ad Copy*: Trải nghiệm thực tế của phụ huynh kiên trì 2 tháng (chỉ ~20k/ngày) + con ăn ngon ngủ sâu tự nhai mỗi tối + Hard CTA (Tư vấn 1-1 miễn phí cùng Dược sĩ).

---

## 3. Hướng Dẫn Sử Dụng Scripts Kỹ Thuật

Tất cả scripts nằm trong thư mục `scripts/`:

### A. Sinh ảnh AI (`scripts/gen_image.py`)
```bash
python scripts/gen_image.py --prompt "Mô tả ảnh chi tiết" --quality low --output output/post_organic.png
```
- Tham số `--quality`: `low` (cho Mode 1) hoặc `medium` (cho Mode 2).
- Tích hợp cơ chế tự động thử lại (Retry 1 lần) nếu gặp sự cố kết nối API.

### B. Sinh Caption / Ad Copy (`scripts/gen_caption.py`)
```bash
# Cho bài đăng Fanpage Organic
python scripts/gen_caption.py --mode organic --topic "sai_lam_canxi_gh" --output output/caption.txt

# Cho Creative Ads
python scripts/gen_caption.py --mode ads --angle pain_point --output output/ad_copy_1.txt
```

### C. Đăng đồng thời Ảnh và Caption lên Facebook (`scripts/post_facebook.py`)
```bash
python scripts/post_facebook.py --image output/post_organic.png --caption output/caption.txt
```
- Endpoint Graph API: `https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos`
- Truyền đồng thời cả `source` (file ảnh nhị phân) và `caption` (văn bản) trong một multipart request duy nhất.
- Hỗ trợ biến môi trường `DRY_RUN=true`: kiểm tra dữ liệu, không gửi request thực tế lên Meta, xuất log an toàn.

---

## 4. Cấu Hình Biến Môi Trường (`.env`)
Tạo file `.env` tại thư mục gốc của skill hoặc thư mục dự án với cấu hình:
```env
OPENAI_API_KEY=sk-proj-your-openai-api-key
FB_PAGE_ID=your-facebook-page-id
FB_PAGE_TOKEN=your-page-access-token
DRY_RUN=true
```
- Nếu `DRY_RUN=true`: Scripts sẽ chạy thử nghiệm, lưu ảnh và caption vào `output/`, kiểm tra kết nối mà không xuất bản thật lên Facebook.
- Chuyển `DRY_RUN=false` khi sẵn sàng đăng bài tự động trên Facebook Page thực tế.
