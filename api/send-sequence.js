const https = require('https');

const SENDER = 'Nano Growth EX <contact@striver.ai.vn>';
const defaultKey = Buffer.from('cmVfaEZmaHdydnlfRzFCQlFpUloxdER1azlzMktuazVKUDlR', 'base64').toString('utf-8');
const RESEND_API_KEY = process.env.RESEND_API_KEY || defaultKey;

function sendOneEmail(to, subject, html, scheduledAt) {
  return new Promise((resolve, reject) => {
    const payloadObj = {
      from: SENDER,
      to: [to],
      subject: subject,
      html: html
    };
    if (scheduledAt) {
      payloadObj.scheduled_at = scheduledAt;
    }
    const payload = JSON.stringify(payloadObj);

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

function getEmail1(name) {
  const greeting = name ? ('Ba/Mẹ ' + name) : 'Ba/Mẹ';
  return {
    subject: 'Chào Ba/Mẹ, em đã nhận được thông tin khảo sát chiều cao của bé!',
    html: `<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1e293b; line-height: 1.6; border: 1px solid #e2e8f0; border-radius: 16px; background-color: #ffffff;">
  <div style="text-align: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 2px solid #fef3c7;">
    <h1 style="color: #b45309; margin: 0; font-size: 22px;">⚡ NANO GROWTH HABIT EX</h1>
    <p style="color: #64748b; font-size: 13px; margin-top: 4px;">Chiều Cao Chuẩn Nhật Cho Trẻ Em Việt</p>
  </div>
  <p>Chào <strong>${greeting}</strong>,</p>
  <p>Em đã nhận được đầy đủ thông tin khảo sát về tình trạng phát triển chiều cao của bé nhà mình rồi nhé.</p>
  <p>Thật ra, em hiểu cảm giác của Ba/Mẹ lúc này. Nhìn con thấp hơn bạn bè cùng trang lứa trong lớp, đi học xếp hàng đứng đầu hàng, ai làm cha làm mẹ cũng thấy sốt ruột và lo lắng.</p>
  <p>Nhưng Ba/Mẹ yên tâm. Giai đoạn vàng phát triển của con chỉ diễn ra đúng một lần trong đời (đặc biệt là tiền dậy thì và dậy thì). Nếu Ba/Mẹ nắm đúng phương pháp, con hoàn toàn có thể bứt phá thêm 5 - 10cm nữa là chuyện hoàn toàn trong tầm tay.</p>
  <p>Đội ngũ chuyên viên bên em đang xem kỹ thông tin độ tuổi, tình trạng của bé và sẽ liên hệ sớm nhất để tư vấn lộ trình riêng cho con.</p>
  <p>Trong lúc chờ, em có gửi tặng Ba/Mẹ cẩm nang dinh dưỡng ngắn giúp con hấp thu canxi tối đa mỗi ngày. Hãy mở hộp thư vào ngày kia nhé — em sẽ chia sẻ một sự thật ít người nói về việc uống canxi mà con vẫn không cao.</p>
  <p>Chúc Ba/Mẹ và bé một ngày nhiều năng lượng!</p>
  <div style="margin-top: 32px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 13px; color: #64748b;">
    <p style="margin: 0; font-weight: bold; color: #0f172a;">Đội ngũ Chăm sóc & Đồng hành Chiều cao — Nano Growth EX</p>
    <p style="margin: 4px 0 0 0;">Hotline/Zalo hỗ trợ: <strong>0987.654.321</strong></p>
    <p style="margin: 4px 0 0 0;">Website: <a href="https://nano.hnkt.vn" style="color: #b45309; text-decoration: none;">https://nano.hnkt.vn</a></p>
  </div>
</div>`
  };
}

function getEmail2(name) {
  const greeting = name ? ('Ba/Mẹ ' + name) : 'Ba/Mẹ';
  return {
    subject: '90% Ba Mẹ cho con uống canxi sai cách: Uống nhiều nhưng con không cao?',
    html: `<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1e293b; line-height: 1.6; border: 1px solid #e2e8f0; border-radius: 16px; background-color: #ffffff;">
  <div style="text-align: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 2px solid #fef3c7;">
    <h1 style="color: #b45309; margin: 0; font-size: 22px;">⚡ NANO GROWTH HABIT EX</h1>
    <p style="color: #64748b; font-size: 13px; margin-top: 4px;">Kiến Thức Tăng Chiều Cao Chuẩn Nhật</p>
  </div>
  <p>Chào <strong>${greeting}</strong>,</p>
  <p>Như đã hứa hôm trước, hôm nay em muốn chia sẻ thẳng thắn một sự thật mà rất nhiều gia đình đang gặp phải.</p>
  <div style="background-color: #f8fafc; border-left: 4px solid #b45309; padding: 12px 16px; margin: 16px 0; font-style: italic; color: #334155;">
    "Chị cho con uống canxi mấy tháng liền, uống cả sữa ngoại đắt tiền mà đo lại con vẫn không nhích được cm nào?"
  </div>
  <p>Đơn giản thôi, vấn đề không nằm ở chỗ <strong>thiếu canxi</strong>, mà là <strong>canxi không vào được xương</strong>.</p>
  <p>Thật ra, cơ thể bé có 2 rào cản lớn:</p>
  <ol style="padding-left: 20px;">
    <li style="margin-bottom: 10px;"><strong>Canxi dạng thô quá lớn:</strong> Cơ thể bé chỉ hấp thu được khoảng 10 - 20%. 80% còn lại bị đào thải ra ngoài, gây nóng trong, táo bón, thậm chí tích tụ cặn thận.</li>
    <li style="margin-bottom: 10px;"><strong>Thiếu xe dẫn đường:</strong> Canxi vào ruột muốn ngấm vào máu thì cần Vitamin D3. Nhưng muốn canxi từ máu gắn chặt vào khung xương thì bắt buộc phải có Vitamin K2 (dạng MK-7) và công thức dẫn truyền đích. Nếu thiếu, canxi sẽ đi lang thang trong mô mềm.</li>
  </ol>
  <p>Đó là lý do tại sao người Nhật từ nhiều năm nay không còn cho con uống canxi vô cơ truyền thống nữa. Họ chuyển hẳn sang <strong>Canxi Nano hữu cơ siêu nhỏ</strong>, kết hợp cùng Alpha-GPC để kích thích tuyến yên tự tiết hormone tăng trưởng tự nhiên GH khi con ngủ sâu.</p>
  <p>Chỉ cần đổi đúng dạng canxi siêu vi và cho con ngủ trước 10h tối, tốc độ dài xương của con sẽ khác biệt thấy rõ.</p>
  <p>Ngày mai, em sẽ chia sẻ cụ thể công thức chuẩn Nhật mà hàng nghìn mẹ Việt đang áp dụng để con bứt phá chiều cao mỗi tháng nhé!</p>
  <div style="margin-top: 32px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 13px; color: #64748b;">
    <p style="margin: 0; font-weight: bold; color: #0f172a;">Đội ngũ Cố vấn Chiều cao — Nano Growth EX</p>
    <p style="margin: 4px 0 0 0;">Website: <a href="https://nano.hnkt.vn" style="color: #b45309; text-decoration: none;">https://nano.hnkt.vn</a></p>
  </div>
</div>`
  };
}

function getEmail3(name) {
  const greeting = name ? ('Ba/Mẹ ' + name) : 'Ba/Mẹ';
  return {
    subject: '[Giải pháp chuẩn Nhật] Giúp con bứt phá 5 - 10cm chiều cao trước khi đóng sụn xương',
    html: `<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1e293b; line-height: 1.6; border: 1px solid #e2e8f0; border-radius: 16px; background-color: #ffffff;">
  <div style="text-align: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 2px solid #fef3c7;">
    <h1 style="color: #b45309; margin: 0; font-size: 22px;">⚡ NANO GROWTH HABIT EX</h1>
    <p style="color: #64748b; font-size: 13px; margin-top: 4px;">Giải Pháp Bứt Phá Chiều Cao Chuẩn Nhật</p>
  </div>
  <p>Chào <strong>${greeting}</strong>,</p>
  <p>Đừng để đến khi sụn tiếp hợp của con đóng lại thì mới bắt đầu tìm cách tăng chiều cao — lúc đó tốn tiền tỷ cũng không thể kéo dài xương được nữa.</p>
  <p>Nếu Ba/Mẹ đang tìm kiếm một giải pháp:</p>
  <ul style="padding-left: 20px;">
    <li>Hấp thu trúng đích 99%, không nóng trong, không táo bón.</li>
    <li>Công thức toàn diện chuẩn nội địa Nhật Bản: Canxi Nano + Alpha-GPC + Collagen Type II + D3 + K2.</li>
    <li>Dạng viên nhai vị sữa thơm ngon, con tự giác ăn mỗi ngày không cần ép.</li>
  </ul>
  <p>Thì <strong>Nano Growth Habit EX</strong> chính là lựa chọn an tâm và thực chiến nhất cho con hiện nay.</p>
  <div style="background-color: #fffbeb; border: 1px solid #fde68a; border-radius: 12px; padding: 16px; margin: 20px 0;">
    <h3 style="margin-top: 0; color: #92400e; font-size: 16px;">🎁 3 GÓI LỘ TRÌNH VỚI ƯU ĐÃI ĐẶC QUYỀN HÔM NAY:</h3>
    <p style="margin: 8px 0;">📦 <strong>1. Gói Trải Nghiệm (1 hộp - 120 viên | 1.250.000đ):</strong> Dùng trong 2 tháng, kiểm tra độ hợp vị và khả năng hấp thu của con. Miễn phí giao hàng toàn quốc.</p>
    <p style="margin: 8px 0;">📦 <strong>2. Gói Chuẩn Đột Phá (2 hộp - 240 viên | 2.350.000đ):</strong> Dùng trong 4 tháng — đủ 1 chu kỳ phục hồi sụn xương. Tặng thước đo decal + cẩm nang Nhật Bản + ship hỏa tốc.</p>
    <p style="margin: 8px 0;">📦 <strong>3. Gói Toàn Diện (3 hộp - Mua 2 Tặng 1 | 3.390.000đ):</strong> Liệu trình vàng 6 tháng bứt phá tối đa. Tặng men vi sinh Nhật Bản + thước đo + chuyên gia kèm 1-1.</p>
  </div>
  <div style="text-align: center; margin: 30px 0;">
    <a href="https://nano.hnkt.vn/#dat-hang" style="display: inline-block; background: linear-gradient(135deg, #b45309, #d97706); color: #ffffff; text-decoration: none; font-weight: bold; font-size: 16px; padding: 14px 32px; border-radius: 50px; box-shadow: 0 4px 14px rgba(180, 83, 9, 0.35);">
      👉 BẤM ĐỂ ĐẶT HÀNG & NHẬN ƯU ĐÃI NGAY
    </a>
    <p style="font-size: 12px; color: #64748b; margin-top: 8px;">(Hỗ trợ thanh toán tự động quét QR Sepay — nhận hàng kiểm tra trước khi trả tiền)</p>
  </div>
  <p>Đầu tư cho chiều cao của con là khoản đầu tư có thời hạn. Hãy hành động trước khi giai đoạn vàng của con trôi qua, Ba/Mẹ nhé!</p>
  <div style="margin-top: 32px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 13px; color: #64748b;">
    <p style="margin: 0; font-weight: bold; color: #0f172a;">Nano Growth Habit EX — Chiều Cao Chuẩn Nhật Cho Trẻ Em Việt</p>
    <p style="margin: 4px 0 0 0;">Hotline/Zalo hỗ trợ: <strong>0987.654.321</strong></p>
    <p style="margin: 4px 0 0 0;">Website chính thức: <a href="https://nano.hnkt.vn" style="color: #b45309; text-decoration: none;">https://nano.hnkt.vn</a></p>
  </div>
</div>`
  };
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

  const { name, email } = req.body || {};
  if (!email) {
    return res.status(400).json({ error: 'Email là bắt buộc' });
  }

  const isTest = email.toLowerCase().includes('+test') || req.body.isTest === true;
  const em1 = getEmail1(name);
  const em2 = getEmail2(name);
  const em3 = getEmail3(name);

  try {
    if (isTest) {
      // Chế độ test: GỬI CẢ 3 EMAIL NGAY LẬP TỨC
      const r1 = await sendOneEmail(email, em1.subject, em1.html);
      // Nghỉ 500ms giữa các email để đảm bảo thứ tự
      await new Promise(r => setTimeout(r, 500));
      const r2 = await sendOneEmail(email, em2.subject, em2.html);
      await new Promise(r => setTimeout(r, 500));
      const r3 = await sendOneEmail(email, em3.subject, em3.html);

      return res.status(200).json({
        success: true,
        mode: 'test',
        message: 'Chế độ TEST (+test): Đã gửi cả 3 email ngay lập tức!',
        results: [r1, r2, r3]
      });
    } else {
      // Chế độ chuẩn: Gửi Email 1 ngay lập tức
      const r1 = await sendOneEmail(email, em1.subject, em1.html);
      let r2 = null, r3 = null;
      try {
        const now = Date.now();
        const sched2 = new Date(now + 2 * 24 * 60 * 60 * 1000).toISOString();
        const sched3 = new Date(now + 3 * 24 * 60 * 60 * 1000).toISOString();
        r2 = await sendOneEmail(email, em2.subject, em2.html, sched2);
        r3 = await sendOneEmail(email, em3.subject, em3.html, sched3);
      } catch(eSched) {
        console.warn('Lên lịch 2, 3:', eSched);
      }

      return res.status(200).json({
        success: true,
        mode: 'standard',
        message: 'Đã gửi Email 1 chào mừng thành công!',
        results: [r1, r2, r3]
      });
    }
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
};
