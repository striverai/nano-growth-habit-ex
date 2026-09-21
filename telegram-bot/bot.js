/**
 * HNKT CEO AI - Telegram Bot Agent
 * Kết nối trực tiếp vào Odoo ERP (luxpeto_prod) cho trang https://hnkt.vn/nano-growth-habit-ex
 */

import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";
import pg from "pg";

const { Pool } = pg;
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env
const envPath = process.env.ENV_PATH || path.resolve(__dirname, "../.env");
if (fs.existsSync(envPath)) {
  dotenv.config({ path: envPath });
} else {
  dotenv.config();
}

const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
if (!BOT_TOKEN) {
  console.error("❌ Thiếu TELEGRAM_BOT_TOKEN trong file .env!");
  process.exit(1);
}

// Kết nối PostgreSQL Odoo (luxpeto_prod)
const pool = new Pool({
  host: process.env.ODOO_DB_HOST || "127.0.0.1",
  port: parseInt(process.env.ODOO_DB_PORT || "5432", 10),
  database: process.env.ODOO_DB_NAME || "luxpeto_prod",
  user: process.env.ODOO_DB_USER || "luxpeto",
  password: process.env.ODOO_DB_PASSWORD || "d95e505b78a44aa494c372170ad63728c506ba56dc71",
  max: 5,
  idleTimeoutMillis: 30000
});

pool.on("error", (err) => {
  console.error("⚠️ Lỗi kết nối PostgreSQL Odoo:", err.message);
});

// Hàm gửi tin nhắn Telegram
async function sendMessage(chatId, text) {
  try {
    const res = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: chatId,
        text: text,
        parse_mode: "HTML"
      })
    });
    return await res.json();
  } catch (err) {
    console.error("❌ Lỗi gửi Telegram:", err.message);
  }
}

// Parse description từ Odoo CRM
function cleanDescription(desc) {
  if (!desc) return "Không có thông tin bổ sung";
  return desc
    .replace(/<\/?[^>]+(>|$)/g, "") // Xoá thẻ html
    .replace(/\+/g, "")
    .trim();
}

// Xử lý lệnh /stats hoặc "báo cáo"
async function handleStats(chatId) {
  try {
    const client = await pool.connect();
    try {
      const statsRes = await client.query(`
        SELECT 
          COUNT(*) AS total,
          COUNT(*) FILTER (WHERE description LIKE '%1 hộp%') AS box_1,
          COUNT(*) FILTER (WHERE description LIKE '%2 hộp%') AS box_2,
          COUNT(*) FILTER (WHERE description LIKE '%3 hộp%') AS box_3
        FROM crm_lead 
        WHERE name LIKE '%Nano Growth Habit%'
      `);

      const row = statsRes.rows[0];
      const total = parseInt(row.total || 0, 10);
      const box1 = parseInt(row.box_1 || 0, 10);
      const box2 = parseInt(row.box_2 || 0, 10);
      const box3 = parseInt(row.box_3 || 0, 10);
      const estRevenue = (box1 * 1250000) + (box2 * 2350000) + (box3 * 3390000);

      const msg = [
        `📊 <b>BÁO CÁO NANO GROWTH HABIT EX (ODOO ERP)</b>`,
        `🌐 <i>Website: https://hnkt.vn/nano-growth-habit-ex</i>`,
        `─────────────────────`,
        `👥 <b>Tổng số khách đăng ký:</b> <code>${total}</code> phụ huynh`,
        `💰 <b>Tổng giá trị tạm tính:</b> <b>${estRevenue.toLocaleString("vi-VN")} đ</b>`,
        `─────────────────────`,
        `📦 <b>Phân bổ gói phụ huynh chọn:</b>`,
        `  • Gói 1 hộp (Trải nghiệm): <b>${box1}</b> khách (1.250.000đ)`,
        `  • Gói 2 hộp (Duy trì): <b>${box2}</b> khách (2.350.000đ)`,
        `  • Gói 3 hộp (Dài hạn): <b>${box3}</b> khách (3.390.000đ)`
      ].join("\n");

      await sendMessage(chatId, msg);
    } finally {
      client.release();
    }
  } catch (err) {
    await sendMessage(chatId, `❌ Lỗi khi đọc dữ liệu Odoo: ${err.message}`);
  }
}

// Xử lý lệnh /leads hoặc "khách mới"
async function handleLeads(chatId, limit = 5) {
  try {
    const client = await pool.connect();
    try {
      const res = await client.query(`
        SELECT id, contact_name, phone, create_date, description 
        FROM crm_lead 
        WHERE name LIKE '%Nano Growth Habit%' 
        ORDER BY id DESC 
        LIMIT $1
      `, [limit]);

      if (res.rows.length === 0) {
        return await sendMessage(chatId, "📭 Hiện chưa có khách hàng nào gửi thông tin trên trang.");
      }

      let msg = `📋 <b>DANH SÁCH ${res.rows.length} KHÁCH HÀNG MỚI NHẤT (ODOO CRM):</b>\n\n`;
      for (const row of res.rows) {
        const desc = cleanDescription(row.description);
        const dateStr = row.create_date ? new Date(row.create_date).toLocaleString("vi-VN", { timeZone: "Asia/Ho_Chi_Minh" }) : "N/A";
        msg += `👤 <b>#${row.id}: ${row.contact_name || "Chưa có tên"}</b>\n`;
        msg += `📞 SĐT: <code>${row.phone || "N/A"}</code>\n`;
        msg += `🕒 Đăng ký: ${dateStr}\n`;
        msg += `📝 Chi tiết:\n${desc}\n`;
        msg += `─────────────────────\n`;
      }

      await sendMessage(chatId, msg);
    } finally {
      client.release();
    }
  } catch (err) {
    await sendMessage(chatId, `❌ Lỗi khi tải danh sách khách: ${err.message}`);
  }
}

