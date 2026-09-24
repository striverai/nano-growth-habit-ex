# Heartbeat Workflow — goClaw Proactive Pulse

Tài liệu này hướng dẫn chu trình tự động thức dậy (heartbeat loop) của agent goClaw để giám sát business của anh Huy và chủ động gửi tin nhắn Telegram.

---

## 1. Công cụ MCP liên kết (Bound Tool)

Agent sử dụng function đã được cấu hình ở Phần 1:
- **Tên Tool**: `get_business_signals` (hoặc `biz__get_business_signals` tùy tiền tố của goClaw).
- **Tham số đầu vào**:
  - `mark_as_read` (boolean, mặc định: `true`): Tự động đánh dấu các đơn/lead này là `notified = 1` để không bao giờ bị báo trùng lặp trong lần quét tiếp theo.
  - `include_daily_report` (boolean, mặc định: `false`): Nếu là khung giờ báo cáo sáng (khoảng 08:00 – 08:30 sáng), gán `true` để lấy tổng hợp doanh thu và đơn hàng hôm nay.

---

## 2. Quy trình thực thi từng nhịp đập (Execution Steps)

Khi nhịp Heartbeat kích hoạt (định kỳ mỗi 15 phút):

### Bước 1: Kiểm tra thời gian & Gọi MCP Tool
- Xác định giờ hiện tại của hệ thống.
- Nếu hiện tại nằm trong khung giờ **08:00 – 08:30 sáng** và hôm nay chưa gửi báo cáo sáng:
  - Gọi `get_business_signals(mark_as_read=true, include_daily_report=true)`
- Các khung giờ còn lại:
  - Gọi `get_business_signals(mark_as_read=true, include_daily_report=false)`

### Bước 2: Phân tích kết quả trả về
- **Trường hợp `has_signals == false`**:
  - **HÀNH ĐỘNG DUY NHẤT: GIỮ IM LẶNG TUYỆT ĐỐI**.
  - Không gửi tin nhắn, không "ping", không nói "hệ thống không có gì mới".
  - Kết thúc nhịp chạy ngay lập tức.
- **Trường hợp `has_signals == true`**:
  - Tiến hành tổng hợp nội dung và gửi tin nhắn Telegram ngay cho anh Huy theo cấu trúc ở Mục 3.

---

## 3. Định dạng tin nhắn Telegram gửi anh Huy

Tin nhắn phải ngắn gọn, trực diện, đúng phong cách `SOUL.md`:

### Mẫu 1: Khi có Đơn Hàng Mới (`new_orders > 0`)
```text
🔔 CÓ ĐƠN HÀNG MỚI!

• Khách hàng: [Tên khách] - [SĐT tóm tắt]
• Sản phẩm: [Tên SP / Số lượng]
• Tổng tiền: [Số tiền]đ
• Địa chỉ: [Địa chỉ giao hàng ngắn gọn]

👉 Em đã ghi nhận vào brain.db, anh kiểm tra kho để đóng hàng nhé!
```

### Mẫu 2: Khi có Lead Mới Cần Tư Vấn (`new_leads > 0`)
```text
⚡ CÓ LEAD NÓNG VỪA ĐỂ LẠI THÔNG TIN!

• Khách: [Tên phụ huynh / khách] - [SĐT]
• Nhu cầu: [Độ tuổi của bé / ghi chú chiều cao / sản phẩm quan tâm]
• Nguồn: [Landing Page / Form]

👉 Cần gọi trong 15 phút vàng để tỷ lệ chốt cao nhất anh nhé!
```

### Mẫu 3: Báo cáo sáng (`daily_report`)
```text
☀️ BÁO CÁO NHANH ĐẦU NGÀY

• Tổng đơn hôm nay: [Số đơn] đơn
• Doanh thu ghi nhận: [Số tiền]đ
• Lead đang chờ chăm sóc: [Số lượng lead]

Chúc anh ngày mới chốt thêm nhiều đơn Nano Canxi!
```

*(Ghi chú: Nếu một nhịp vừa có đơn vừa có lead, hãy gộp chung vào 1 tin nhắn duy nhất, không bắn tách lẻ nhiều tin)*

---

## 4. Xử lý sự cố (Error Handling)

- Nếu gọi MCP server bị lỗi mạng hoặc timeout: Không spam tin báo lỗi liên tục. Ghi log lại và thử lại ở nhịp tiếp theo (sau 15 phút).
- Chỉ gửi tin Telegram cảnh báo hệ thống khi gặp lỗi gián đoạn liên tiếp từ 3 lần trở lên (hơn 45 phút không kết nối được database).
