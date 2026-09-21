#!/usr/bin/env node

/**
 * Nano Growth Habit EX - Model Context Protocol (MCP) Server
 * Transport: Streamable-HTTP (lắng nghe tại http://127.0.0.1:3001/mcp)
 * Kết nối với goClaw AI Agent / Telegram Bot
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";
import { DatabaseSync } from "node:sqlite";
import http from "node:http";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env
const envPath = process.env.ENV_PATH || path.resolve(__dirname, "../.env");
if (fs.existsSync(envPath)) {
  dotenv.config({ path: envPath });
} else {
  dotenv.config();
}

// Cổng lắng nghe (mặc định 3001 cho goClaw)
const PORT = parseInt(process.env.MCP_PORT || "3001", 10);
const HOST = process.env.MCP_HOST || "127.0.0.1";

// Kết nối brain.db
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
// TOOL 1: update_hero - Sửa tiêu đề landing page trong 3 giây
// ─────────────────────────────────────────────────────────────
server.tool(
  "update_hero",
  "Đổi tiêu đề chính (Hero Headline h1) trên landing page index.html khi có flash sale hoặc chiến dịch mới.",
  {
    new_title: z.string().describe("Nội dung tiêu đề mới cần hiển thị trên website")
  },
  async ({ new_title }) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [MCP CALL] update_hero: "${new_title}"`);

    try {
      const htmlPath = path.resolve(__dirname, "../index.html");
      if (!fs.existsSync(htmlPath)) {
        return {
          content: [{ type: "text", text: `❌ Không tìm thấy file index.html tại: ${htmlPath}` }],
          isError: true
        };
      }

      let content = fs.readFileSync(htmlPath, "utf8");

      // Tạo bản backup trước khi sửa
      const backupPath = path.resolve(__dirname, "../index.html.bak");
      fs.writeFileSync(backupPath, content, "utf8");

      // Thay thế thẻ h1 của Hero Section
      const h1Regex = /<h1 class="text-2xl sm:text-4xl md:text-5xl font-black text-brand-cacao-900 tracking-tight leading-tight md:leading-snug mb-4">[\s\S]*?<\/h1>/;
      if (!h1Regex.test(content)) {
        return {
          content: [{ type: "text", text: `❌ Không tìm thấy thẻ tiêu đề h1 Hero Section trong index.html để thay thế.` }],
          isError: true
        };
      }

      const newH1 = `<h1 class="text-2xl sm:text-4xl md:text-5xl font-black text-brand-cacao-900 tracking-tight leading-tight md:leading-snug mb-4">\n            ${new_title}\n          </h1>`;
      content = content.replace(h1Regex, newH1);
      fs.writeFileSync(htmlPath, content, "utf8");

      return {
        content: [{
          type: "text",
          text: `✅ ĐÃ ĐỔI TIÊU ĐỀ LANDING THÀNH CÔNG!\n\n📝 Tiêu đề mới:\n"${new_title}"\n\n🌐 Khách hàng truy cập website https://nano.hnkt.vn refresh trang là sẽ thấy tiêu đề mới ngay lập tức!`
        }]
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: `❌ Lỗi khi đổi tiêu đề: ${err.message}` }],
        isError: true
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────
// TOOL 2: today_orders / get_business_stats - Báo cáo doanh thu
// ─────────────────────────────────────────────────────────────
server.tool(
  "get_business_stats",
  "Lấy báo cáo tổng quan tình hình kinh doanh: tổng doanh thu thực nhận, số đơn thành công, tổng đơn, khách hàng.",
  {},
  async () => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [MCP CALL] get_business_stats`);

    try {
      const database = getDb();
      const products = database.prepare("SELECT COUNT(*) AS count FROM products WHERE is_active = 1").get()?.count || 0;
      const customers = database.prepare("SELECT COUNT(*) AS count FROM customers").get()?.count || 0;
      const totalOrders = database.prepare("SELECT COUNT(*) AS count FROM orders").get()?.count || 0;
      const successOrders = database.prepare("SELECT COUNT(*) AS count FROM orders WHERE status = 'success'").get()?.count || 0;
      const pendingOrders = database.prepare("SELECT COUNT(*) AS count FROM orders WHERE status = 'pending'").get()?.count || 0;
      const totalRevenue = database.prepare("SELECT SUM(amount) AS total FROM orders WHERE status = 'success'").get()?.total || 0;

      const summaryText = [
        `📊 BÁO CÁO TỔNG QUAN KINH DOANH (NANO GROWTH HABIT EX):`,
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
// TOOL 3: search_customer - Tra cứu khách hàng theo SĐT / Tên
// ─────────────────────────────────────────────────────────────
server.tool(
  "search_customer",
  "Tìm kiếm thông tin khách hàng theo Số điện thoại, Email hoặc Họ tên, kèm lịch sử đơn hàng của họ.",
  {
    query: z.string().describe("Số điện thoại, email hoặc họ tên khách hàng")
  },
  async ({ query }) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [MCP CALL] search_customer: "${query}"`);

    try {
      const database = getDb();
      const searchTerm = `%${query.trim()}%`;
      const customers = database.prepare(`
        SELECT * FROM customers 
        WHERE phone LIKE ? OR email LIKE ? OR name LIKE ?
        LIMIT 5
      `).all(searchTerm, searchTerm, searchTerm);

      if (customers.length === 0) {
        return {
          content: [{ type: "text", text: `Không tìm thấy khách hàng nào khớp với từ khoá: "${query}"` }]
        };
      }

      let resultText = `🔍 Tìm thấy ${customers.length} khách hàng:\n\n`;
      for (const c of customers) {
        resultText += `👤 ID #${c.id}: ${c.name} | SĐT: ${c.phone} | Email: ${c.email || "Chưa có"} | Zalo: ${c.zalo || "N/A"}\n`;
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
          resultText += `   👉 Khách chưa phát sinh đơn hàng (đang ở danh sách waitlist/tư vấn).\n`;
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
// TOOL 4: list_orders - Xem danh sách đơn hàng gần đây
// ─────────────────────────────────────────────────────────────
server.tool(
  "list_orders",
  "Tra cứu danh sách đơn hàng gần đây, hỗ trợ lọc theo trạng thái (all, pending, success, cancelled, shipping).",
  {
    status: z.enum(["all", "pending", "success", "cancelled", "shipping"]).optional().default("all"),
    limit: z.number().int().min(1).max(50).optional().default(10)
  },
  async ({ status, limit }) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [MCP CALL] list_orders: status=${status}, limit=${limit}`);

    try {
      const database = getDb();
      let query = `
        SELECT o.id, o.quantity, o.amount, o.status, o.payment_code, o.ordered_at, o.paid_at, o.note,
               c.name AS customer_name, c.phone AS customer_phone,
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
        `#${o.id} | Khách: ${o.customer_name || "Chưa rõ"} (${o.customer_phone || "N/A"}) | SP: ${o.product_name || "N/A"} x${o.quantity} | Tiền: ${Number(o.amount).toLocaleString("vi-VN")}đ | [${o.status.toUpperCase()}] | ${o.ordered_at || "N/A"}`
      )).join("\n");

      return {
        content: [{ type: "text", text: `📦 Danh sách ${rows.length} đơn hàng gần nhất:\n\n${formatted}` }]
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: `❌ Lỗi lấy đơn hàng: ${err.message}` }],
        isError: true
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────
// TOOL 5: update_order_status - Duyệt đơn thủ công
// ─────────────────────────────────────────────────────────────
server.tool(
  "update_order_status",
  "Cập nhật trạng thái đơn hàng (duyệt đơn thành công: 'success', huỷ đơn: 'cancelled', v.v.).",
  {
    order_id: z.number().int().describe("ID đơn hàng"),
    status: z.enum(["pending", "success", "cancelled", "shipping"]).describe("Trạng thái mới"),
    note: z.string().optional().describe("Ghi chú bổ sung")
  },
  async ({ order_id, status, note }) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [MCP CALL] update_order_status: #${order_id} -> ${status}`);

    try {
      const database = getDb();
      const existing = database.prepare("SELECT * FROM orders WHERE id = ?").get(order_id);
      if (!existing) {
        return {
          content: [{ type: "text", text: `❌ Không tìm thấy đơn hàng #${order_id}.` }],
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
        content: [{ type: "text", text: `✅ Đã cập nhật đơn hàng #${order_id} sang trạng thái [${status.toUpperCase()}].` }]
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: `❌ Lỗi cập nhật: ${err.message}` }],
        isError: true
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────
// KHỞI TẠO HTTP TRANSPORT (STREAMABLE-HTTP CHO GOCLAW)
// ─────────────────────────────────────────────────────────────
async function main() {
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined // Stateless mode cho goClaw
  });

  await server.connect(transport);

  const httpServer = http.createServer(async (req, res) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, x-session-id");

    if (req.method === "OPTIONS") {
      res.writeHead(204);
      res.end();
      return;
    }

    if (req.url === "/health") {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ status: "ok", name: "nano-canxi-mcp", port: PORT, transport: "streamable-http" }));
      return;
    }

    if (req.url === "/mcp" || req.url?.startsWith("/mcp")) {
      await transport.handleRequest(req, res);
      return;
    }

    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end("Not Found");
  });

  httpServer.listen(PORT, HOST, () => {
    console.log(`===================================================`);
    console.log(`🚀 Nano Canxi MCP Server (Streamable-HTTP) running!`);
    console.log(`📍 Endpoint: http://${HOST}:${PORT}/mcp`);
    console.log(`❤️  Health:   http://${HOST}:${PORT}/health`);
    console.log(`🔒 Localhost-only bind: ${HOST}`);
    console.log(`===================================================`);
  });
}

main().catch((err) => {
  console.error("Fatal error starting MCP Server:", err);
  process.exit(1);
});
