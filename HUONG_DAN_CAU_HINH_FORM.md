# HƯỚNG DẪN TÍCH HỢP FORM VÀO GOOGLE SHEETS (KHÔNG CẦN BACKEND)

Website Salepage **Nano Growth Habit EX** hiện đã được tích hợp sẵn 2 chế độ điền form linh hoạt tại **Section 13**:
- **Chế độ 1:** Form chuẩn giao diện Salepage (Đẹp, chuyên nghiệp, hỗ trợ Google Sheets qua Google Apps Script hoặc Formspree.io, đồng thời tự động báo Telegram).
- **Chế độ 2:** Khung nhúng Google Form trực tiếp (Iframe Google Forms – tự động 100% vào Google Sheets, đơn giản nhất).

Dưới đây là hướng dẫn chi tiết từng cách thực hiện:

---

## CÁCH 1: NHÚNG GOOGLE FORM TRỰC TIẾP (ĐƠN GIẢN NHẤT)

Đây là cách không cần đụng đến code hay cấu hình server, Google Form sẽ tự động lưu tất cả dữ liệu vào Google Sheets.

### Bước 1: Tạo Google Form
1. Truy cập: **[https://forms.new](https://forms.new)**
2. Đặt tiêu đề biểu mẫu: **Khảo Sát Tăng Trưởng & Đăng Ký Tư Vấn Nano Growth**
3. Thêm các câu hỏi theo đúng danh sách:
   - **Họ và tên Ba/Mẹ** *(Trả lời ngắn - Bắt buộc)*
   - **Số điện thoại / Zalo** *(Trả lời ngắn - Bắt buộc)*
   - **Câu 1: Bé nhà mình hiện mấy tuổi, là bé trai hay bé gái?** *(Trả lời ngắn - Bắt buộc)*
   - **Câu 2: Điều gì khiến Ba/Mẹ trăn trở nhất về con hiện nay?** *(Trắc nghiệm)*:
     - Con thấp hơn các bạn cùng lứa, sợ con bị lùn
     - Con lười ăn, hấp thu kém, người gầy gò
     - Con hay ốm vặt, sức đề kháng kém
     - Con sắp bước qua "giai đoạn vàng" tăng chiều cao (tiền dậy thì / dậy thì)
   - **Câu 3: Ba/Mẹ mong muốn con cải thiện điều gì nhất trong 3 - 6 tháng tới?** *(Trắc nghiệm)*:
     - Tăng chiều cao rõ rệt (3 - 5 cm)
     - Ăn ngon miệng, tiêu hóa tốt, tăng cân đều
     - Phát triển toàn diện, cơ thể săn chắc, khỏe mạnh
   - **Câu 4: Ba/Mẹ đã từng cho con dùng giải pháp tăng trưởng nào chưa?** *(Trắc nghiệm)*:
     - Chưa từng dùng, đang tìm hiểu giải pháp chuẩn khoa học
     - Đã uống canxi / sữa bột nhưng chưa thấy hiệu quả
     - Muốn được tư vấn lộ trình chuẩn, an toàn, không lo lắng tác dụng phụ
   - **Câu 5: Gói sản phẩm Ba/Mẹ quan tâm nhận ưu đãi:** *(Trắc nghiệm)*:
     - Gói 1: Trải nghiệm (1 hộp - 1.250.000đ)
     - Gói 2: Chuẩn đột phá (2 hộp - 2.350.000đ - Ưa chuộng nhất)
     - Gói 3: Toàn diện (3 hộp - 3.390.000đ - Mua 2 tặng 1)
   - **Địa chỉ nhận hàng** *(Trả lời ngắn - Không bắt buộc)*

### Bước 2: Bật tính năng tự động lưu vào Google Sheets
1. Trong Google Form của bạn, chuyển sang tab **Câu trả lời** (Responses).
2. Bấm vào nút màu xanh lá **Liên kết với Trang tính** (Link to Sheets).
3. Chọn **Tạo bảng tính mới** ➔ Bấm **Tạo** (Create).
4. Từ giờ, mỗi khi có phụ huynh điền form, dữ liệu sẽ **ngay lập tức xuất hiện trong Google Sheet** này.

### Bước 3: Lấy link nhúng (Embed) và dán vào Website
1. Bấm nút **Gửi** (Send) ở góc trên bên phải Google Form.
2. Chọn tab có biểu tượng dấu ngoặc nhọn **`< >`** (Nhúng HTML).
3. Sao chép đường link nằm trong thuộc tính `src="..."` (ví dụ: `https://docs.google.com/forms/d/e/1FAIpQLSc.../viewform?embedded=true`).
4. Mở file `index.html`, tìm dòng có `id="googleFormIframe"` (khoảng dòng 1920) và dán link của bạn vào:
   ```html
   <iframe 
     id="googleFormIframe"
     src="DÁN_LINK_GOOGLE_FORM_VÀO_ĐÂY" 
     width="100%" 
     height="850" ...>
   </iframe>
   ```
5. Lưu file lại. Khách hàng bấm tab **🔗 Nhúng Google Form** là có thể điền form ngay trên website.

---

## CÁCH 2: DÙNG FORMSPREE.IO (GIỮ GIAO DIỆN ĐẸP + TỰ ĐẨY VÀO GOOGLE SHEETS)

Nếu bạn muốn giữ giao diện thiết kế sang trọng, đồng bộ phong cách Nhật Bản của Salepage:

1. Đăng ký tài khoản miễn phí tại **[https://formspree.io](https://formspree.io)**.
2. Bấm **+ New Form**, đặt tên form (ví dụ: `Nano Growth Survey`).
3. Sao chép link **Endpoint URL** mà Formspree cấp cho bạn (dạng: `https://formspree.io/f/mdoqvwab`).
4. Trong Formspree, bấm vào tab **Settings** / **Integrations** ➔ chọn **Google Sheets** ➔ kết nối tài khoản Google của bạn để Formspree tự động đồng bộ mỗi đơn hàng sang 1 file Google Sheet.
5. Mở file `index.html`, tìm dòng `const FORMSPREE_ENDPOINT = "";` (khoảng dòng 2371) và dán link vào:
   ```javascript
   const FORMSPREE_ENDPOINT = "https://formspree.io/f/mdoqvwab";
   ```
6. Lưu file lại là xong!

---

## CÁCH 3: DÙNG GOOGLE APPS SCRIPT (MIỄN PHÍ 100% + BÁO TELEGRAM TỨC THÌ)

Mã nguồn Apps Script đã được viết sẵn đầy đủ trong file [`google_apps_script.js`](file:///c:/Users/Surface/Documents/2.HNKT%20OFFICIAL/Nano%20Canxi/google_apps_script.js):

1. Mở **[https://sheets.new](https://sheets.new)** để tạo 1 Google Sheet mới.
2. Bấm menu **Tiện ích mở rộng** (Extensions) ➔ **Apps Script**.
3. Xóa code mặc định, dán toàn bộ nội dung file `google_apps_script.js` vào.
4. Bấm **Triển khai** (Deploy) ➔ **Tùy chọn triển khai mới** (New deployment).
5. Chọn loại **Ứng dụng web** (Web app):
   - *Execute as:* **Tôi (Me)**
   - *Who has access:* **Bất kỳ ai (Anyone)**
6. Bấm **Triển khai** ➔ Cấp quyền truy cập ➔ Copy đường link Web App (`.../exec`).
7. Mở file `index.html`, dán vào dòng `const GOOGLE_SHEETS_SCRIPT_URL = "...";` (khoảng dòng 2368).

---

### TÓM TẮT:
- **Nếu muốn nhanh nhất trong 1 phút:** Dùng **Cách 1 (Google Forms Embed)**.
- **Nếu muốn giao diện Salepage đẹp nhất:** Dùng **Cách 2 (Formspree)** hoặc **Cách 3 (Google Apps Script)**.
