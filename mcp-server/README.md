# Hướng Dẫn Triển Khai MCP Server (Streamable-HTTP)

MCP Server dành cho dự án **Nano Growth Habit EX**, kết nối với hệ thống **goClaw AI Gateway** qua giao thức `streamable-http`.

---

## 1. Cấu hình Cổng & Endpoint
- **Giao thức:** `streamable-http`
- **Địa chỉ:** `http://127.0.0.1:3001/mcp`
- **Health check:** `http://127.0.0.1:3001/health`
- **Bảo mật:** Chỉ lắng nghe trên `127.0.0.1` (localhost only), không mở ra internet công khai.

---

## 2. Danh sách Tools hỗ trợ
1. `update_hero`: Đổi tiêu đề landing page `index.html` trong 3 giây.
2. `get_business_stats`: Báo cáo tổng quan doanh thu, số đơn thành công, tổng đơn, khách hàng.
3. `search_customer`: Tra cứu thông tin khách hàng theo SĐT / Email.
4. `list_orders`: Xem danh sách đơn hàng gần đây.
5. `update_order_status`: Duyệt đơn hoặc cập nhật trạng thái đơn hàng.

---

## 3. Khởi chạy bằng PM2 trên VPS

```bash
# Cài đặt thư viện
cd /var/www/hnkt/nano-canxi/mcp-server
npm install --omit=dev

# Khởi chạy bằng PM2
MCP_PORT=3001 pm2 start index.js --name nano-mcp-server
pm2 save
```

---

## 4. File mẫu Systemd Service (nếu không dùng PM2)

Lưu tại `/etc/systemd/system/mcp-server.service`:

```ini
[Unit]
Description=Nano Canxi MCP Streamable-HTTP Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/hnkt/nano-canxi/mcp-server
ExecStart=/usr/local/bin/node index.js
Restart=always
RestartSec=5
Environment=NODE_ENV=production
Environment=MCP_PORT=3001
Environment=MCP_HOST=127.0.0.1

[Install]
WantedBy=multi-user.target
```

---

## 5. Kết nối vào goClaw Dashboard (`https://agent.hnkt.vn`)
1. Vào **Capabilities** -> **MCP Servers** -> Bấm **Add MCP Server**.
2. Điền:
   - **Name:** `my-business`
   - **Transport:** `streamable-http`
   - **URL:** `http://127.0.0.1:3001/mcp`
   - **Tool prefix:** `biz`
   - **Enabled:** Bật ✅
3. Bấm **Save** để kết nối.