// Xử lý lệnh /find <sdt>
async function handleFind(chatId, query) {
  if (!query || query.trim().length === 0) {
    return await sendMessage(chatId, "⚠️ Vui lòng nhập số điện thoại hoặc tên cần tìm. Ví dụ: <code>/find 0912345678</code>");
  }

  try {
    const client = await pool.connect();
    try {
      const searchTerm = `%${query.trim()}%`;
      const res = await client.query(`
        SELECT id, contact_name, phone, create_date, description 
        FROM crm_lead 
        WHERE name LIKE '%Nano Growth Habit%' 
          AND (phone LIKE $1 OR contact_name ILIKE $1)
        ORDER BY id DESC 
        LIMIT 5
      `, [searchTerm]);

      if (res.rows.length === 0) {
        return await sendMessage(chatId, `🔍 Không tìm thấy phụ huynh nào khớp với: "<code>${query}</code>"`);
      }

      let msg = `🔍 <b>KẾT QUẢ TÌM KIẾM CHO: "${query}"</b>\n\n`;
      for (const row of res.rows) {
        const desc = cleanDescription(row.description);
        msg += `👤 <b>#${row.id}: ${row.contact_name}</b> | SĐT: <code>${row.phone}</code>\n`;
        msg += `${desc}\n`;
        msg += `─────────────────────\n`;
      }
      await sendMessage(chatId, msg);
    } finally {
      client.release();
    }
  } catch (err) {
    await sendMessage(chatId, `❌ Lỗi khi tìm kiếm: ${err.message}`);
  }
}

// Xử lý tin nhắn đến
async function handleMessage(msg) {
  if (!msg || !msg.text) return;

  const chatId = msg.chat.id;
  const text = msg.text.trim();
  const lower = text.toLowerCase();

  console.log(`[INCOMING] Chat ID: ${chatId} | Message: ${text}`);

  if (lower.startsWith("/start") || lower === "hi" || lower === "hello") {
    const welcome = [
      `👋 <b>Xin chào ${msg.from?.first_name || "anh"}! Em là HNKT CEO AI Assistant.</b>`,
      `Em được kết nối trực tiếp vào hệ thống Odoo ERP cho sản phẩm <b>Nano Growth Habit EX</b> tại web: https://hnkt.vn/nano-growth-habit-ex`,
      ``,
      `📌 <b>CÁC LỆNH ANH CÓ THỂ DÙNG:</b>`,
      `📊 <code>/stats</code> hoặc nhắn <code>báo cáo</code>: Xem tổng khách & tạm tính`,
      `👥 <code>/leads</code> hoặc nhắn <code>khách mới</code>: Xem danh sách phụ huynh mới nhất`,
      `🔍 <code>/find [sdt]</code>: Tra cứu phụ huynh theo số điện thoại`,
      `❓ <code>/help</code>: Xem lại hướng dẫn này`,
      ``,
      `<i>💡 Chat ID của anh hiện tại là: <code>${chatId}</code></i>`
    ].join("\n");
    return await sendMessage(chatId, welcome);
  }

  if (lower === "/stats" || lower.includes("báo cáo") || lower.includes("doanh thu") || lower.includes("thống kê")) {
    return await handleStats(chatId);
  }

  if (lower === "/leads" || lower.includes("khách mới") || lower.includes("đơn hàng") || lower.includes("danh sách")) {
    return await handleLeads(chatId, 5);
  }

  if (lower.startsWith("/find")) {
    const query = text.replace(/^\/find\s*/i, "");
    return await handleFind(chatId, query);
  }

  // Nếu người dùng nhập thẳng số điện thoại
  if (/^0[0-9]{8,10}$/.test(text.replace(/\s+/g, ""))) {
    return await handleFind(chatId, text.replace(/\s+/g, ""));
  }

  // Mặc định phản hồi hướng dẫn
  const helpMsg = [
    `🤖 Em đã nhận được tin nhắn: "<i>${text}</i>"`,
    `Để em hỗ trợ chính xác nhất, anh hãy dùng các lệnh sau nhé:`,
    `• Gõ <code>/stats</code>: Báo cáo số liệu Odoo`,
    `• Gõ <code>/leads</code>: Xem khách đăng ký mới`,
    `• Gõ <code>/find [sđt]</code>: Tìm phụ huynh theo SĐT`
  ].join("\n");
  await sendMessage(chatId, helpMsg);
}

// Vòng lặp Long Polling nhận tin nhắn Telegram
let lastUpdateId = 0;

async function poll() {
  while (true) {
    try {
      const res = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/getUpdates?offset=${lastUpdateId + 1}&timeout=30`);
      if (res.ok) {
        const data = await res.json();
        if (data.ok && Array.isArray(data.result)) {
          for (const update of data.result) {
            lastUpdateId = update.update_id;
            if (update.message) {
              await handleMessage(update.message);
            }
          }
        }
      }
    } catch (err) {
      console.error("Lỗi polling Telegram (sẽ thử lại sau 3s):", err.message);
      await new Promise((r) => setTimeout(r, 3000));
    }
  }
}

console.log("🚀 HNKT CEO AI Telegram Bot is starting...");
poll();
