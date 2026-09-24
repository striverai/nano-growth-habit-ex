#!/usr/bin/env node

/**
 * Nano Growth Habit EX - Model Context Protocol (MCP) Server
 * Transports:
 *  - Streamable-HTTP (/mcp)
 *  - SSE (/sse & /messages)
 * Tools: update_hero, get_business_stats, search_customer, list_orders, update_order_status
 */

import express from "express";
import cors from "cors";
import { randomUUID } from "node:crypto";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { isInitializeRequest } from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";
import { DatabaseSync } from "node:sqlite";
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

const PORT = parseInt(process.env.MCP_PORT || "3001", 10);
const HOST = process.env.MCP_HOST || "0.0.0.0";

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

// Hàm khởi tạo McpServer kèm toàn bộ 5 tools
function createMcpServer() {
  const server = new McpServer({
    name: "nano-canxi-mcp",
    version: "1.0.0"
  });

  // TOOL 1: update_hero
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
        const backupPath = path.resolve(__dirname, "../index.html.bak");
        fs.writeFileSync(backupPath, content, "utf8");

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

  // TOOL 2: get_business_stats
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

  // TOOL 3: search_customer
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

  // TOOL 4: list_orders
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

  // TOOL 5: update_order_status
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
  // TOOL 6: get_business_signals - Đọc tín hiệu đơn mới, lead mới & báo cáo sáng
  // ─────────────────────────────────────────────────────────────
  server.tool(
    "get_business_signals",
    "Quét các tín hiệu kinh doanh mới (đơn hàng mới, lead mới) chưa gửi thông báo và tổng hợp số liệu báo cáo sáng cho chủ doanh nghiệp.",
    {
      mark_as_read: z.boolean().optional().default(true).describe("Đánh dấu các đơn và lead này là đã thông báo (notified=1) để không gửi trùng"),
      include_daily_report: z.boolean().optional().default(false).describe("Bật chế độ kèm báo cáo tổng quan kinh doanh (doanh thu, đơn hàng) phục vụ báo cáo sáng")
    },
    async ({ mark_as_read = true, include_daily_report = false }) => {
      const timestamp = new Date().toISOString();
      console.log(`[${timestamp}] [MCP CALL] get_business_signals: mark_as_read=${mark_as_read}, include_daily_report=${include_daily_report}`);
      try {
        const database = getDb();

        // 1. Quét đơn hàng mới (notified = 0)
        const newOrders = database.prepare(`
          SELECT o.id, o.quantity, o.amount, o.status, o.payment_code, o.ordered_at, o.note,
                 c.name AS customer_name, c.phone AS customer_phone,
                 p.name AS product_name
          FROM orders o
          LEFT JOIN customers c ON o.customer_id = c.id
          LEFT JOIN products p ON o.product_id = p.id
          WHERE o.notified = 0
          ORDER BY o.id ASC
        `).all();

        // 2. Quét khách hàng/lead mới (notified = 0)
        const newLeads = database.prepare(`
          SELECT id, name, phone, email, zalo, note, registered_at
          FROM customers
          WHERE notified = 0
          ORDER BY id ASC
        `).all();

        // 3. Đánh dấu đã đọc nếu mark_as_read = true
        if (mark_as_read) {
          if (newOrders.length > 0) {
            const orderIds = newOrders.map((o) => o.id);
            database.prepare(`UPDATE orders SET notified = 1 WHERE id IN (${orderIds.map(() => '?').join(',')})`).run(...orderIds);
          }
          if (newLeads.length > 0) {
            const leadIds = newLeads.map((l) => l.id);
            database.prepare(`UPDATE customers SET notified = 1 WHERE id IN (${leadIds.map(() => '?').join(',')})`).run(...leadIds);
          }
        }

        const hasSignals = newOrders.length > 0 || newLeads.length > 0;
        const sections = [];

        // Soạn nội dung thông báo
        if (hasSignals) {
          sections.push("🔔 TÍN HIỆU KINH DOANH MỚI CẦN XỬ LÝ:");

          if (newOrders.length > 0) {
            sections.push(`\n📦 ĐƠN HÀNG MỚI (${newOrders.length} đơn):`);
            for (const o of newOrders) {
              sections.push(`  • Đơn #${o.id} - ${Number(o.amount).toLocaleString("vi-VN")}đ: ${o.customer_name || "Khách"} (${o.customer_phone || "N/A"}) - ${o.product_name || "Sản phẩm"} x${o.quantity} [${o.status.toUpperCase()}]`);
            }
          }

          if (newLeads.length > 0) {
            sections.push(`\n👤 KHÁCH HÀNG / LEAD MỚI (${newLeads.length} khách):`);
            for (const l of newLeads) {
              sections.push(`  • Lead #${l.id}: ${l.name || "Khách mới"} - SĐT: ${l.phone || "Chưa có"} | Email: ${l.email || "N/A"} (${l.registered_at || "Vừa đăng ký"})`);
            }
          }
        } else if (!include_daily_report) {
          sections.push("✨ Hiện tại không có đơn hàng hay lead mới nào chưa xử lý.");
        }

        // Báo cáo sáng nếu được yêu cầu
        if (include_daily_report) {
          const totalRevenue = database.prepare("SELECT SUM(amount) AS total FROM orders WHERE status = 'success'").get()?.total || 0;
          const totalOrders = database.prepare("SELECT COUNT(*) AS count FROM orders").get()?.count || 0;
          const successOrders = database.prepare("SELECT COUNT(*) AS count FROM orders WHERE status = 'success'").get()?.count || 0;
          const pendingOrders = database.prepare("SELECT COUNT(*) AS count FROM orders WHERE status = 'pending'").get()?.count || 0;
          const totalCustomers = database.prepare("SELECT COUNT(*) AS count FROM customers").get()?.count || 0;

          sections.push(`\n☀️ BÁO CÁO SÁNG DOANH THU & HOẠT ĐỘNG:`);
          sections.push(`- Doanh thu thực nhận: ${Number(totalRevenue).toLocaleString("vi-VN")} đ`);
          sections.push(`- Tổng số đơn: ${totalOrders} (Thành công: ${successOrders} | Đang chờ: ${pendingOrders})`);
          sections.push(`- Tổng số khách/leads trong hệ thống: ${totalCustomers} khách`);
        }

        const summaryText = sections.join("\n");

        return {
          content: [{
            type: "text",
            text: summaryText
          }]
        };
      } catch (err) {
        return {
          content: [{ type: "text", text: `❌ Lỗi quét tín hiệu: ${err.message}` }],
          isError: true
        };
      }
    }
  );

  // ─────────────────────────────────────────────────────────────
  // TOOL 7: publish_facebook_post - Đăng đồng thời CẢ ẢNH & CAPTION lên Page
  // ─────────────────────────────────────────────────────────────
  server.tool(
    "publish_facebook_post",
    "Đăng bài viết và ảnh đồng thời lên Facebook Fanpage Nano Growth qua Facebook Graph API /{page_id}/photos.",
    {
      caption: z.string().describe("Nội dung bài viết / caption cần đăng"),
      image_path: z.string().optional().describe("Đường dẫn file ảnh local trên server hoặc URL ảnh online")
    },
    async ({ caption, image_path }) => {
      const timestamp = new Date().toISOString();
      console.log(`[${timestamp}] [MCP CALL] publish_facebook_post: length=${caption?.length}, image=${image_path}`);
      try {
        const pageId = process.env.FB_PAGE_ID;
        const pageToken = process.env.FB_PAGE_TOKEN;

        if (!pageId || !pageToken) {
          return {
            content: [{ type: "text", text: "❌ Thiếu cấu hình FB_PAGE_ID hoặc FB_PAGE_TOKEN trong .env!" }],
            isError: true
          };
        }

        // Tự động tìm ảnh nếu không cung cấp
        let targetImg = image_path;
        if (!targetImg) {
          const defaultCandidates = [
            path.resolve(__dirname, "../my-skills/tao-creative-fb/output/organic_post/post_organic_idea_3.png"),
            path.resolve(__dirname, "../my-skills/tao-creative-fb/output/organic_post/post_organic_idea_1.png"),
            path.resolve(__dirname, "../my-skills/tao-creative-fb/output/creative_ads/ad_set_1_pain_point.png"),
            path.resolve(__dirname, "../Ảnh sản phẩm/2026.04.16 GH 5.png")
          ];
          for (const cand of defaultCandidates) {
            if (fs.existsSync(cand)) {
              targetImg = cand;
              break;
            }
          }
        }

        const apiUrl = `https://graph.facebook.com/v19.0/${pageId}/photos`;
        const formData = new FormData();
        formData.append("caption", caption);
        formData.append("access_token", pageToken);

        if (targetImg && (targetImg.startsWith("http://") || targetImg.startsWith("https://"))) {
          formData.append("url", targetImg);
        } else if (targetImg && fs.existsSync(targetImg)) {
          const fileBuffer = fs.readFileSync(targetImg);
          const blob = new Blob([fileBuffer], { type: "image/png" });
          formData.append("source", blob, path.basename(targetImg));
        } else {
          return {
            content: [{ type: "text", text: `❌ Không tìm thấy file ảnh để đăng: ${targetImg || "Không có ảnh"}` }],
            isError: true
          };
        }

        const res = await fetch(apiUrl, {
          method: "POST",
          body: formData
        });

        const resData = await res.json();
        if (res.ok && resData.id) {
          const photoId = resData.id;
          const postId = resData.post_id || `${pageId}_${photoId}`;
          return {
            content: [{
              type: "text",
              text: `🎉 ĐÃ ĐĂNG BÀI LÊN FACEBOOK FANPAGE THÀNH CÔNG!\n\n🆔 Photo ID: ${photoId}\n📌 Post ID: ${postId}\n🔗 Xem bài đăng: https://facebook.com/${postId}`
            }]
          };
        } else {
          const errMsg = resData.error?.message || "Lỗi không xác định từ Meta API";
          return {
            content: [{ type: "text", text: `❌ Facebook Graph API báo lỗi: ${errMsg}` }],
            isError: true
          };
        }
      } catch (err) {
        return {
          content: [{ type: "text", text: `❌ Lỗi khi đăng bài Facebook: ${err.message}` }],
          isError: true
        };
      }
    }
  );

  return server;
}

