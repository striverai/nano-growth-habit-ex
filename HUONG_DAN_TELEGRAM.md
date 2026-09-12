# Hướng Dẫn Cài Đặt Báo Lead Vào Group Telegram (2 Phút)

Tính năng thông báo đơn hàng trực tiếp vào **Group Telegram** giúp đội ngũ kinh doanh / dược sĩ nhận lead ngay lập tức trên điện thoại mỗi khi có phụ huynh đặt hàng.

---

### BƯỚC 1: Tạo Bot Telegram (Mất 30 giây)
1. Mở ứng dụng Telegram trên điện thoại hoặc máy tính.
2. Tìm kiếm người dùng: **`@BotFather`** (có dấu tích xanh chính chủ).
3. Bấm **Start** (Bắt đầu) hoặc gửi tin nhắn `/start`.
4. Gửi lệnh: `/newbot`.
5. Đặt tên hiển thị cho Bot (ví dụ: `Nano Growth Habit Lead Bot`).
6. Đặt username cho Bot (phải kết thúc bằng chữ `bot`, ví dụ: `nanogrowth_lead_bot`).
7. `@BotFather` sẽ gửi lại cho bạn một chuỗi **HTTP API token** (dạng: `7123456789:AAHk1234abcd5678efgh...`). 
👉 **Hãy copy mã Token này lại** (đây là `TELEGRAM_BOT_TOKEN`).

---

### BƯỚC 2: Thêm Bot Vào Group Telegram & Lấy Chat ID
1. Tạo một Group Telegram mới (ví dụ: `[HOT] Lead Nano Growth Habit EX`) hoặc dùng Group có sẵn.
2. Thêm con Bot bạn vừa tạo ở Bước 1 vào Group đó.
3. Cấp quyền **Admin (Quản trị viên)** cho Bot trong Group.
4. Gửi một tin nhắn bất kỳ vào Group (ví dụ: `hello bot`).
5. **Cách lấy CHAT_ID của Group (chọn 1 trong 2 cách)**:
   - **Cách A**: Thêm con bot `@userinfobot` hoặc `@RawDataBot` vào nhóm, nó sẽ báo ngay `Chat ID` (thường bắt đầu bằng dấu trừ `-`, ví dụ: `-1002345678901` hoặc `-987654321`). Xong thì xóa bot đó ra khỏi nhóm.
   - **Cách B**: Mở trình duyệt và truy cập đường link sau (thay TOKEN của bạn vào):
     ```text
     https://api.telegram.org/bot<TOKEN_CỦA_BẠN>/getUpdates
     ```
     Tìm đoạn `"chat":{"id": -100xxxxxxxxxx` ➔ Đó chính là `CHAT_ID`.

---

### BƯỚC 3: Kích Hoạt Báo Lead (Chọn Cách 1 hoặc Cách 2)

#### 🌟 Cách 1: Tích hợp bảo mật qua Google Apps Script (Khuyên Dùng)
- Mở file Google Sheet ➔ vào **Tiện ích mở rộng** (Extensions) ➔ **Apps Script**.
- Mở file **[`google_apps_script.js`](file:///c:/Users/Surface/Documents/2.HNKT%20OFFICIAL/Nano%20Canxi/google_apps_script.js)**, điền Token và Chat ID vào dòng 14-15:
  ```javascript
  var TELEGRAM_BOT_TOKEN = "7123456789:AAHk..."; // Token từ @BotFather
  var TELEGRAM_CHAT_ID = "-1002345678901";       // Chat ID của Group
  ```
- Nhấn **Lưu** (Ctrl + S) ➔ bấm **Triển khai** ➔ **Quản lý phiên triển khai** ➔ bấm bút chì Chỉnh sửa ➔ chọn **Phiên bản: Mới** ➔ bấm **Triển khai**.
*(Cách này giữ bảo mật 100% token của bạn, vừa lưu vào Google Sheet vừa ping về Telegram).*

#### ⚡ Cách 2: Cấu hình trực tiếp trên Salepage (Nhanh nhất)
- Mở file [`index.html`](file:///c:/Users/Surface/Documents/2.HNKT%20OFFICIAL/Nano%20Canxi/index.html) tại dòng 2261:
  ```javascript
  const TELEGRAM_BOT_TOKEN = "7123456789:AAHk..."; // Token của bạn
  const TELEGRAM_CHAT_ID = "-1002345678901";       // Chat ID Group
  ```
- Lưu file và đẩy lên web là xong!

---

### 📲 MẪU TIN NHẮN TỰ ĐỘNG BẮN VỀ GROUP:
```text
🔔 CÓ ĐƠN HÀNG MỚI - NANO GROWTH HABIT EX!
━━━━━━━━━━━━━━━━━━
👤 Phụ huynh: Chị Minh Trang
📞 Số điện thoại: 0987654321
👶 Tuổi của con: 13 tuổi
📏 Chiều cao: 145 cm | ⚖️ Cân nặng: 38 kg
💊 SP con đang dùng: Sữa chua, Canxi nước
📦 Gói lựa chọn: Gói Chuẩn Đột Phá (2 hộp)
📍 Địa chỉ: Cầu Giấy, Hà Nội
⏰ Thời gian: 2026-09-12 10:30:15
━━━━━━━━━━━━━━━━━━
👉 Dược sĩ chuyên môn hãy liên hệ tư vấn ngay!
```
