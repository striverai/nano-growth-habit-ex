#!/usr/bin/env node

/**
 * Nano Growth Habit EX - Model Context Protocol (MCP) Server
 * Cung cấp "tay chân" cho AI Agent quản lý đơn hàng, khách hàng, sản phẩm, và thông báo.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { DatabaseSync } from "node:sqlite";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env from project root
const envPath = process.env.ENV_PATH || path.resolve(__dirname, "../.env");
if (fs.existsSync(envPath)) {
  dotenv.config({ path: envPath });
} else {
  dotenv.config();
}

// Locate SQLite database brain.db
const DB_PATH = process.env.BRAIN_DB_PATH || path.resolve(__dirname, "../brain.db");
let db = null;

function getDb() {
  if (!db) {
    if (!fs.existsSync(DB_PATH)) {
      throw new Error(`Không tìm thấy cơ sở dữ liệu brain.db tại: ${DB_PATH}`);
    }
    db = new DatabaseSync(DB_PATH);
  }
  return db;
}

// Khởi tạo MCP Server
const server = new McpServer({
  name: "nano-canxi-mcp",
  version: "1.0.0"
});

// ─────────────────────────────────────────────────────────────
// TOOL 1: get_business_stats - Báo cáo tổng quan kinh doanh
// ─────────────────────────────────────────────────────────────
server.tool(
  "get_business_stats",
  "Lấy báo cáo tổng quan tình hình kinh doanh: tổng doanh thu thực nhận, số đơn thành công, tổng đơn, khách hàng, sản phẩm.",
  {},
  async () => {
    try {
      const database = getDb();
      const products = database.prepare("SELECT COUNT(*) AS count FROM products WHERE is_active = 1").get()?.count || 0;
      const customers = database.prepare("SELECT COUNT(*) AS count FROM customers").get()?.count || 0;
      const totalOrders = database.prepare("SELECT COUNT(*) AS count FROM orders").get()?.count || 0;
      const successOrders = database.prepare("SELECT COUNT(*) AS count FROM orders WHERE status = 'success'").get()?.count || 0;
      const pendingOrders = database.prepare("SELECT COUNT(*) AS count FROM orders WHERE status = 'pending'").get()?.count || 0;
      const totalRevenue = database.prepare("SELECT SUM(amount) AS total FROM orders WHERE status = 'success'").get()?.total || 0;

      const summaryText = [
        `📊 BÁO CÁO TỔNG QUAN KINH DOANH (NANO CANXI):`,
        `- Tổng doanh thu thực nhận: ${Number(totalRevenue).toLocaleString("vi-VN")} đ`,
        `- Tổng số đơn hàng: ${totalOrders} đơn`,
        `  + Đã thanh toán thành công: ${successOrders} đơn`,
        `  + Chờ thanh toán / duyệt: ${pendingOrders} đơn`,
        `- Tổng số khách hàng/waitlist: ${customers} khách`,
        `- Số sản phẩm đang kinh doanh: ${products} sản phẩm`
      ].join("\n");

      return {
        content: [{ type: "text", text: summaryText }]
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: `❌ Lỗi khi lấy thống kê: ${err.message}` }],
        isError: true
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────
// TOOL 2: list_orders - Xem danh sách đơn hàng
// ─────────────────────────────────────────────────────────────
server.tool(
  "list_orders",
  "Tra cứu danh sách đơn hàng gần đây, hỗ trợ lọc theo trạng thái (all, pending, success, cancelled, shipping).",
  {
    status: z.enum(["all", "pending", "success", "cancelled", "shipping"]).optional().default("all"),
    limit: z.number().int().min(1).max(100).optional().default(20)
  },
  async ({ status, limit }) => {
    try {
      const database = getDb();
      let query = `
        SELECT o.id, o.quantity, o.amount, o.status, o.payment_code, o.ordered_at, o.paid_at, o.note,
               c.name AS customer_name, c.phone AS customer_phone, c.email AS customer_email,
               p.name AS product_name
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.id
        LEFT JOIN products p ON o.product_id = p.id
      `;
      const params = [];
      if (status && status !== "all") {
        query += " WHERE o.status = ?";
        params.push(status);
      }
      query += " ORDER BY o.id DESC LIMIT ?";
      params.push(limit);

      const rows = database.prepare(query).all(...params);
      if (rows.length === 0) {
        return {
          content: [{ type: "text", text: `Không tìm thấy đơn hàng nào với trạng thái [${status}].` }]
        };
      }

      const formatted = rows.map((o) => (
        `#${o.id} | Khách: ${o.customer_name || "Chưa rõ"} (${o.customer_phone || "N/A"}) | SP: ${o.product_name || "N/A"} x${o.quantity} | Tiền: ${Number(o.amount).toLocaleString("vi-VN")}đ | Trạng thái: [${o.status.toUpperCase()}] | Mã: ${o.payment_code || "N/A"} | Ngày: ${o.ordered_at || "N/A"}`
      )).join("\n");

      return {
        content: [{ type: "text", text: `📦 Danh sách ${rows.length} đơn hàng gần nhất:\n\n${formatted}` }]
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: `❌ Lỗi khi lấy danh sách đơn: ${err.message}` }],
        isError: true
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────
// TOOL 3: update_order_status - Cập nhật trạng thái / duyệt đơn
// ─────────────────────────────────────────────────────────────
server.tool(
  "update_order_status",
  "Cập nhật trạng thái đơn hàng (ví dụ duyệt đơn thành công: 'success', huỷ đơn: 'cancelled', v.v.).",
  {
    order_id: z.number().int().describe("ID của đơn hàng cần cập nhật"),
    status: z.enum(["pending", "success", "cancelled", "shipping"]).describe("Trạng thái mới"),
    note: z.string().optional().describe("Ghi chú bổ sung (tùy chọn)")
  },
  async ({ order_id, status, note }) => {
    try {
      const database = getDb();
      const existing = database.prepare("SELECT * FROM orders WHERE id = ?").get(order_id);
      if (!existing) {
        return {
          content: [{ type: "text", text: `❌ Không tìm thấy đơn hàng mang ID #${order_id}.` }],
          isError: true
        };
      }

      const now = new Date().toISOString();
      let sql = "UPDATE orders SET status = ?";
      const params = [status];

      if (status === "success" && !existing.paid_at) {
        sql += ", paid_at = ?";
        params.push(now);
      }
      if (note) {
        sql += ", note = ?";
        params.push(note);
      }
      sql += " WHERE id = ?";
      params.push(order_id);

      database.prepare(sql).run(...params);

      return {
        content: [{
          type: "text",
          text: `✅ Đã cập nhật đơn hàng #${order_id} thành trạng thái [${status.toUpperCase()}].${note ? ` Ghi chú: ${note}` : ""}`
        }]
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: `❌ Lỗi cập nhật đơn hàng: ${err.message}` }],
        isError: true
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────
// TOOL 4: search_customer - Tra cứu thông tin khách hàng
// ─────────────────────────────────────────────────────────────
server.tool(
  "search_customer",
  "Tìm kiếm thông tin khách hàng theo Số điện thoại, Email hoặc Họ tên, kèm lịch sử đơn hàng của họ.",
  {
    query: z.string().describe("Số điện thoại, email hoặc họ tên khách hàng")
  },
  async ({ query }) => {
    try {
      const database = getDb();
      const searchTerm = `%${query.trim()}%`;
      const customers = database.prepare(`
        SELECT * FROM customers 
        WHERE phone LIKE ? OR email LIKE ? OR name LIKE ?
        LIMIT 10
      `).all(searchTerm, searchTerm, searchTerm);

      if (customers.length === 0) {
        return {
          content: [{ type: "text", text: `Không tìm thấy khách hàng nào khớp với từ khoá: "${query}"` }]
        };
      }

      let resultText = `🔍 Tìm thấy ${customers.length} khách hàng:\n\n`;
      for (const c of customers) {
        resultText += `👤 ID #${c.id}: ${c.name} | SĐT: ${c.phone} | Email: ${c.email || "Chưa có"} | Zalo: ${c.zalo || "N/A"}\n`;
        // Lấy lịch sử đơn hàng của khách này
        const customerOrders = database.prepare(`
          SELECT o.id, o.amount, o.status, o.ordered_at, p.name AS product_name
          FROM orders o
          LEFT JOIN products p ON o.product_id = p.id
          WHERE o.customer_id = ?
        `).all(c.id);

        if (customerOrders.length > 0) {
          resultText += `   👉 Lịch sử đơn hàng (${customerOrders.length} đơn):\n`;
          for (const ord of customerOrders) {
            resultText += `      - Đơn #${ord.id}: ${ord.product_name} | ${Number(ord.amount).toLocaleString("vi-VN")}đ | [${ord.status}] | ${ord.ordered_at}\n`;
          }
        } else {
          resultText += `   👉 Khách chưa phát sinh đơn hàng nào (đang ở danh sách waitlist/tư vấn).\n`;
        }
        resultText += `\n`;
      }

      return {
        content: [{ type: "text", text: resultText.trim() }]
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: `❌ Lỗi khi tìm khách hàng: ${err.message}` }],
        isError: true
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────
// TOOL 5: list_products - Xem danh mục sản phẩm & tồn kho
// ─────────────────────────────────────────────────────────────
server.tool(
  "list_products",
  "Lấy danh sách toàn bộ sản phẩm, giá bán, loại và trạng thái tồn kho.",
  {},
  async () => {
    try {
      const database = getDb();
      const products = database.prepare("SELECT * FROM products ORDER BY id ASC").all();

      const formatted = products.map((p) => (
        `📦 ID #${p.id}: ${p.name} | Giá: ${Number(p.price).toLocaleString("vi-VN")}đ | Loại: ${p.type} | Tồn kho: ${p.stock ?? "Không giới hạn"} | Bật bán: ${p.is_active ? "ĐANG BÁN" : "TẠM NGƯNG"}\n   Mô tả: ${p.description || "N/A"}`
      )).join("\n\n");

      return {
        content: [{ type: "text", text: `📋 Danh mục sản phẩm Nano Growth Habit EX:\n\n${formatted}` }]
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: `❌ Lỗi khi lấy danh sách sản phẩm: ${err.message}` }],
        isError: true
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────
// TOOL 6: get_knowledge_base - Đọc kiến thức & brand voice
// ─────────────────────────────────────────────────────────────
server.tool(
  "get_knowledge_base",
  "Đọc tri thức sản phẩm, USP, Brand Voice, thông điệp bán hàng từ brain.db.",
  {
    topic: z.enum(["all", "business", "brand_voice", "knowledge"]).optional().default("all")
  },
  async ({ topic }) => {
    try {
      const database = getDb();
      let output = `🧠 TRI THỨC SẢN PHẨM & THƯƠNG HIỆU (brain.db):\n\n`;

      if (topic === "all" || topic === "business") {
        const businessRows = database.prepare("SELECT title, content FROM business").all();
        output += `=== 1. THÔNG TIN DOANH NGHIỆP & SẢN PHẨM ===\n`;
        businessRows.forEach((r) => { output += `📌 ${r.title}:\n${r.content}\n\n`; });
      }

      if (topic === "all" || topic === "brand_voice") {
        const voiceRows = database.prepare("SELECT title, content FROM brand_voice").all();
        output += `=== 2. BRAND VOICE & QUY TẮC NÓI CHUYỆN ===\n`;
        voiceRows.forEach((r) => { output += `🗣️ ${r.title}:\n${r.content}\n\n`; });
      }

      if (topic === "all" || topic === "knowledge") {
        const knowRows = database.prepare("SELECT title, content FROM knowledge").all();
        output += `=== 3. KIẾN THỨC BỔ SUNG ===\n`;
        knowRows.forEach((r) => { output += `💡 ${r.title}:\n${r.content}\n\n`; });
      }

      return {
        content: [{ type: "text", text: output.trim() }]
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: `❌ Lỗi đọc tri thức: ${err.message}` }],
        isError: true
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────
// TOOL 7: send_telegram_alert - Gửi thông báo Telegram
// ─────────────────────────────────────────────────────────────
server.tool(
  "send_telegram_alert",
  "Gửi tin nhắn thông báo hoặc cảnh báo tức thì vào nhóm/kênh Telegram quản trị.",
  {
    message: z.string().describe("Nội dung tin nhắn cần gửi qua Telegram")
  },
  async ({ message }) => {
    const token = process.env.TELEGRAM_BOT_TOKEN;
    const chatId = process.env.TELEGRAM_CHAT_ID;

    if (!token || !chatId) {
      return {
        content: [{ type: "text", text: "❌ Chưa cấu hình TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID trong .env" }],
        isError: true
      };
    }

    try {
      const response = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_id: chatId,
          text: message,
          parse_mode: "HTML"
        })
      });

      const data = await response.json();
      if (data.ok) {
        return {
          content: [{ type: "text", text: `✅ Đã gửi tin nhắn Telegram thành công!` }]
        };
      } else {
        return {
          content: [{ type: "text", text: `❌ Lỗi từ Telegram: ${data.description}` }],
          isError: true
        };
      }
    } catch (err) {
      return {
        content: [{ type: "text", text: `❌ Lỗi gửi Telegram: ${err.message}` }],
        isError: true
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────
// TOOL 8: send_customer_email - Gửi email qua Resend
// ─────────────────────────────────────────────────────────────
server.tool(
  "send_customer_email",
  "Gửi email chăm sóc khách hàng hoặc thông báo đơn hàng qua dịch vụ Resend.",
  {
    to: z.string().email().describe("Địa chỉ email người nhận"),
    subject: z.string().describe("Tiêu đề email"),
    html_content: z.string().describe("Nội dung email định dạng HTML")
  },
  async ({ to, subject, html_content }) => {
    const resendKey = process.env.RESEND_API_KEY;
    if (!resendKey) {
      return {
        content: [{ type: "text", text: "❌ Chưa cấu hình RESEND_API_KEY trong .env" }],
        isError: true
      };
    }

    try {
      const response = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${resendKey}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          from: "Nano Canxi <onboarding@resend.dev>",
          to: [to],
          subject: subject,
          html: html_content
        })
      });

      const data = await response.json();
      if (response.ok) {
        return {
          content: [{ type: "text", text: `✅ Đã gửi email thành công tới ${to}! (ID: ${data.id})` }]
        };
      } else {
        return {
          content: [{ type: "text", text: `❌ Lỗi từ Resend: ${data.message || JSON.stringify(data)}` }],
          isError: true
        };
      }
    } catch (err) {
      return {
        content: [{ type: "text", text: `❌ Lỗi gửi email: ${err.message}` }],
        isError: true
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────
// KHỞI CHẠY TRANSPORT (STDIO)
// ─────────────────────────────────────────────────────────────
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("🚀 Nano Canxi MCP Server is running on stdio!");
}

main().catch((err) => {
  console.error("Fatal error starting MCP Server:", err);
  process.exit(1);
});
