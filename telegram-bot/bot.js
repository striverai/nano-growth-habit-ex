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

// ─────────────────────────────────────────────────────────────
// TÍCH HỢP TRÍ TUỆ NHÂN TẠO GEMINI CONVERSATIONAL AI
// ─────────────────────────────────────────────────────────────
async function askGemini(userText) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return null;

  try {
    let odooContext = "Hiện chưa có dữ liệu Odoo.";
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

        const recentLeadsRes = await client.query(`
          SELECT id, contact_name, phone, create_date, description 
          FROM crm_lead 
          WHERE name LIKE '%Nano Growth Habit%' 
          ORDER BY id DESC 
          LIMIT 5
        `);

        let leadsSummary = "";
        for (const l of recentLeadsRes.rows) {
          leadsSummary += `  • Khách #${l.id}: ${l.contact_name || "Chưa rõ tên"} (SĐT: ${l.phone || "N/A"}) - ${cleanDescription(l.description)}\n`;
        }

        odooContext = [
          `DỮ LIỆU THỰC TẾ ODOO ERP (Website: https://hnkt.vn/nano-growth-habit-ex):`,
          `- Tổng số khách gửi thông tin: ${total} phụ huynh`,
          `- Tổng doanh thu tạm tính: ${estRevenue.toLocaleString("vi-VN")} đ`,
          `- Phân bổ gói đã chọn: 1 hộp (${box1} khách), 2 hộp (${box2} khách), 3 hộp (${box3} khách)`,
          `- Các khách hàng đăng ký gần nhất:`,
          leadsSummary || "  (Chưa có khách đăng ký mới)"
        ].join("\n");
      } finally {
        client.release();
      }
    } catch (e) {
      console.warn("Lỗi đọc dữ liệu context cho Gemini:", e.message);
    }

    const systemPrompt = [
      `Bạn là "HNKT CEO AI" - Trợ lý thông minh cao cấp kiêm Giám đốc Vận hành cho sản phẩm Nano Growth Habit EX Nhật Bản (website: https://hnkt.vn/nano-growth-habit-ex).`,
      `Bạn đang trò chuyện trực tiếp với anh CEO Huy qua Telegram.`,
      ``,
      `QUY TẮC GIAO TIẾP:`,
      `- Luôn xưng "em" và gọi người dùng là "anh" (hoặc "anh Huy").`,
      `- Giọng văn: Thân thiện, tôn trọng, chuyên nghiệp, sắc bén kinh doanh, ân cần và tự nhiên, dùng emoji hợp lý.`,
      `- Trả lời ngắn gọn, rõ ràng, đi thẳng vào câu hỏi của anh. Định dạng tin nhắn đẹp mắt, dễ đọc trên điện thoại.`,
      `- Dựa vào dữ liệu thực tế Odoo được cung cấp bên dưới để trả lời chính xác số liệu, thông tin khách hàng.`,
      ``,
      `THÔNG TIN SẢN PHẨM:`,
      `- Nano Growth Habit EX: Canxi Tảo Đỏ sinh học kết hợp Bonepep & Vitamin D3/K2 Nhật Bản giúp trẻ 3-18 tuổi bứt phá chiều cao.`,
      `- Gói 1: Trải nghiệm 1 hộp (1.250.000đ).`,
      `- Gói 2: Chuẩn đột phá 2 hộp (2.350.000đ) - Tiết kiệm 150k.`,
      `- Gói 3: Toàn diện dài hạn 3 hộp (3.390.000đ) - Tiết kiệm 360k.`,
      ``,
      `BỐI CẢNH DỮ LIỆU THỜI GIAN THỰC TỪ ODOO ERP:`,
      odooContext
    ].join("\n");

    const payload = {
      system_instruction: { parts: [{ text: systemPrompt }] },
      contents: [{ role: "user", parts: [{ text: userText }] }],
      generationConfig: {
        temperature: 0.7,
        maxOutputTokens: 1000
      }
    };

    const candidateModels = ["gemini-flash-lite-latest", "gemini-3-flash-preview", "gemini-flash-latest"];
    for (const model of candidateModels) {
      try {
        const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          const data = await res.json();
          const reply = data.candidates?.[0]?.content?.parts?.[0]?.text;
          if (reply) return reply.trim();
        } else {
          console.warn(`Model ${model} trả về mã lỗi:`, res.status);
        }
      } catch (err) {
        console.warn(`Lỗi khi gọi model ${model}:`, err.message);
      }
    }
  } catch (err) {
    console.error("Lỗi gọi Gemini AI:", err.message);
  }
  return null;
}

