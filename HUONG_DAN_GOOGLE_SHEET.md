# Hướng Dẫn Kết Nối Form Đặt Hàng Vào Google Sheets Tự Động (1 Phút)

Tính năng tự động gửi thông tin từ form trên Salepage vào **Google Sheets** đã được tích hợp sẵn trong mã nguồn. Bạn chỉ cần thực hiện 3 bước đơn giản dưới đây để kết nối với Google Sheet của bạn:

---

### BƯỚC 1: Tạo Google Sheet Mới
1. Mở trình duyệt và truy cập: **[https://sheets.new](https://sheets.new)** để tạo một trang tính Google mới.
2. Đổi tên trang tính thành: **`Đơn Hàng - Nano Growth Habit EX`** (hoặc tên tùy ý).
*(Bạn không cần tạo trước các cột tiêu đề, script sẽ tự động tạo đẹp mắt khi có đơn đầu tiên).*

---

### BƯỚC 2: Dán Mã Script Vào Google Sheet
1. Trên thanh menu của Google Sheet, bấm vào **Tiện ích mở rộng** (Extensions) ➔ chọn **Apps Script**.
2. Một trang mới sẽ hiện ra. Bạn hãy **xóa hết toàn bộ code mặc định** trong file `Code.gs`.
3. Mở file **[`google_apps_script.js`](file:///c:/Users/Surface/Documents/2.HNKT%20OFFICIAL/Nano%20Canxi/google_apps_script.js)** trong thư mục dự án, sao chép toàn bộ mã và dán vào ô soạn thảo Apps Script.
4. Bấm tổ hợp phím **Ctrl + S** (hoặc bấm biểu tượng đĩa mềm Lưu).

---

### BƯỚC 3: Triển Khai Web App & Lấy Link Kết Nối
1. Ở góc trên bên phải màn hình Apps Script, bấm nút **Triển khai** (Deploy) màu xanh ➔ chọn **Tùy chọn triển khai mới** (New deployment).
2. Bấm vào biểu tượng bánh răng bên cạnh dòng *Chọn loại*, chọn **Ứng dụng web** (Web app).
3. Điền cấu hình:
   - **Mô tả**: Nhận đơn hàng Salepage
   - **Thực thi dưới dạng** (Execute as): Chọn **Tôi** (Me)
   - **Người có quyền truy cập** (Who has access): Chọn **Bất kỳ ai** (Anyone) *(Bắt buộc chọn Bất kỳ ai để người dùng trên web gửi được đơn mà không cần đăng nhập Google)*.
4. Bấm nút **Triển khai** (Deploy).
5. Nếu Google hiển thị cửa sổ yêu cầu cấp quyền:
   - Bấm **Ủy quyền truy cập** (Authorize access).
   - Chọn tài khoản Google của bạn.
   - Bấm chữ **Nâng cao** (Advanced) ở góc dưới bên trái ➔ bấm **Đi tới dự án (không an toàn)**.
   - Bấm **Cho phép** (Allow).
6. Sau khi xong, bạn sẽ nhận được một đường link **URL ứng dụng web** (có đuôi dạng: `.../exec`). Hãy bấm **Sao chép** (Copy) link đó.

---

### BƯỚC 4: Dán Link Vào File `index.html`
1. Mở file [`index.html`](file:///c:/Users/Surface/Documents/2.HNKT%20OFFICIAL/Nano%20Canxi/index.html).
2. Tìm đến dòng `const GOOGLE_SHEETS_SCRIPT_URL = "";` (gần cuối file, khoảng dòng 2257).
3. Dán đường link URL của bạn vào giữa 2 dấu ngoặc kép:
   ```javascript
   const GOOGLE_SHEETS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby.../exec";
   ```
4. Lưu file lại (`Ctrl + S`).

---

### ✅ KẾT QUẢ:
Mỗi khi có khách hàng điền form trên website và bấm **GỬI THÔNG TIN ĐẶT HÀNG**, dữ liệu sẽ ngay lập tức xuất hiện trong Google Sheet với đầy đủ 10 cột:
1. **Thời Gian Đặt Hàng** (Giờ Việt Nam: `YYYY-MM-DD HH:mm:ss`)
2. **Họ Tên Phụ Huynh**
3. **Số Điện Thoại** (Giữ nguyên số 0 ở đầu)
4. **Tuổi Của Con**
5. **Chiều Cao (cm)**
6. **Cân Nặng (kg)**
7. **Sản Phẩm Đang Dùng**
8. **Địa Chỉ Nhận Hàng**
9. **Gói Sản Phẩm** (Gói 1, Gói 2 hay Gói 3)
10. **Nguồn Đơn Hàng**