// Khởi tạo Express app
const app = express();
app.use(cors());
app.use(express.json());

// Chuẩn hoá header Accept để tương thích tuyệt đối với MCP SDK
app.use((req, res, next) => {
  const accept = req.headers["accept"] || "";
  if (!accept.includes("application/json") || !accept.includes("text/event-stream")) {
    req.headers["accept"] = "application/json, text/event-stream";
  }
  next();
});

// Quản lý sessions
const httpTransports = {};
const sseTransports = {};

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    name: "nano-canxi-mcp",
    version: "1.0.0",
    transports: ["streamable-http", "sse"],
    endpoints: {
      mcp: "/mcp",
      sse: "/sse",
      messages: "/messages"
    },
    activeSessions: {
      http: Object.keys(httpTransports).length,
      sse: Object.keys(sseTransports).length
    }
  });
});

// ─────────────────────────────────────────────────────────────
// GIAO THỨC 1: STREAMABLE-HTTP (/mcp)
// ─────────────────────────────────────────────────────────────
app.all("/mcp", async (req, res) => {
  try {
    const sessionId = req.headers["mcp-session-id"] || req.query.sessionId;
    let transport;

    if (sessionId && httpTransports[sessionId]) {
      // Tái sử dụng transport theo Session ID
      transport = httpTransports[sessionId];
    } else if (req.method === "POST" && isInitializeRequest(req.body)) {
      // Yêu cầu initialize mới
      transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: () => randomUUID(),
        enableJsonResponse: true,
        onsessioninitialized: (sid) => {
          console.log(`[Streamable-HTTP] Session initialized: ${sid}`);
          httpTransports[sid] = transport;
        }
      });

      transport.onclose = () => {
        const sid = transport.sessionId;
        if (sid && httpTransports[sid]) {
          console.log(`[Streamable-HTTP] Session closed: ${sid}`);
          delete httpTransports[sid];
        }
      };

      const mcpServer = createMcpServer();
      await mcpServer.connect(transport);
    } else if (req.method === "POST" && !sessionId) {
      // Chế độ Stateless cho các request POST không kèm session
      transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: undefined,
        enableJsonResponse: true
      });
      const mcpServer = createMcpServer();
      await mcpServer.connect(transport);
    } else if (req.method === "GET") {
      // SSE GET request cho Streamable-HTTP
      if (sessionId && httpTransports[sessionId]) {
        transport = httpTransports[sessionId];
      } else {
        transport = new StreamableHTTPServerTransport({
          sessionIdGenerator: () => randomUUID(),
          enableJsonResponse: true,
          onsessioninitialized: (sid) => {
            httpTransports[sid] = transport;
          }
        });
        const mcpServer = createMcpServer();
        await mcpServer.connect(transport);
      }
    } else {
      return res.status(400).json({
        jsonrpc: "2.0",
        error: { code: -32000, message: "Bad Request: No valid session ID or initialize request" },
        id: null
      });
    }

    await transport.handleRequest(req, res, req.body);
  } catch (err) {
    console.error("[Streamable-HTTP Error]:", err);
    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: "2.0",
        error: { code: -32603, message: err.message },
        id: null
      });
    }
  }
});

