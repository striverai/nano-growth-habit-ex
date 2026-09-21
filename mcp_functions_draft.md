# Danh Sách MCP Functions Cho goClaw AI Agent (Ngày 14)

Dựa trên toàn bộ hệ thống bán hàng và landing page của **Nano Growth Habit EX**, đây là 3 MCP functions quan trọng nhất được lựa chọn để điều khiển trực tiếp qua Telegram:

---

### 1. `biz__update_hero` (Độ ưu tiên: 1 - Tuyệt đối)
- **Mục đích:** Đổi ngay tiêu đề chính (Hero Headline) của landing page `index.html` trong 3 giây khi có chương trình khuyến mãi bất ngờ hoặc flash sale.
- **Input params:** 
  - `new_title` (string): Nội dung tiêu đề mới cần hiển thị trên website.
- **Output:** Thông báo thành công và đường dẫn website đã cập nhật.
- **Tình huống dùng:** Đang ngồi cà phê, nảy ra ý tưởng flash sale cuối tuần, nhắn 1 câu qua Telegram để sửa web ngay tức thì mà không cần mở laptop.
- **Ví dụ câu nhắn Telegram:**
  > *"Đổi tiêu đề landing thành 'Flash sale cuối tuần 30% — Tặng ngay cẩm nang chiều cao Nhật Bản!'"*

---

### 2. `biz__today_orders` / `biz__get_business_stats` (Độ ưu tiên: 2)
- **Mục đích:** Báo cáo nhanh tổng doanh thu thực tế, số đơn thành công, số đơn đang chờ xử lý, số lượng khách hàng từ cơ sở dữ liệu.
- **Input params:** Không cần tham số.
- **Output:** Báo cáo chi tiết dạng bảng tóm tắt doanh số.
- **Tình huống dùng:** Đầu ngày hoặc cuối ngày, nhắn tin hỏi trợ lý AI xem hôm nay bán được bao nhiêu rồi.
- **Ví dụ câu nhắn Telegram:**
  > *"Báo cáo doanh thu và tình hình đơn hàng hôm nay cho anh."*

---

### 3. `biz__search_customer` (Độ ưu tiên: 3)
- **Mục đích:** Tra cứu nhanh thông tin khách hàng và lịch sử đơn hàng theo số điện thoại hoặc họ tên.
- **Input params:**
  - `query` (string): Số điện thoại hoặc họ tên của khách hàng.
- **Output:** Họ tên, số điện thoại, email, địa chỉ và toàn bộ lịch sử đơn hàng.
- **Tình huống dùng:** Đang đi ngoài đường, khách nhắn tin Zalo hỏi đơn hàng, chỉ cần copy SĐT gửi vào bot Telegram là AI tra cứu ngay toàn bộ lịch sử.
- **Ví dụ câu nhắn Telegram:**
  > *"Kiểm tra giúp anh khách hàng có số điện thoại 0988123456 đã đặt đơn nào chưa."*
