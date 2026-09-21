const https = require('https');

const SENDER = process.env.EMAIL_SENDER || 'Nano Growth EX <cskh@hnkt.vn>';
const RESEND_API_KEY = process.env.RESEND_API_KEY;

function sendEmail(to, subject, html) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      from: SENDER,
      to: Array.isArray(to) ? to : [to],
      subject: subject,
      html: html
    });

    const options = {
      hostname: 'api.resend.com',
      port: 443,
      path: '/emails',
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + RESEND_API_KEY,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        'User-Agent': 'ResendClient/1.0'
      }
    };

    const req = https.request(options, (resp) => {
      let data = '';
      resp.on('data', chunk => data += chunk);
      resp.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve({ status: resp.statusCode, data: parsed });
        } catch(e) {
          resolve({ status: resp.statusCode, raw: data });
        }
      });
    });

    req.on('error', err => reject(err));
    req.write(payload);
    req.end();
  });
}

function buildOrderEmailHtml({ customer_name, product_name, quantity, amount, payment_code, customer_address, status }) {
  const formattedAmount = (amount || 0).toLocaleString('vi-VN') + 'đ';
  const isPaid = status === 'success';
  const statusBadge = isPaid 
    ? '<span style="display: inline-block; padding: 4px 12px; border-radius: 999px; background-color: #dcfce7; color: #15803d; font-weight: bold; font-size: 12px;">✓ ĐÃ THANH TOÁN</span>'
    : '<span style="display: inline-block; padding: 4px 12px; border-radius: 999px; background-color: #fef3c7; color: #b45309; font-weight: bold; font-size: 12px;">⏳ CHỜ THANH TOÁN (COD / CHUYỂN KHOẢN)</span>';

  return `
  <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1e293b; line-height: 1.6; border: 1px solid #e2e8f0; border-radius: 16px; background-color: #ffffff;">
    <div style="text-align: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 2px solid #fef3c7;">
      <h1 style="color: #b45309; margin: 0; font-size: 22px;">⚡ NANO GROWTH HABIT EX</h1>
      <p style="color: #64748b; font-size: 13px; margin-top: 4px;">Xác Nhận Đơn Hàng Thành Công</p>
    </div>

    <p>Chào <strong>Ba/Mẹ ${customer_name || 'Quý khách'}</strong>,</p>

    <p>Cảm ơn Ba/Mẹ đã tin tưởng đặt mua giải pháp tăng chiều cao chuẩn Nhật <strong>Nano Growth Habit EX</strong> cho con!</p>

    <p>Đơn hàng của Ba/Mẹ đã được hệ thống ghi nhận thành công và đang được bộ phận kho tiến hành đóng gói kiểm định để giao sớm nhất.</p>

    <!-- THÔNG TIN ĐƠN HÀNG -->
    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; margin: 20px 0;">
      <h3 style="margin-top: 0; margin-bottom: 14px; color: #0f172a; font-size: 15px; border-bottom: 1px dashed #cbd5e1; padding-bottom: 8px;">
        📦 THÔNG TIN ĐƠN HÀNG #${payment_code || 'NANO'}
      </h3>
      <table style="width: 100%; font-size: 14px; border-collapse: collapse;">
        <tr>
          <td style="padding: 6px 0; color: #64748b;">Sản phẩm:</td>
          <td style="padding: 6px 0; font-weight: bold; text-align: right; color: #0f172a;">${product_name || 'Nano Growth Habit EX'}</td>
        </tr>
        <tr>
          <td style="padding: 6px 0; color: #64748b;">Số lượng:</td>
          <td style="padding: 6px 0; font-weight: bold; text-align: right; color: #0f172a;">${quantity || 1} gói</td>
        </tr>
        <tr>
          <td style="padding: 6px 0; color: #64748b;">Tổng thanh toán:</td>
          <td style="padding: 6px 0; font-weight: 900; text-align: right; color: #b45309; font-size: 16px;">${formattedAmount}</td>
        </tr>
        <tr>
          <td style="padding: 6px 0; color: #64748b;">Mã thanh toán / CK:</td>
          <td style="padding: 6px 0; font-family: monospace; font-weight: bold; text-align: right; color: #0f172a;">${payment_code || '—'}</td>
        </tr>
        <tr>
          <td style="padding: 6px 0; color: #64748b;">Trạng thái:</td>
          <td style="padding: 6px 0; text-align: right;">${statusBadge}</td>
        </tr>
        ${customer_address ? `
        <tr>
          <td style="padding: 6px 0; color: #64748b; vertical-align: top;">Địa chỉ nhận hàng:</td>
          <td style="padding: 6px 0; text-align: right; color: #334155;">${customer_address}</td>
        </tr>` : ''}
      </table>
    </div>

    <!-- HƯỚNG DẪN NHẬN HÀNG -->
    <div style="background-color: #eff6ff; border-left: 4px solid #3b82f6; padding: 14px 16px; margin: 20px 0; border-radius: 0 8px 8px 0;">
      <h4 style="margin: 0 0 8px 0; color: #1e40af; font-size: 14px;">🚚 HƯỚNG DẪN NHẬN HÀNG & BẢO QUẢN:</h4>
      <ul style="margin: 0; padding-left: 18px; font-size: 13px; color: #1e3a8a; line-height: 1.6;">
        <li><strong>Thời gian giao hàng:</strong> 1 - 3 ngày làm việc (khu vực nội thành nhận trong 24h).</li>
        <li><strong>Đồng kiểm hàng:</strong> Ba/Mẹ được quyền mở hộp kiểm tra đúng sản phẩm nguyên seal niêm phong trước khi nhận.</li>
        <li><strong>Bảo quản:</strong> Để nơi khô ráo, thoáng mát, tránh ánh nắng gắt. Sau khi mở nắp nên đậy kín và cho con dùng đều đặn mỗi ngày.</li>
      </ul>
    </div>

    <p>Thật ra, đầu tư cho chiều cao của con là cả một hành trình đồng hành. Đội ngũ chuyên gia bên em sẽ liên hệ thăm hỏi định kỳ để cùng Ba/Mẹ theo dõi từng cm phát triển của bé.</p>

    <p>Nếu cần hỗ trợ gấp về đơn hàng, Ba/Mẹ hãy gọi ngay Hotline hoặc nhắn tin Zalo bên dưới để được xử lý ngay nhé!</p>

    <div style="margin-top: 32px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 13px; color: #64748b;">
      <p style="margin: 0; font-weight: bold; color: #0f172a;">Nano Growth Habit EX — Đồng Hành Chiều Cao Chuẩn Nhật</p>
      <p style="margin: 4px 0 0 0;">Hotline / Zalo hỗ trợ: <strong>0987.654.321</strong></p>
      <p style="margin: 4px 0 0 0;">Website: <a href="https://nano.hnkt.vn" style="color: #b45309; text-decoration: none;">https://nano.hnkt.vn</a></p>
    </div>
  </div>
  `;
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { customer_name, customer_email, product_name, quantity, amount, payment_code, customer_address, status } = req.body || {};

  if (!customer_email) {
    return res.status(400).json({ error: 'Email khách hàng là bắt buộc' });
  }

  const subject = `[Xác Nhận Đơn Hàng #${payment_code || 'NANO'}] Cảm ơn Ba/Mẹ đã tin tưởng Nano Growth EX!`;
  const html = buildOrderEmailHtml({
    customer_name,
    product_name,
    quantity,
    amount,
    payment_code,
    customer_address,
    status
  });

  try {
    const result = await sendEmail(customer_email, subject, html);
    return res.status(200).json({
      success: true,
      message: 'Đã gửi email xác nhận đơn hàng thành công!',
      data: result
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
};