// ─────────────────────────────────────────────────────────────
// GIAO THỨC 2: SSE (/sse & /messages) - Cho goClaw SSE mode
// ─────────────────────────────────────────────────────────────
app.get("/sse", async (req, res) => {
  console.log("[SSE] New client connection request");
  try {
    const transport = new SSEServerTransport("/messages", res);
    sseTransports[transport.sessionId] = transport;

    res.on("close", () => {
      console.log(`[SSE] Session disconnected: ${transport.sessionId}`);
      delete sseTransports[transport.sessionId];
    });

    const mcpServer = createMcpServer();
    await mcpServer.connect(transport);
  } catch (err) {
    console.error("[SSE Error]:", err);
    if (!res.headersSent) {
      res.status(500).send("SSE Connection Error: " + err.message);
    }
  }
});

app.post("/messages", async (req, res) => {
  const sessionId = req.query.sessionId;
  const transport = sseTransports[sessionId];
  if (transport) {
    await transport.handlePostMessage(req, res, req.body);
  } else {
    res.status(400).json({ error: "Session not found for sessionId: " + sessionId });
  }
});

// Khởi động server
app.listen(PORT, HOST, () => {
  console.log("===================================================");
  console.log("🚀 Nano Canxi Multi-Protocol MCP Server running!");
  console.log(`📍 Streamable-HTTP: http://${HOST}:${PORT}/mcp`);
  console.log(`📍 SSE Transport:   http://${HOST}:${PORT}/sse`);
  console.log(`❤️  Health:          http://${HOST}:${PORT}/health`);
  console.log("===================================================");
});
