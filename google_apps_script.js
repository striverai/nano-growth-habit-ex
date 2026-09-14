"""
=========================================================================
GOOGLE APPS SCRIPT: TỰ ĐỘNG LƯU KHẢO SÁT & ĐƠN HÀNG VÀO GOOGLE SHEETS
DỰ ÁN: NANO GROWTH HABIT EX
=========================================================================
"""

var TELEGRAM_BOT_TOKEN = "7966144550:AAEUt6ystZCBFMrZUBXS7lJII6RZjZDNTTY"; // Bot: Huy CEO
var TELEGRAM_CHAT_ID = "-1004414191458";   // Group: Huy 8

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(10000);
  
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Tự động tạo hàng Tiêu đề cột nếu trang tính còn mới
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        "Thời Gian",
        "Họ Tên Ba/Mẹ",
        "Số Điện Thoại / Zalo",
        "Tuổi & Giới Tính Bé",
        "Trăn Trở Lớn Nhất",
        "Mục Tiêu 3-6 Tháng",
        "Đã Dùng Giải Pháp Gì",
        "Gói Quan Tâm",
        "Địa Chỉ Nhận Hàng",
        "Nguồn Đơn Hàng"
      ]);
      
      var headerRange = sheet.getRange(1, 1, 1, 10);
      headerRange.setFontWeight("bold");
      headerRange.setBackground("#FFF2CC");
      headerRange.setFontColor("#381A05");
      headerRange.setHorizontalAlignment("center");
      sheet.setFrozenRows(1);
    }
    
    // Đọc dữ liệu gửi từ form website
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
    var phone = (data.phoneNumber || data['phone'] || '').toString();
    var cleanPhone = phone.replace(/['"]+/g, '');
    
    // Lưu vào Sheet (thêm ' phía trước để không mất số 0 đầu)
    var newRow = [
      timestamp,
      data.parentName || data['name'] || '',
      "'" + cleanPhone,
      data.childAgeGender || data.childAge || data['age'] || '',
      data.growthWorry || data['worry'] || '',
      data.growthGoal || data['goal'] || '',
      data.previousSupplements || data.currentSupplements || data['supplements'] || '',
      data.packageSelect || data['package'] || 'Gói Chuẩn Đột Phá (2 hộp)',
      data.shippingAddress || data['address'] || '',
      data.source || 'Salepage Nano Growth Habit EX'
    ];
    
    sheet.appendRow(newRow);
    
    var lastRow = sheet.getLastRow();
    sheet.getRange(lastRow, 1).setHorizontalAlignment("center");
    sheet.getRange(lastRow, 3).setHorizontalAlignment("center");
    sheet.getRange(lastRow, 4).setHorizontalAlignment("center");
    
    // GỬI THÔNG BÁO TỨC THÌ ĐẾN TELEGRAM GROUP
    if (TELEGRAM_BOT_TOKEN && TELEGRAM_CHAT_ID) {
      try {
        sendTelegramNotification(data, timestamp, cleanPhone);
      } catch (teleError) {
        Logger.log("Lỗi gửi Telegram: " + teleError.toString());
      }
    }
    
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

function sendTelegramNotification(data, timestamp, phone) {
  var parentName = data.parentName || data['name'] || 'Khách hàng';
  var childInfo = data.childAgeGender || data.childAge || 'Chưa rõ';
  var worry = data.growthWorry || 'Chưa rõ';
  var goal = data.growthGoal || 'Chưa rõ';
  var supplements = data.previousSupplements || data.currentSupplements || 'Không';
  var pkg = data.packageSelect || 'Gói chuẩn đột phá (2 hộp)';
  var address = data.shippingAddress || data['address'] || 'Chưa cung cấp';

  var message = "🔔 <b>CÓ KHẢO SÁT & ĐĂNG KÝ TƯ VẤN MỚI - NANO GROWTH!</b>\n";
  message += "━━━━━━━━━━━━━━━━━━\n";
  message += "👤 <b>Phụ huynh:</b> " + parentName + "\n";
  message += "📞 <b>Số điện thoại / Zalo:</b> <code>" + phone + "</code>\n";
  message += "👶 <b>Tuổi & Giới tính bé:</b> " + childInfo + "\n";
  message += "⚠️ <b>Trăn trở nhất:</b> " + worry + "\n";
  message += "🎯 <b>Mục tiêu 3-6 tháng:</b> " + goal + "\n";
  message += "💊 <b>Đã dùng giải pháp:</b> " + supplements + "\n";
  message += "📦 <b>Gói lựa chọn:</b> <b>" + pkg + "</b>\n";
  message += "📍 <b>Địa chỉ:</b> " + address + "\n";
  message += "⏰ <b>Thời gian:</b> " + timestamp + "\n";
  message += "━━━━━━━━━━━━━━━━━━\n";
  message += "👉 <i>Dược sĩ chuyên môn hãy liên hệ tư vấn lộ trình ngay!</i>";

  var url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage";
  var payload = {
    chat_id: TELEGRAM_CHAT_ID,
    text: message,
    parse_mode: "HTML"
  };

  var options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  UrlFetchApp.fetch(url, options);
}

function doGet(e) {
  return ContentService
    .createTextOutput("Google Apps Script Endpoint cho Salepage Nano Growth đang chạy tốt!")
    .setMimeType(ContentService.MimeType.TEXT);
}
