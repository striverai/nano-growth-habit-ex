# BÁO CÁO NGHIỆM THU HOÀN THÀNH SOP NGÀY 14
**Dự án:** Nano Growth Habit EX (HNKT)  
**Mục tiêu:** (1) Di chuyển website lên VPS thật & (2) Xây dựng MCP Server / AI Agent có tay chân.

---

## 1. PHẦN 1: MIGRATION TỪ VERCEL LÊN VPS CONTABO

- **Địa chỉ IP VPS:** `194.233.82.227` (Ubuntu 24.04 LTS, Node.js v22)
- **Thư mục dự án:** `/var/www/hnkt/nano-canxi`
- **Quản lý tiến trình (PM2):** Tiến trình `nano-canxi` chạy trên cổng nội bộ `3005`, tự động khởi động cùng hệ thống (`pm2 startup`).
- **Web Server Caddy & SSL:** Đã cấu hình Reverse Proxy và cấp phát chứng chỉ SSL Let's Encrypt tự động.
- **Tên miền hoạt động:**
  - Trang bán hàng chính: [https://nano.hnkt.vn](https://nano.hnkt.vn) (HTTP/2 200 OK)
  - Trang quản trị Admin: [https://nano.hnkt.vn/admin](https://nano.hnkt.vn/admin)
  - Endpoint kiểm tra sức khỏe: [https://nano.hnkt.vn/health](https://nano.hnkt.vn/health)

---

## 2. PHẦN 2: BUILD MCP SERVER & AI AGENT CÓ TAY CHÂN

### 2.1. Model Context Protocol (MCP Server)
- **Mã nguồn:** Thư mục `/var/www/hnkt/nano-canxi/mcp-server`
- **SDK:** `@modelcontextprotocol/sdk` chuẩn quốc tế, chạy qua transport `stdio`.
- **Trang bị 8 công cụ (Tools):**
  1. `get_business_stats`: Báo cáo tổng quan doanh thu, đơn hàng, khách hàng.
  2. `list_orders`: Xem danh sách đơn hàng theo trạng thái (`pending`, `success`...).
  3. `update_order_status`: Duyệt đơn hoặc cập nhật trạng thái đơn hàng.
  4. `search_customer`: Tra cứu thông tin và lịch sử mua sắm theo SĐT/Email.
  5. `list_products`: Xem bảng giá và tồn kho sản phẩm.
  6. `get_knowledge_base`: Đọc tri thức USP sản phẩm, Brand Voice từ `brain.db`.
  7. `send_telegram_alert`: Gửi tin nhắn tức thì vào nhóm quản trị.
  8. `send_customer_email`: Gửi email chăm sóc khách qua Resend API.

### 2.2. Kết nối Odoo ERP & Website Chính thức
- **Trang web chính thức:** `https://hnkt.vn/nano-growth-habit-ex`
- **Cơ sở dữ liệu:** PostgreSQL (`luxpeto_prod`) cổng `5432` trên VPS.
- **Dữ liệu quản trị:** Đồng bộ 100% với các bảng `crm_lead` và `hnkt_nano_submission`.

### 2.3. Telegram Bot AI Agent (@hnktceoai_bot)
- **Tên Bot:** `HNKT CEO AI` ([t.me/hnktceoai_bot](https://t.me/hnktceoai_bot))
- **Tiến trình chạy ngầm:** `hnkt-ai-bot` (quản lý bởi PM2 trên VPS).
- **Tính năng nổi bật:**
  1. **Báo động Lead mới tức thì (Realtime Alert):** Mỗi khi khách gửi form trên web, bot tự động bắn thông tin chi tiết (Tên, SĐT, Tuổi con, Gói chọn, Tạm tính) về Telegram cá nhân của anh trong vòng 5 giây.
  2. **Trí tuệ nhân tạo đàm thoại (Google Gemini AI):** Tích hợp Gemini AI với cơ chế dự phòng đa tầng (`gemini-flash-lite-latest`, `gemini-3-flash-preview`, `gemini-flash-latest`), tự động hiểu dữ liệu Odoo thời gian thực để trả lời tự nhiên mọi câu hỏi của anh.
  3. **Lệnh quản trị nhanh:**
     - `/stats` hoặc nhắn `báo cáo`: Xem tổng số khách và doanh thu tạm tính.
     - `/leads` hoặc nhắn `khách mới`: Xem danh sách khách hàng mới nhất.
     - `/find <sđt>`: Tra cứu nhanh phụ huynh theo số điện thoại.

---

## 3. CÁC LỆNH QUẢN TRỊ KHI CẦN KIỂM TRA VPS

```bash
# Kiểm tra trạng thái các dịch vụ đang chạy
pm2 status

# Xem nhật ký hoạt động của Telegram Bot
pm2 logs hnkt-ai-bot

# Xem nhật ký hoạt động của Website
pm2 logs nano-canxi

# Khởi động lại toàn bộ dịch vụ
pm2 restart all
```
