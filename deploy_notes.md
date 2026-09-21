# 📋 HƯỚNG DẪN TRIỂN KHAI PRODUCTION (DEPLOY NOTES)

Tài liệu hướng dẫn triển khai hệ thống **Nano Growth Habit EX** lên máy chủ VPS Ubuntu.

---

## 1. Danh Sách Biến Môi Trường Cần Có Trên VPS (`.env`)

Tạo file `/var/www/hnkt/nano-canxi/.env` với nội dung sau:

```env
# 1. CỔNG MÁY CHỦ LẮNG NGHE (Mặc định: 3005 trên VPS để tránh trùng các dịch vụ khác)
PORT=3005

# 2. DỊCH VỤ EMAIL RESEND
RESEND_API_KEY=your_resend_api_key_here
EMAIL_SENDER=Nano Growth EX <cskh@hnkt.vn>

# 3. THÔNG BÁO NỘI BỘ TELEGRAM
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=-1004414191458

# 4. SUPABASE CLOUD DATABASE
SUPABASE_URL=https://tuvjisjiinjydgqvbzru.supabase.co
SUPABASE_ANON_KEY=sb_publishable_Sfq7rfo4kFRf-N12cP3RSw_5qKf-AVE

# 5. TÀI KHOẢN NGÂN HÀNG VIETQR (SEPAY)
SEPAY_BANK_NAME=TPBank
SEPAY_ACCOUNT_NO=00005510675
SEPAY_ACCOUNT_NAME=Le Quang Cuong
```

---

## 2. Cổng Lắng Nghe (Listening Port)

* **Cổng mặc định cục bộ:** `3000`
* **Cổng đề xuất chạy trên VPS:** `3005` (hoặc cổng bất kỳ được truyền qua `PORT=3005`)
* Server đọc trực tiếp từ: `process.env.PORT || 3000`

---

## 3. Lệnh Cài Đặt & Khởi Chạy Server Trên VPS

### Bước 1: Di chuyển vào thư mục dự án
```bash
cd /var/www/hnkt/nano-canxi
```

### Bước 2: Cài đặt thư viện phụ thuộc
```bash
npm install --production
```

### Bước 3: Chạy ứng dụng

#### Cách A: Chạy trực tiếp (để kiểm tra nhanh)
```bash
node server.js
```

#### Cách B: Chạy ngầm vĩnh viễn bằng PM2 (Khuyến nghị cho Production)
```bash
# Cài đặt PM2 toàn cục nếu chưa có
npm install -g pm2

# Khởi chạy ứng dụng
pm2 start server.js --name "nano-canxi"

# Cấu hình PM2 tự khởi động cùng hệ thống khi reboot VPS
pm2 save
pm2 startup
```

Các lệnh quản lý PM2 thường dùng:
* Xem trạng thái: `pm2 status`
* Xem log: `pm2 logs nano-canxi`
* Khởi động lại: `pm2 restart nano-canxi`
* Dừng: `pm2 stop nano-canxi`

---

## 4. Cấu Hình Caddy Web Server (Đã có sẵn trên VPS)

Thêm đoạn cấu hình sau vào file `/etc/caddy/Caddyfile`:

```caddyfile
nano.hnkt.vn {
    encode zstd gzip

    # Chuyển tiếp các API sang backend Node.js (cổng 3005)
    handle /api/* {
        reverse_proxy 127.0.0.1:3005
    }

    handle /health {
        reverse_proxy 127.0.0.1:3005
    }

    # Trang quản trị Admin
    handle /admin* {
        root * /var/www/hnkt/nano-canxi
        try_files {path} /admin/index.html =404
        file_server
    }

    # Salepage chính và tệp tĩnh
    handle {
        root * /var/www/hnkt/nano-canxi
        try_files {path} /index.html =404
        file_server
    }
}
```

Sau đó tải lại cấu hình Caddy:
```bash
caddy reload --config /etc/caddy/Caddyfile
```

---

## 5. Kiểm Tra Hoạt Động (Health Check)
* Kiểm tra API: `curl http://127.0.0.1:3005/health`
* Kiểm tra thống kê cơ sở dữ liệu: `curl http://127.0.0.1:3005/api/db/stats`
* Truy cập web chính thức: `https://nano.hnkt.vn`
