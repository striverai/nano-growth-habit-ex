/**
 * =========================================================================
 * GOOGLE APPS SCRIPT: TỰ ĐỘNG LƯU ĐƠN HÀNG TỪ SALEPAGE NANO GROWTH HABIT EX
 * =========================================================================
 * 
 * Hướng dẫn 3 bước cài đặt (chỉ mất 1 phút):
 * 
 * BƯỚC 1: Tạo Google Sheet
 * - Mở https://sheets.new để tạo một trang tính mới.
 * - Đặt tên file: "Đơn Hàng - Nano Growth Habit EX".
 * 
 * BƯỚC 2: Dán mã Script này
 * - Trên menu của Google Sheet, chọn: "Tiện ích mở rộng" (Extensions) -> "Apps Script".
 * - Xóa toàn bộ mã mặc định có sẵn trong file Code.gs.
 * - Dán toàn bộ nội dung của file này vào và nhấn biểu tượng "Lưu" (Ctrl + S).
 * 
 * BƯỚC 3: Triển khai Web App (Deploy)
 * - Nhấn nút "Triển khai" (Deploy) màu xanh ở góc trên bên phải -> chọn "Tùy chọn triển khai mới" (New deployment).
 * - Tại mục bánh răng "Chọn loại", chọn "Ứng dụng web" (Web app).
 * - Cấu hình 3 mục:
 *     + Mô tả: "Nhận đơn hàng Nano Canxi"
 *     + Thực thi dưới dạng (Execute as): "Tôi" (Me - email của bạn)
 *     + Người có quyền truy cập (Who has access): "Bất kỳ ai" (Anyone) <-- BẮT BUỘC để website có thể gửi dữ liệu
 * - Nhấn "Triển khai" (Deploy).
 * - Cấp quyền truy cập nếu Google hỏi (Chọn email của bạn -> Nâng cao / Advanced -> Đi tới dự án / Go to project).
 * - Sao chép đường link "URL ứng dụng web" (có đuôi /exec).
 * - Dán link đó vào dòng `const GOOGLE_SHEETS_SCRIPT_URL = "..."` trong file `index.html`!
 */

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(10000);
  
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Tự động tạo hàng Tiêu đề cột nếu trang tính còn mới
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        "Thời Gian Đặt Hàng",
        "Họ Tên Phụ Huynh",
        "Số Điện Thoại",
        "Tuổi Của Con",
        "Chiều Cao (cm)",
        "Cân Nặng (kg)",
        "Sản Phẩm Đang Dùng",
        "Địa Chỉ Nhận Hàng",
        "Gói Sản Phẩm",
        "Nguồn Đơn Hàng"
      ]);
      
      // Định dạng dòng tiêu đề: In đậm, nền vàng kem ấm, chữ nâu cacao, căn giữa
      var headerRange = sheet.getRange(1, 1, 1, 10);
      headerRange.setFontWeight("bold");
      headerRange.setBackground("#FFF2CC");
      headerRange.setFontColor("#381A05");
      headerRange.setHorizontalAlignment("center");
      sheet.setFrozenRows(1);
    }
    
    // Đọc dữ liệu gửi từ website
    var data = e.parameter || {};
    if (e.postData && e.postData.contents) {
      try {
        var jsonData = JSON.parse(e.postData.contents);
        for (var key in jsonData) {
          data[key] = jsonData[key];
        }
      } catch (err) {}
    }
    
    var timestamp = Utilities.formatDate(new Date(), "Asia/Ho_Chi_Minh", "yyyy-MM-dd HH:mm:ss");
    var phone = data.phoneNumber || data['phone'] || '';
    // Thêm ký tự ' trước số điện thoại để giữ số 0 ở đầu
    if (phone && !phone.toString().startsWith("'")) {
      phone = "'" + phone;
    }
    
    var newRow = [
      timestamp,
      data.parentName || data['name'] || '',
      phone,
      data.childAge || data['age'] || '',
      data.childHeight || data['height'] || '',
      data.childWeight || data['weight'] || '',
      data.currentSupplements || data['supplements'] || '',
      data.shippingAddress || data['address'] || '',
      data.packageSelect || data['package'] || '',
      data.source || 'Salepage Nano Growth Habit EX'
    ];
    
    sheet.appendRow(newRow);
    
    // Căn giữa các cột ngày tháng, số điện thoại, tuổi, chiều cao, cân nặng
    var lastRow = sheet.getLastRow();
    sheet.getRange(lastRow, 1).setHorizontalAlignment("center");
    sheet.getRange(lastRow, 3).setHorizontalAlignment("center");
    sheet.getRange(lastRow, 4).setHorizontalAlignment("center");
    sheet.getRange(lastRow, 5).setHorizontalAlignment("center");
    sheet.getRange(lastRow, 6).setHorizontalAlignment("center");
    
    return ContentService
      .createTextOutput(JSON.stringify({ "status": "success", "row": lastRow }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ "status": "error", "message": err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput("Google Apps Script Endpoint cho Nano Growth Habit EX đang hoạt động bình thường!")
    .setMimeType(ContentService.MimeType.TEXT);
}