// Xử lý tin nhắn đến
async function handleMessage(msg) {
  if (!msg || !msg.text) return;

  const chatId = msg.chat.id;
  const text = msg.text.trim();
  const lower = text.toLowerCase();

  console.log(`[INCOMING] Chat ID: ${chatId} | Message: ${text}`);

  if (lower === "/start") {
    const welcome = [
      `👋 <b>Xin chào ${msg.from?.first_name || "anh"}! Em là HNKT CEO AI Assistant.</b>`,
      `Em được tích hợp <b>Google Gemini AI</b> và kết nối trực tiếp vào hệ thống Odoo ERP cho sản phẩm <b>Nano Growth Habit EX</b> tại: https://hnkt.vn/nano-growth-habit-ex`,
      ``,
      `💬 <b>Anh có thể chat tự nhiên với em như một trợ lý thật:</b>`,
      `• <i>"Hôm nay có ai đăng ký không em?"</i>`,
      `• <i>"Tư vấn giúp anh mẹ có con 12 tuổi nên dùng gói nào?"</i>`,
      `• <i>"Khách mới nhất tên gì, mua gói nào?"</i>`,
      ``,
      `📌 <b>HOẶC DÙNG CÁC LỆNH NHANH:</b>`,
      `📊 <code>/stats</code>: Xem báo cáo doanh thu & khách`,
      `👥 <code>/leads</code>: Xem danh sách phụ huynh mới nhất`,
      `🔍 <code>/find [sdt]</code>: Tra cứu phụ huynh theo SĐT`,
      ``,
      `<i>💡 Chat ID của anh: <code>${chatId}</code></i>`
    ].join("\n");
    return await sendMessage(chatId, welcome);
  }

  // Các lệnh nhanh
  if (lower === "/stats" || lower === "stats" || lower === "báo cáo" || lower === "doanh thu") {
    return await handleStats(chatId);
  }

  if (lower === "/leads" || lower === "leads" || lower === "khách mới" || lower === "danh sách") {
    return await handleLeads(chatId, 5);
  }

  if (lower.startsWith("/find")) {
    const query = text.replace(/^\/find\s*/i, "");
    return await handleFind(chatId, query);
  }

  // Nhập thẳng số điện thoại
  if (/^0[0-9]{8,10}$/.test(text.replace(/\s+/g, ""))) {
    return await handleFind(chatId, text.replace(/\s+/g, ""));
  }

  // Gửi thông báo đang suy nghĩ nếu câu hỏi dài
  // Gọi Gemini AI để xử lý ngôn ngữ tự nhiên
  const aiReply = await askGemini(text);
  if (aiReply) {
    return await sendMessage(chatId, aiReply);
  }

  // Fallback nếu không có Gemini
  const helpMsg = [
    `🤖 Em đã nhận được tin nhắn: "<i>${text}</i>"`,
    `Để em hỗ trợ chính xác nhất, anh hãy dùng các lệnh sau nhé:`,
    `• Gõ <code>/stats</code>: Báo cáo số liệu Odoo`,
    `• Gõ <code>/leads</code>: Xem khách đăng ký mới`,
    `• Gõ <code>/find [sđt]</code>: Tìm phụ huynh theo SĐT`
  ].join("\n");
  await sendMessage(chatId, helpMsg);
}

// ─────────────────────────────────────────────────────────────
// TÍNH NĂNG BÁO ĐỘNG LEAD MỚI TỰ ĐỘNG (REALTIME LEAD ALERT)
// ─────────────────────────────────────────────────────────────
let lastSeenLeadId = null;

async function checkNewLeads() {
  try {
    const client = await pool.connect();
    try {
      if (lastSeenLeadId === null) {
        const maxRes = await client.query(`
          SELECT MAX(id) AS max_id 
          FROM crm_lead 
          WHERE name LIKE '%Nano Growth Habit%'
        `);
        lastSeenLeadId = parseInt(maxRes.rows[0]?.max_id || 0, 10);
        console.log(`[LEAD WATCHER] Khởi tạo theo dõi lead từ ID: ${lastSeenLeadId}`);
        return;
      }

      const newLeadsRes = await client.query(`
        SELECT id, contact_name, phone, create_date, description 
        FROM crm_lead 
        WHERE name LIKE '%Nano Growth Habit%' AND id > $1 
        ORDER BY id ASC
      `, [lastSeenLeadId]);

      for (const lead of newLeadsRes.rows) {
        lastSeenLeadId = Math.max(lastSeenLeadId, lead.id);
        const desc = cleanDescription(lead.description);
        const dateStr = lead.create_date 
          ? new Date(lead.create_date).toLocaleString("vi-VN", { timeZone: "Asia/Ho_Chi_Minh" }) 
          : "Vừa xong";

        const alertMsg = [
          `🔔 <b>CÓ KHÁCH HÀNG MỚI ĐĂNG KÝ TƯ VẤN!</b>`,
          `🌐 <i>Từ website: https://hnkt.vn/nano-growth-habit-ex</i>`,
          `─────────────────────`,
          `👤 <b>Phụ huynh:</b> ${lead.contact_name || "Chưa có tên"}`,
          `📞 <b>Số điện thoại:</b> <code>${lead.phone || "N/A"}</code>`,
          `🕒 <b>Thời gian gửi:</b> ${dateStr}`,
          `─────────────────────`,
          `📝 <b>Chi tiết nhu cầu:</b>`,
          `${desc}`,
          `─────────────────────`,
          `⚡ <i>Hãy gọi tư vấn hoặc kết bạn Zalo ngay nhé!</i>`
        ].join("\n");

        // Gửi thông báo đến Admin
        const targetChats = new Set();
        if (process.env.ADMIN_CHAT_ID) targetChats.add(process.env.ADMIN_CHAT_ID);
        if (process.env.TELEGRAM_CHAT_ID) targetChats.add(process.env.TELEGRAM_CHAT_ID);
        targetChats.add("5781808621"); // Chat ID của anh

        for (const targetId of targetChats) {
          console.log(`[LEAD ALERT] Gửi thông báo lead #${lead.id} đến Chat ID: ${targetId}`);
          await sendMessage(targetId, alertMsg);
        }
      }
    } finally {
      client.release();
    }
  } catch (err) {
    console.error("Lỗi kiểm tra lead mới:", err.message);
  }
}

// Kiểm tra lead mới mỗi 5 giây
setInterval(checkNewLeads, 5000);

// Vòng lặp Long Polling nhận tin nhắn Telegram
let lastUpdateId = 0;

async function poll() {
  // Chạy kiểm tra lead lần đầu
  await checkNewLeads();

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

console.log("🚀 HNKT CEO AI Telegram Bot is starting with Realtime Lead Alert...");
poll();

