# ⚡ NANO GROWTH HABIT EX — SALEPAGE & PAYMENT SYSTEM

Hệ thống Salepage bán hàng và cổng thanh toán tự động VietQR (Sepay) kết hợp cơ sở dữ liệu Supabase, hệ thống Email tự động Resend và Admin Panel quản trị thời gian thực.

---

## 🏗️ 1. Kiến Trúc Hệ Thống

| Thành phần | Công nghệ / Dịch vụ | Nhiệm vụ |
|---|---|---|
| **Frontend** | HTML5, Tailwind CSS (CDN), Vanilla JS | Salepage chính (`index.html`), popup VietQR động, chatbot |
| **Admin Panel** | Single Page Application (`/admin`) | Quản lý Đơn hàng, Tồn kho Sản phẩm, Danh bạ Khách hàng |
| **Serverless API** | Vercel Node.js Serverless (`/api/*`) | Gửi email xác nhận, chuỗi email marketing, proxy Telegram an toàn |
| **Cơ sở dữ liệu Cloud** | Supabase (PostgreSQL) | Lưu trữ đơn hàng (`orders`), khách hàng (`customers`), sản phẩm (`products`) |
| **Cổng thanh toán** | Sepay (VietQR qua TPBank) | Sinh mã QR động, bắt Webhook giao dịch ngân hàng theo thời gian thực |
| **Email Marketing** | Resend API (`@hnkt.vn`) | Gửi email xác nhận đơn hàng thành công và chuỗi nuôi dưỡng tự động |
| **Thông báo nội bộ** | Telegram Bot | Bắn thông báo đơn mới và thanh toán thành công về nhóm nội bộ |

---

## ⚙️ 2. Cấu Hình Biến Môi Trường (`.env`)

Tạo file `.env` tại thư mục gốc của dự án (sử dụng mẫu từ `.env.example`):

```bash
cp .env.example .env
```

Nội dung cấu hình chi tiết:

```env
# 1. DỊCH VỤ EMAIL RESEND (https://resend.com)
RESEND_API_KEY=re_your_api_key_here
EMAIL_SENDER=Nano Growth EX <cskh@hnkt.vn>

# 2. THÔNG BÁO TELEGRAM (https://t.me/BotFather)
TELEGRAM_BOT_TOKEN=7966144550:AAEUt6ystZCBFMrZUBXS7lJII6RZjZDNTTY
TELEGRAM_CHAT_ID=-1004414191458

# 3. CƠ SỞ DỮ LIỆU SUPABASE (https://supabase.com)
SUPABASE_URL=https://tuvjisjiinjydgqvbzru.supabase.co
SUPABASE_ANON_KEY=sb_publishable_Sfq7rfo4kFRf-N12cP3RSw_5qKf-AVE

# 4. TÀI KHOẢN NGÂN HÀNG VIETQR SEPAY
SEPAY_BANK_NAME=TPBank
SEPAY_ACCOUNT_NO=00005510675
SEPAY_ACCOUNT_NAME=Le Quang Cuong
```

> ⚠️ **Bảo mật:** File `.env` chứa token bí mật và đã được khai báo trong `.gitignore`. Tuyệt đối **không** commit file `.env` lên GitHub hoặc kho lưu trữ công khai.

---

## 🚀 3. Hướng Dẫn Deploy Lên Server Thật

### Cách 1: Triển khai qua Vercel (Khuyến nghị – Miễn phí & Tối ưu nhất)

Dự án đã được cấu hình sẵn cho Vercel (`vercel.json` định tuyến tự động `/admin` và `/api/*`):

1. **Đẩy mã nguồn lên GitHub:**
   ```bash
   git add .
   git commit -m "deploy: cap nhat ma nguon"
   git push origin main
   ```
2. **Import vào Vercel:**
   - Đăng nhập [Vercel](https://vercel.com) ➔ Chọn **Add New Project** ➔ Chọn repository GitHub của bạn.
   - Framework Preset: Chọn **Other**.
   - Root Directory: `./` (mặc định).
3. **Thêm Biến Môi Trường (Environment Variables):**
   - Vào **Settings** ➔ **Environment Variables** trên Vercel.
   - Thêm các biến từ file `.env` (`RESEND_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`).
4. **Cấu hình Tên Miền (Custom Domain `nano.hnkt.vn`):**
   - Vào **Settings** ➔ **Domains** ➔ Thêm tên miền `nano.hnkt.vn`.
   - Vào nhà cung cấp tên miền (Cloudflare / Inet / Mắt Bão) và thêm bản ghi DNS:
     - **Loại:** `CNAME`
     - **Tên (Host):** `nano`
     - **Giá trị (Value):** `cname.vercel-dns.com`

---

### Cách 2: Triển khai trên VPS Linux (Nginx + Node.js)

1. **Cài đặt Node.js & Nginx:**
   ```bash
   sudo apt update
   sudo apt install -y nginx nodejs npm git
   ```
2. **Clone mã nguồn về thư mục web:**
   ```bash
   cd /var/www
   git clone https://github.com/striverai/nano-growth-habit-ex.git nano-canxi
   cd nano-canxi
   npm install
   ```
3. **Cấu hình Nginx Virtual Host (`/etc/nginx/sites-available/nano.hnkt.vn`):**
   ```nginx
   server {
       listen 80;
       server_name nano.hnkt.vn;
       root /var/www/nano-canxi;
       index index.html;

       location / {
           try_files $uri $uri/ /index.html;
       }

       location /admin {
           try_files /admin/index.html =404;
       }

       location /api/ {
           proxy_pass http://127.0.0.1:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
4. **Bật SSL Let's Encrypt:**
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d nano.hnkt.vn
   ```

---

## 💳 4. Cấu Hình Webhook Sepay (Thanh Toán Tự Động)

1. Đăng nhập vào [my.sepay.vn](https://my.sepay.vn).
2. Vào mục **Webhooks** ➔ **Tạo Webhook mới**:
   - **URL Webhook:** `https://tuvjisjiinjydgqvbzru.supabase.co/functions/v1/sepay-webhook`
   - **Sự kiện:** Nhận tiền vào (Chuyển khoản đến).
3. ⚠️ **Lưu ý bắt buộc trong Supabase:**
   - Vào **Supabase Dashboard** ➔ **Edge Functions** ➔ Chọn `sepay-webhook`.
   - Vào tab **Settings** ➔ **Gạt TẮT "Enforce JWT Verification"** (để Sepay có thể gọi vào mà không bị chặn lỗi 401).

---

## 🗄️ 5. Quản Lý & Sao Lưu Dữ Liệu (Backup)

### Sao lưu cơ sở dữ liệu `brain.db`:
Chạy lệnh tự động tạo bản sao lưu có kiểm tra tính toàn vẹn (Integrity Check):
```bash
python backup_db.py
```
File sao lưu sẽ được tạo dưới dạng: `brain_backup_YYYYMMDD_HHMMSS.db`.

### Đồng bộ cơ sở dữ liệu Supabase Cloud:
Nếu cần xem và duyệt đơn hàng trên Cloud, truy cập trực tiếp trang quản trị:
👉 **[https://nano.hnkt.vn/admin](https://nano.hnkt.vn/admin)**

---

## 📞 Hỗ Trợ Kỹ Thuật
- **Kỹ thuật:** striverai
- **Website:** [https://nano.hnkt.vn](https://nano.hnkt.vn)
- **Tài liệu tham khảo:** [Sepay Docs](https://docs.sepay.vn/) | [Supabase Docs](https://supabase.com/docs)
