/**
 * =========================================================================
 * GOOGLE APPS SCRIPT: TỰ ĐỘNG LƯU ĐƠN VÀO SHEET & BÁO LEAD VÀO TELEGRAM GROUP
 * DỰ ÁN: NANO GROWTH HABIT EX
 * =========================================================================
 */

// =========================================================================
// 1. CẤU HÌNH THÔNG BÁO TELEGRAM (ĐIỀN VÀO ĐÂY)
// =========================================================================
// Hướng dẫn:
// 1. Chat với @BotFather trên Telegram để tạo Bot và lấy BOT_TOKEN
// 2. Thêm Bot vào Group của bạn, phân quyền Admin
// 3. Lấy CHAT_ID của Group (thường bắt đầu bằng dấu trừ, ví dụ: -1001234567890 hoặc -987654321)
var TELEGRAM_BOT_TOKEN = "7966144550:AAEUt6ystZCBFMrZUBXS7lJII6RZjZDNTTY"; // Bot: Huy CEO
var TELEGRAM_CHAT_ID = "-1004414191458";   // Group: Huy 8

// =========================================================================
// 2. XỬ LÝ NHẬN ĐƠN HÀNG TỪ WEBSITE (POST REQUEST)
// =========================================================================
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
    
    // Lưu vào Sheet (thêm ' phía trước để không mất số 0)
    var newRow = [
      timestamp,
      data.parentName || data['name'] || '',
      "'" + cleanPhone,
      data.childAge || data['age'] || '',
      data.childHeight || data['height'] || '',
      data.childWeight || data['weight'] || '',
      data.currentSupplements || data['supplements'] || '',
      data.shippingAddress || data['address'] || '',
      data.packageSelect || data['package'] || '',
      data.source || 'Salepage Nano Growth Habit EX'
    ];
    
    sheet.appendRow(newRow);
    
    var lastRow = sheet.getLastRow();
    sheet.getRange(lastRow, 1).setHorizontalAlignment("center");
    sheet.getRange(lastRow, 3).setHorizontalAlignment("center");
    sheet.getRange(lastRow, 4).setHorizontalAlignment("center");
    sheet.getRange(lastRow, 5).setHorizontalAlignment("center");
    sheet.getRange(lastRow, 6).setHorizontalAlignment("center");
    
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

// =========================================================================
// 3. HÀM GỬI TIN NHẮN ĐẸP MẮT VÀO GROUP TELEGRAM
// =========================================================================
function sendTelegramNotification(data, timestamp, phone) {
  var parentName = data.parentName || data['name'] || 'Khách hàng';
  var childAge = data.childAge || data['age'] || 'Chưa rõ';
  var height = data.childHeight || data['height'] || 'Chưa rõ';
  var weight = data.childWeight || data['weight'] || 'Chưa rõ';
  var supplements = data.currentSupplements || data['supplements'] || 'Không';
  var address = data.shippingAddress || data['address'] || 'Chưa cung cấp';
  var pkg = data.packageSelect || data['package'] || 'Gói chuẩn đột phá (2 hộp)';

  var message = "🔔 <b>CÓ ĐƠN HÀNG MỚI - NANO GROWTH HABIT EX!</b>\n";
  message += "━━━━━━━━━━━━━━━━━━\n";
  message += "👤 <b>Phụ huynh:</b> " + parentName + "\n";
  message += "📞 <b>Số điện thoại:</b> <code>" + phone + "</code>\n";
  message += "👶 <b>Tuổi của con:</b> " + childAge + "\n";
  message += "📏 <b>Chiều cao:</b> " + height + " | ⚖️ <b>Cân nặng:</b> " + weight + "\n";
  message += "💊 <b>SP con đang dùng:</b> " + supplements + "\n";
  message += "📦 <b>Gói lựa chọn:</b> <b>" + pkg + "</b>\n";
  message += "📍 <b>Địa chỉ:</b> " + address + "\n";
  message += "⏰ <b>Thời gian:</b> " + timestamp + "\n";
  message += "━━━━━━━━━━━━━━━━━━\n";
  message += "👉 <i>Dược sĩ chuyên môn hãy liên hệ tư vấn ngay!</i>";

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

  var response = UrlFetchApp.fetch(url, options);
  Logger.log("Telegram response: " + response.getContentText());
}

// =========================================================================
// 4. HÀM THỬ NGHIỆM GỬI TIN NHẮN TELEGRAM TRONG APPS SCRIPT
// =========================================================================
// (Sau khi điền Token & Chat ID, bạn chọn hàm testTelegram và bấm "Chạy / Run" để kiểm tra)
function testTelegram() {
  if (!TELEGRAM_BOT_TOKEN || !TELEGRAM_CHAT_ID) {
    Logger.log("Vui lòng điền TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID trước khi kiểm tra!");
    return;
  }
  var dummyData = {
    parentName: "Nguyễn Thị Mai (Test)",
    childAge: "11 tuổi",
    childHeight: "138 cm",
    childWeight: "32 kg",
    currentSupplements: "Sữa tươi, canxi nước",
    shippingAddress: "123 Cầu Giấy, Hà Nội",
    packageSelect: "Gói Chuẩn Đột Phá (2 hộp)"
  };
  var now = Utilities.formatDate(new Date(), "Asia/Ho_Chi_Minh", "yyyy-MM-dd HH:mm:ss");
  sendTelegramNotification(dummyData, now, "0987654321");
  Logger.log("Đã gửi tin nhắn test thành công vào Group Telegram!");
}

function doGet(e) {
  return ContentService
    .createTextOutput("Google Apps Script & Telegram Notification Endpoint đang hoạt động bình thường!")
    .setMimeType(ContentService.MimeType.TEXT);
}
