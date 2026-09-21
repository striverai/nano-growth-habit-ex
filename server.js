const path = require('path');
const fs = require('fs');
const express = require('express');

// Nạp biến môi trường từ file .env nếu có
try {
  require('dotenv').config();
} catch (e) {
  // dotenv chưa được cài đặt hoặc môi trường production đã có env
}

const app = express();
const PORT = process.env.PORT || 3000;
const DB_PATH = path.join(__dirname, 'brain.db');

// Middleware xử lý JSON & URL-encoded request body
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// CORS middleware
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, apikey');
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  next();
});

// ─────────────────────────────────────────────────────────────
// 1. KẾT NỐI CƠ SỞ DỮ LIỆU brain.db (SQLite)
// ─────────────────────────────────────────────────────────────
let db = null;
try {
  const { DatabaseSync } = require('node:sqlite');
  if (fs.existsSync(DB_PATH)) {
    db = new DatabaseSync(DB_PATH);
    console.log('✅ Đã kết nối cơ sở dữ liệu brain.db (node:sqlite)');
  } else {
    console.warn('⚠️ Chưa tìm thấy file brain.db tại:', DB_PATH);
  }
} catch (err) {
  console.warn('ℹ️ Native SQLite warning:', err.message);
}

// ─────────────────────────────────────────────────────────────
// 2. CÁC ENDPOINT API HỆ THỐNG
// ─────────────────────────────────────────────────────────────
app.all('/api/send-email', (req, res) => {
  const handler = require('./api/send-email.js');
  return handler(req, res);
});

app.all('/api/send-order-confirmation', (req, res) => {
  const handler = require('./api/send-order-confirmation.js');
  return handler(req, res);
});

app.all('/api/send-sequence', (req, res) => {
  const handler = require('./api/send-sequence.js');
  return handler(req, res);
});

app.all('/api/send-telegram', (req, res) => {
  const handler = require('./api/send-telegram.js');
  return handler(req, res);
});

// ─────────────────────────────────────────────────────────────
// 3. API TRUY VẤN brain.db (Dành cho AI Agent & Admin)
// ─────────────────────────────────────────────────────────────
app.get('/api/db/stats', (req, res) => {
  if (!db) {
    return res.status(503).json({ error: 'brain.db chưa sẵn sàng hoặc không tồn tại' });
  }
  try {
    const products = db.prepare('SELECT COUNT(*) AS count FROM products').get()?.count || 0;
    const customers = db.prepare('SELECT COUNT(*) AS count FROM customers').get()?.count || 0;
    const orders = db.prepare('SELECT COUNT(*) AS count FROM orders').get()?.count || 0;
    const successOrders = db.prepare("SELECT COUNT(*) AS count FROM orders WHERE status = 'success'").get()?.count || 0;
    const revenue = db.prepare("SELECT SUM(amount) AS total FROM orders WHERE status = 'success'").get()?.total || 0;

    return res.json({
      success: true,
      data: {
        products,
        customers,
        orders,
        success_orders: successOrders,
        total_revenue: revenue
      }
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

app.get('/api/db/products', (req, res) => {
  if (!db) return res.status(503).json({ error: 'brain.db chưa sẵn sàng' });
  try {
    const rows = db.prepare('SELECT * FROM products ORDER BY id ASC').all();
    return res.json({ success: true, data: rows });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

app.get('/api/db/customers', (req, res) => {
  if (!db) return res.status(503).json({ error: 'brain.db chưa sẵn sàng' });
  try {
    const rows = db.prepare('SELECT * FROM customers ORDER BY id DESC').all();
    return res.json({ success: true, data: rows });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

app.get('/api/db/orders', (req, res) => {
  if (!db) return res.status(503).json({ error: 'brain.db chưa sẵn sàng' });
  try {
    const rows = db.prepare(`
      SELECT o.*, c.name AS customer_name, c.phone AS customer_phone, p.name AS product_name 
      FROM orders o
      LEFT JOIN customers c ON o.customer_id = c.id
      LEFT JOIN products p ON o.product_id = p.id
      ORDER BY o.id DESC
    `).all();
    return res.json({ success: true, data: rows });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString(), port: PORT });
});

// ─────────────────────────────────────────────────────────────
// 4. ĐỊNH TUYẾN GIAO DIỆN & TỆP TĨNH
// ─────────────────────────────────────────────────────────────
// Admin Panel
app.get(['/admin', '/admin/'], (req, res) => {
  res.sendFile(path.join(__dirname, 'admin', 'index.html'));
});

// Phục vụ tệp tĩnh (ảnh sản phẩm, giấy phép, css/js...)
app.use(express.static(__dirname));

// Salepage chính
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// ─────────────────────────────────────────────────────────────
// 5. KHỞI ĐỘNG SERVER
// ─────────────────────────────────────────────────────────────
app.listen(PORT, '0.0.0.0', () => {
  console.log(`===================================================`);
  console.log(`🚀 Nano Growth Server đang lắng nghe tại cổng ${PORT}`);
  console.log(`👉 Salepage: http://localhost:${PORT}`);
  console.log(`👉 Admin:    http://localhost:${PORT}/admin`);
  console.log(`👉 Health:   http://localhost:${PORT}/health`);
  console.log(`===================================================`);
});
