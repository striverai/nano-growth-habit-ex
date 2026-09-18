import os
import sys
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string, redirect

sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brain.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ─────────────────────────────────────────
# HTML TEMPLATE (Modern Tailwind UI)
# ─────────────────────────────────────────
HTML_PAGE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Nano Growth Admin Panel</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" />
  <style>
    body { background-color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; }
    .tab-active { border-bottom: 3px solid #b45309; color: #b45309; font-weight: 700; }
  </style>
</head>
<body class="min-h-screen text-slate-800">
  <!-- Header -->
  <header class="bg-gradient-to-r from-amber-900 via-amber-800 to-amber-950 text-white shadow-lg sticky top-0 z-30">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex flex-wrap justify-between items-center gap-3">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-400/40 flex items-center justify-center text-amber-300 font-black text-xl shadow-inner">
          ⚡
        </div>
        <div>
          <h1 class="text-lg sm:text-xl font-black tracking-tight">NANO GROWTH EX — ADMIN PANEL</h1>
          <p class="text-xs text-amber-200/80">Quản trị Sản phẩm, Khách hàng & Đơn hàng (brain.db)</p>
        </div>
      </div>
      <div class="flex items-center gap-2 text-xs">
        <span class="px-3 py-1.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1.5 font-semibold">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          brain.db đã kết nối
        </span>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <nav class="flex space-x-8 border-b border-amber-800/60" aria-label="Tabs">
        <button onclick="switchTab('products')" id="tab-btn-products" class="tab-btn py-3 px-1 text-sm font-semibold text-amber-100 hover:text-white flex items-center gap-2 border-b-2 border-transparent transition-all">
          <i class="fa-solid fa-box"></i> 📦 Sản Phẩm
          <span id="badge-products" class="ml-1 px-2 py-0.5 text-xs bg-amber-700/60 rounded-full font-mono">0</span>
        </button>
        <button onclick="switchTab('customers')" id="tab-btn-customers" class="tab-btn py-3 px-1 text-sm font-semibold text-amber-100 hover:text-white flex items-center gap-2 border-b-2 border-transparent transition-all">
          <i class="fa-solid fa-users"></i> 👥 Khách Hàng
          <span id="badge-customers" class="ml-1 px-2 py-0.5 text-xs bg-amber-700/60 rounded-full font-mono">0</span>
        </button>
        <button onclick="switchTab('orders')" id="tab-btn-orders" class="tab-btn py-3 px-1 text-sm font-semibold text-amber-100 hover:text-white flex items-center gap-2 border-b-2 border-transparent transition-all">
          <i class="fa-solid fa-receipt"></i> 🧾 Đơn Hàng
          <span id="badge-orders" class="ml-1 px-2 py-0.5 text-xs bg-amber-700/60 rounded-full font-mono">0</span>
        </button>
      </nav>
    </div>
  </header>

  <!-- Main Content Area -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6">
    <!-- Notifications / Alerts -->
    <div id="toast" class="hidden fixed bottom-5 right-5 z-50 px-4 py-3 rounded-xl shadow-xl text-white font-medium text-sm transition-all transform flex items-center gap-2"></div>

    <!-- ============================================================= -->
    <!-- TAB 1: SẢN PHẨM -->
    <!-- ============================================================= -->
    <section id="view-products" class="tab-view space-y-4">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
        <div>
          <h2 class="text-base sm:text-lg font-extrabold text-slate-900">Danh Sách Sản Phẩm</h2>
          <p class="text-xs text-slate-500">Quản lý các gói sản phẩm vật lý (có tồn kho) hoặc sản phẩm số / dịch vụ</p>
        </div>
        <button onclick="openProductModal()" class="px-4 py-2.5 bg-amber-700 hover:bg-amber-800 text-white rounded-xl font-bold text-xs sm:text-sm shadow flex items-center gap-2 transition-all">
          <i class="fa-solid fa-plus"></i> Thêm Sản Phẩm Mới
        </button>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm">
            <thead class="bg-slate-50 text-slate-600 font-bold border-b text-xs uppercase tracking-wider">
              <tr>
                <th class="p-3.5 text-center w-12">ID</th>
                <th class="p-3.5">Tên Sản Phẩm</th>
                <th class="p-3.5">Loại</th>
                <th class="p-3.5 text-right">Giá Bán</th>
                <th class="p-3.5 text-center">Tồn Kho</th>
                <th class="p-3.5">Mô Tả</th>
                <th class="p-3.5 text-center">Thao Tác</th>
              </tr>
            </thead>
            <tbody id="products-table-body" class="divide-y divide-slate-100 font-medium text-slate-700">
              <tr><td colspan="7" class="p-8 text-center text-slate-400">Đang tải dữ liệu...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ============================================================= -->
    <!-- TAB 2: KHÁCH HÀNG -->
    <!-- ============================================================= -->
    <section id="view-customers" class="tab-view space-y-4 hidden">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
        <div>
          <h2 class="text-base sm:text-lg font-extrabold text-slate-900">Danh Sách Khách Hàng</h2>
          <p class="text-xs text-slate-500">Danh bạ khách hàng tiềm năng, đăng ký khảo sát và đặt mua</p>
        </div>
        <button onclick="openCustomerModal()" class="px-4 py-2.5 bg-amber-700 hover:bg-amber-800 text-white rounded-xl font-bold text-xs sm:text-sm shadow flex items-center gap-2 transition-all">
          <i class="fa-solid fa-user-plus"></i> Thêm Khách Hàng
        </button>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm">
            <thead class="bg-slate-50 text-slate-600 font-bold border-b text-xs uppercase tracking-wider">
              <tr>
                <th class="p-3.5 text-center w-12">ID</th>
                <th class="p-3.5">Họ & Tên</th>
                <th class="p-3.5">Email</th>
                <th class="p-3.5">Số Điện Thoại</th>
                <th class="p-3.5">Zalo</th>
                <th class="p-3.5">Ngày Đăng Ký</th>
                <th class="p-3.5">Ghi Chú</th>
                <th class="p-3.5 text-center">Thao Tác</th>
              </tr>
            </thead>
            <tbody id="customers-table-body" class="divide-y divide-slate-100 font-medium text-slate-700">
              <tr><td colspan="8" class="p-8 text-center text-slate-400">Đang tải dữ liệu...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ============================================================= -->
    <!-- TAB 3: ĐƠN HÀNG -->
    <!-- ============================================================= -->
    <section id="view-orders" class="tab-view space-y-4 hidden">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
        <div>
          <h2 class="text-base sm:text-lg font-extrabold text-slate-900">Danh Sách Đơn Hàng</h2>
          <p class="text-xs text-slate-500">Tự động trừ tồn kho khi tạo đơn sản phẩm vật lý. Kích hoạt duyệt thanh toán thủ công nếu cần.</p>
        </div>
        <button onclick="openOrderModal()" class="px-4 py-2.5 bg-amber-700 hover:bg-amber-800 text-white rounded-xl font-bold text-xs sm:text-sm shadow flex items-center gap-2 transition-all">
          <i class="fa-solid fa-cart-plus"></i> Tạo Đơn Hàng Mới
        </button>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm">
            <thead class="bg-slate-50 text-slate-600 font-bold border-b text-xs uppercase tracking-wider">
              <tr>
                <th class="p-3.5 text-center w-12">ID</th>
                <th class="p-3.5">Khách Hàng</th>
                <th class="p-3.5">Sản Phẩm</th>
                <th class="p-3.5 text-center">SL</th>
                <th class="p-3.5 text-right">Tổng Tiền</th>
                <th class="p-3.5 text-center">Mã Sepay</th>
                <th class="p-3.5 text-center">Trạng Thái</th>
                <th class="p-3.5">Thời Gian</th>
                <th class="p-3.5 text-center">Hành Động</th>
              </tr>
            </thead>
            <tbody id="orders-table-body" class="divide-y divide-slate-100 font-medium text-slate-700">
              <tr><td colspan="9" class="p-8 text-center text-slate-400">Đang tải dữ liệu...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  </main>

  <!-- ============================================================= -->
  <!-- MODAL: SẢN PHẨM (THÊM / SỬA) -->
  <!-- ============================================================= -->
  <div id="modal-product" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm hidden flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden border border-slate-200">
      <div class="px-6 py-4 bg-slate-50 border-b flex justify-between items-center">
        <h3 id="product-modal-title" class="font-extrabold text-slate-900 text-base">Thêm Sản Phẩm Mới</h3>
        <button onclick="closeModal('modal-product')" class="text-slate-400 hover:text-slate-700 text-xl font-bold">&times;</button>
      </div>
      <form id="form-product" onsubmit="saveProduct(event)" class="p-6 space-y-4">
        <input type="hidden" id="p-id" name="id" />
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Tên sản phẩm *</label>
          <input type="text" id="p-name" required class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Loại sản phẩm *</label>
            <select id="p-type" onchange="toggleStockField()" class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none bg-white">
              <option value="physical">Vật lý (physical)</option>
              <option value="digital">Kỹ thuật số (digital)</option>
              <option value="service">Dịch vụ (service)</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Giá bán (VNĐ) *</label>
            <input type="number" id="p-price" required min="0" step="1000" class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none" />
          </div>
        </div>
        <div id="stock-container">
          <label class="block text-xs font-bold text-slate-700 mb-1">Số lượng còn lại (Tồn kho)</label>
          <input type="number" id="p-stock" min="0" placeholder="Chỉ áp dụng với hàng vật lý" class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none" />
          <p class="text-[11px] text-slate-400 mt-1">Sản phẩm số hoặc dịch vụ có thể để trống.</p>
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Mô tả sản phẩm</label>
          <textarea id="p-desc" rows="3" class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none"></textarea>
        </div>
        <div class="flex justify-end gap-2 pt-2 border-t">
          <button type="button" onclick="closeModal('modal-product')" class="px-4 py-2 border rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-50">Hủy</button>
          <button type="submit" class="px-5 py-2 bg-amber-700 hover:bg-amber-800 text-white rounded-xl text-xs font-bold shadow">Lưu Sản Phẩm</button>
        </div>
      </form>
    </div>
  </div>

  <!-- ============================================================= -->
  <!-- MODAL: KHÁCH HÀNG (THÊM / SỬA) -->
  <!-- ============================================================= -->
  <div id="modal-customer" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm hidden flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden border border-slate-200">
      <div class="px-6 py-4 bg-slate-50 border-b flex justify-between items-center">
        <h3 id="customer-modal-title" class="font-extrabold text-slate-900 text-base">Thêm Khách Hàng Mới</h3>
        <button onclick="closeModal('modal-customer')" class="text-slate-400 hover:text-slate-700 text-xl font-bold">&times;</button>
      </div>
      <form id="form-customer" onsubmit="saveCustomer(event)" class="p-6 space-y-4">
        <input type="hidden" id="c-id" name="id" />
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Họ và tên *</label>
          <input type="text" id="c-name" required class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Số điện thoại *</label>
            <input type="tel" id="c-phone" required class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Số Zalo</label>
            <input type="text" id="c-zalo" placeholder="Để trống nếu trùng SĐT" class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none" />
          </div>
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Địa chỉ Email</label>
          <input type="email" id="c-email" placeholder="email@example.com" class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none" />
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Ghi chú</label>
          <textarea id="c-note" rows="3" placeholder="Độ tuổi của bé, nhu cầu, tình trạng..." class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none"></textarea>
        </div>
        <div class="flex justify-end gap-2 pt-2 border-t">
          <button type="button" onclick="closeModal('modal-customer')" class="px-4 py-2 border rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-50">Hủy</button>
          <button type="submit" class="px-5 py-2 bg-amber-700 hover:bg-amber-800 text-white rounded-xl text-xs font-bold shadow">Lưu Khách Hàng</button>
        </div>
      </form>
    </div>
  </div>

  <!-- ============================================================= -->
  <!-- MODAL: ĐƠN HÀNG (THÊM / SỬA) -->
  <!-- ============================================================= -->
  <div id="modal-order" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm hidden flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden border border-slate-200">
      <div class="px-6 py-4 bg-slate-50 border-b flex justify-between items-center">
        <h3 id="order-modal-title" class="font-extrabold text-slate-900 text-base">Tạo Đơn Hàng Mới</h3>
        <button onclick="closeModal('modal-order')" class="text-slate-400 hover:text-slate-700 text-xl font-bold">&times;</button>
      </div>
      <form id="form-order" onsubmit="saveOrder(event)" class="p-6 space-y-4">
        <input type="hidden" id="o-id" name="id" />
        
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Khách hàng *</label>
          <select id="o-customer" required class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none bg-white"></select>
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Sản phẩm *</label>
          <select id="o-product" required onchange="onProductSelectChange()" class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none bg-white"></select>
          <div id="o-stock-hint" class="text-[11px] text-amber-700 font-medium mt-1"></div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Số lượng *</label>
            <input type="number" id="o-quantity" value="1" min="1" required oninput="calculateOrderAmount()" class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Tổng tiền (VNĐ) *</label>
            <input type="number" id="o-amount" required min="0" step="1000" class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none font-bold text-amber-800" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Trạng thái *</label>
            <select id="o-status" class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none bg-white font-semibold">
              <option value="pending">Chờ thanh toán (pending)</option>
              <option value="success">Đã thanh toán (success)</option>
              <option value="cancelled">Đã hủy (cancelled)</option>
              <option value="refunded">Đã hoàn tiền (refunded)</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Mã Sepay (Payment Code)</label>
            <input type="text" id="o-code" placeholder="Tự sinh nếu để trống" class="w-full px-3 py-2 border rounded-xl text-sm font-mono focus:ring-2 focus:ring-amber-500 outline-none" />
          </div>
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Ghi chú đơn hàng</label>
          <textarea id="o-note" rows="2" class="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none" placeholder="Địa chỉ giao hàng hoặc ghi chú..."></textarea>
        </div>

        <div class="p-3 bg-amber-50 border border-amber-200 rounded-xl text-[11px] text-amber-800">
          <i class="fa-solid fa-circle-info mr-1"></i>
          <strong>Quy tắc tồn kho:</strong> Khi thêm đơn mới cho <em>sản phẩm vật lý</em>, hệ thống sẽ tự động trừ số lượng còn lại trong kho. Sản phẩm số / dịch vụ sẽ giữ nguyên.
        </div>

        <div class="flex justify-end gap-2 pt-2 border-t">
          <button type="button" onclick="closeModal('modal-order')" class="px-4 py-2 border rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-50">Hủy</button>
          <button type="submit" class="px-5 py-2 bg-amber-700 hover:bg-amber-800 text-white rounded-xl text-xs font-bold shadow">Lưu Đơn Hàng</button>
        </div>
      </form>
    </div>
  </div>

  <!-- JAVASCRIPT LOGIC -->
  <script>
    let globalProducts = [];
    let globalCustomers = [];
    let globalOrders = [];

    // Notifications
    function showToast(msg, type = 'success') {
      const toast = document.getElementById('toast');
      toast.textContent = msg;
      toast.className = `fixed bottom-5 right-5 z-50 px-5 py-3 rounded-xl shadow-2xl text-white font-bold text-sm transition-all transform flex items-center gap-2 ${
        type === 'error' ? 'bg-red-600' : 'bg-emerald-600'
      }`;
      toast.classList.remove('hidden');
      setTimeout(() => toast.classList.add('hidden'), 3500);
    }

    function switchTab(tab) {
      document.querySelectorAll('.tab-view').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(el => {
        el.classList.remove('border-white', 'text-white');
        el.classList.add('border-transparent', 'text-amber-100');
      });

      document.getElementById('view-' + tab).classList.remove('hidden');
      const activeBtn = document.getElementById('tab-btn-' + tab);
      activeBtn.classList.remove('border-transparent', 'text-amber-100');
      activeBtn.classList.add('border-white', 'text-white');

      if (tab === 'products') loadProducts();
      if (tab === 'customers') loadCustomers();
      if (tab === 'orders') loadOrders();
    }

    function closeModal(id) {
      document.getElementById(id).classList.add('hidden');
    }

    // ─────────────────────────────────────────
    // PRODUCTS API & RENDER
    // ─────────────────────────────────────────
    async function loadProducts() {
      try {
        const res = await fetch('/api/products');
        globalProducts = await res.json();
        document.getElementById('badge-products').textContent = globalProducts.length;
        const tbody = document.getElementById('products-table-body');
        if (!globalProducts.length) {
          tbody.innerHTML = '<tr><td colspan="7" class="p-8 text-center text-slate-400">Chưa có sản phẩm nào.</td></tr>';
          return;
        }
        tbody.innerHTML = globalProducts.map(p => {
          const typeBadge = p.type === 'physical' 
            ? '<span class="px-2 py-0.5 rounded bg-blue-100 text-blue-700 text-xs font-bold">Vật lý</span>'
            : p.type === 'digital'
            ? '<span class="px-2 py-0.5 rounded bg-purple-100 text-purple-700 text-xs font-bold">Kỹ thuật số</span>'
            : '<span class="px-2 py-0.5 rounded bg-amber-100 text-amber-700 text-xs font-bold">Dịch vụ</span>';

          const stockDisplay = p.type === 'physical'
            ? `<span class="font-bold ${(p.stock ?? 0) <= 5 ? 'text-red-600' : 'text-slate-800'}">${p.stock !== null ? p.stock : 'Chưa nhập'}</span>`
            : '<span class="text-slate-400 text-xs italic">Không giới hạn</span>';

          return `
            <tr class="hover:bg-slate-50 transition-colors">
              <td class="p-3.5 text-center text-xs text-slate-400 font-mono">${p.id}</td>
              <td class="p-3.5 font-bold text-slate-900">${p.name}</td>
              <td class="p-3.5">${typeBadge}</td>
              <td class="p-3.5 text-right font-mono font-bold text-amber-800">${Number(p.price).toLocaleString('vi-VN')}đ</td>
              <td class="p-3.5 text-center font-mono">${stockDisplay}</td>
              <td class="p-3.5 text-xs text-slate-500 max-w-xs truncate">${p.description || '—'}</td>
              <td class="p-3.5 text-center whitespace-nowrap">
                <button onclick='editProduct(${JSON.stringify(p)})' class="px-2.5 py-1 text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg mr-1 font-semibold">Sửa</button>
                <button onclick="deleteProduct(${p.id})" class="px-2.5 py-1 text-xs bg-red-50 hover:bg-red-100 text-red-600 rounded-lg font-semibold">Xóa</button>
              </td>
            </tr>
          `;
        }).join('');
      } catch (e) {
        console.error(e);
        showToast('Lỗi tải danh sách sản phẩm', 'error');
      }
    }

    function toggleStockField() {
      const type = document.getElementById('p-type').value;
      const container = document.getElementById('stock-container');
      const input = document.getElementById('p-stock');
      if (type === 'physical') {
        container.style.opacity = '1';
        input.placeholder = "Ví dụ: 100";
      } else {
        container.style.opacity = '0.5';
        input.placeholder = "Sản phẩm số / dịch vụ không cần tồn kho";
      }
    }

    function openProductModal() {
      document.getElementById('product-modal-title').textContent = 'Thêm Sản Phẩm Mới';
      document.getElementById('form-product').reset();
      document.getElementById('p-id').value = '';
      toggleStockField();
      document.getElementById('modal-product').classList.remove('hidden');
    }

    function editProduct(p) {
      document.getElementById('product-modal-title').textContent = 'Chỉnh Sửa Sản Phẩm #' + p.id;
      document.getElementById('p-id').value = p.id;
      document.getElementById('p-name').value = p.name;
      document.getElementById('p-type').value = p.type;
      document.getElementById('p-price').value = p.price;
      document.getElementById('p-stock').value = p.stock !== null ? p.stock : '';
      document.getElementById('p-desc').value = p.description || '';
      toggleStockField();
      document.getElementById('modal-product').classList.remove('hidden');
    }

    async function saveProduct(e) {
      e.preventDefault();
      const id = document.getElementById('p-id').value;
      const type = document.getElementById('p-type').value;
      const stockVal = document.getElementById('p-stock').value;
      const payload = {
        name: document.getElementById('p-name').value,
        type: type,
        price: parseInt(document.getElementById('p-price').value),
        stock: type === 'physical' && stockVal !== '' ? parseInt(stockVal) : null,
        description: document.getElementById('p-desc').value
      };

      const url = id ? `/api/products/${id}` : '/api/products';
      const method = id ? 'PUT' : 'POST';
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok) {
        showToast(id ? 'Đã cập nhật sản phẩm!' : 'Đã thêm sản phẩm mới!');
        closeModal('modal-product');
        loadProducts();
      } else {
        showToast(data.error || 'Lỗi khi lưu sản phẩm', 'error');
      }
    }

    async function deleteProduct(id) {
      if (!confirm('Bạn có chắc chắn muốn xóa sản phẩm này?')) return;
      const res = await fetch(`/api/products/${id}`, { method: 'DELETE' });
      if (res.ok) {
        showToast('Đã xóa sản phẩm');
        loadProducts();
      } else {
        const data = await res.json();
        showToast(data.error || 'Không thể xóa sản phẩm', 'error');
      }
    }

    // ─────────────────────────────────────────
    // CUSTOMERS API & RENDER
    // ─────────────────────────────────────────
    async function loadCustomers() {
      try {
        const res = await fetch('/api/customers');
        globalCustomers = await res.json();
        document.getElementById('badge-customers').textContent = globalCustomers.length;
        const tbody = document.getElementById('customers-table-body');
        if (!globalCustomers.length) {
          tbody.innerHTML = '<tr><td colspan="8" class="p-8 text-center text-slate-400">Chưa có khách hàng nào.</td></tr>';
          return;
        }
        tbody.innerHTML = globalCustomers.map(c => `
          <tr class="hover:bg-slate-50 transition-colors">
            <td class="p-3.5 text-center text-xs text-slate-400 font-mono">${c.id}</td>
            <td class="p-3.5 font-bold text-slate-900">${c.name}</td>
            <td class="p-3.5 font-mono text-slate-700 text-xs">${c.email || '—'}</td>
            <td class="p-3.5 font-mono text-slate-800">${c.phone}</td>
            <td class="p-3.5 font-mono text-slate-600">${c.zalo || c.phone || '—'}</td>
            <td class="p-3.5 text-xs text-slate-500">${c.registered_at ? c.registered_at.slice(0, 10) : '—'}</td>
            <td class="p-3.5 text-xs text-slate-500 max-w-xs truncate">${c.note || '—'}</td>
            <td class="p-3.5 text-center whitespace-nowrap">
              <button onclick='editCustomer(${JSON.stringify(c)})' class="px-2.5 py-1 text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg mr-1 font-semibold">Sửa</button>
              <button onclick="deleteCustomer(${c.id})" class="px-2.5 py-1 text-xs bg-red-50 hover:bg-red-100 text-red-600 rounded-lg font-semibold">Xóa</button>
            </td>
          </tr>
        `).join('');
      } catch (e) {
        console.error(e);
        showToast('Lỗi tải danh sách khách hàng', 'error');
      }
    }

    function openCustomerModal() {
      document.getElementById('customer-modal-title').textContent = 'Thêm Khách Hàng Mới';
      document.getElementById('form-customer').reset();
      document.getElementById('c-id').value = '';
      document.getElementById('c-email').value = '';
      document.getElementById('modal-customer').classList.remove('hidden');
    }

    function editCustomer(c) {
      document.getElementById('customer-modal-title').textContent = 'Chỉnh Sửa Khách Hàng #' + c.id;
      document.getElementById('c-id').value = c.id;
      document.getElementById('c-name').value = c.name;
      document.getElementById('c-email').value = c.email || '';
      document.getElementById('c-phone').value = c.phone;
      document.getElementById('c-zalo').value = c.zalo || '';
      document.getElementById('c-note').value = c.note || '';
      document.getElementById('modal-customer').classList.remove('hidden');
    }

    async function saveCustomer(e) {
      e.preventDefault();
      const id = document.getElementById('c-id').value;
      const payload = {
        name: document.getElementById('c-name').value,
        email: document.getElementById('c-email').value,
        phone: document.getElementById('c-phone').value,
        zalo: document.getElementById('c-zalo').value,
        note: document.getElementById('c-note').value
      };

      const url = id ? `/api/customers/${id}` : '/api/customers';
      const method = id ? 'PUT' : 'POST';
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok) {
        showToast(id ? 'Đã cập nhật khách hàng!' : 'Đã thêm khách hàng!');
        closeModal('modal-customer');
        loadCustomers();
      } else {
        showToast(data.error || 'Lỗi khi lưu khách hàng', 'error');
      }
    }

    async function deleteCustomer(id) {
      if (!confirm('Bạn có chắc muốn xóa khách hàng này? Các đơn hàng liên quan có thể bị ảnh hưởng.')) return;
      const res = await fetch(`/api/customers/${id}`, { method: 'DELETE' });
      if (res.ok) {
        showToast('Đã xóa khách hàng');
        loadCustomers();
      } else {
        const data = await res.json();
        showToast(data.error || 'Không thể xóa khách hàng', 'error');
      }
    }

    // ─────────────────────────────────────────
    // ORDERS API & RENDER
    // ─────────────────────────────────────────
    async function loadOrders() {
      try {
        const res = await fetch('/api/orders');
        globalOrders = await res.json();
        document.getElementById('badge-orders').textContent = globalOrders.length;
        const tbody = document.getElementById('orders-table-body');
        if (!globalOrders.length) {
          tbody.innerHTML = '<tr><td colspan="9" class="p-8 text-center text-slate-400">Chưa có đơn hàng nào.</td></tr>';
          return;
        }

        tbody.innerHTML = globalOrders.map(o => {
          const statusBadge = o.status === 'success'
            ? '<span class="px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold inline-flex items-center gap-1">✓ Đã thanh toán</span>'
            : o.status === 'pending'
            ? '<span class="px-2.5 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-bold inline-flex items-center gap-1">⏳ Chờ duyệt</span>'
            : o.status === 'cancelled'
            ? '<span class="px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 text-xs font-semibold">Đã hủy</span>'
            : '<span class="px-2.5 py-1 rounded-full bg-red-100 text-red-700 text-xs font-semibold">Đã hoàn tiền</span>';

          const markSuccessBtn = o.status !== 'success'
            ? `<button onclick="markOrderPaid(${o.id})" class="px-2 py-1 text-xs bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-bold shadow-sm" title="Kích hoạt thanh toán thủ công (nội dung sai / chuyển tay)">⚡ Duyệt tiền</button>`
            : '';

          return `
            <tr class="hover:bg-slate-50 transition-colors">
              <td class="p-3.5 text-center text-xs text-slate-400 font-mono">${o.id}</td>
              <td class="p-3.5">
                <div class="font-bold text-slate-900">${o.customer_name || 'Khách #' + o.customer_id}</div>
                <div class="text-xs text-slate-500 font-mono">${o.customer_phone || ''}</div>
              </td>
              <td class="p-3.5">
                <div class="font-semibold text-slate-800">${o.product_name || 'SP #' + o.product_id}</div>
                <span class="text-[10px] px-1.5 py-0.5 bg-slate-100 text-slate-600 rounded font-medium">${o.product_type}</span>
              </td>
              <td class="p-3.5 text-center font-bold font-mono">${o.quantity}</td>
              <td class="p-3.5 text-right font-mono font-black text-amber-800">${Number(o.amount).toLocaleString('vi-VN')}đ</td>
              <td class="p-3.5 text-center font-mono text-xs">
                <span class="bg-amber-50 px-2 py-0.5 rounded border border-amber-200 text-amber-900 font-bold">${o.payment_code || '—'}</span>
              </td>
              <td class="p-3.5 text-center whitespace-nowrap">${statusBadge}</td>
              <td class="p-3.5 text-xs text-slate-500 whitespace-nowrap">${o.ordered_at ? o.ordered_at.slice(0, 16) : '—'}</td>
              <td class="p-3.5 text-center whitespace-nowrap space-x-1">
                ${markSuccessBtn}
                <button onclick='editOrder(${JSON.stringify(o)})' class="px-2 py-1 text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-semibold">Sửa</button>
                <button onclick="deleteOrder(${o.id})" class="px-2 py-1 text-xs bg-red-50 hover:bg-red-100 text-red-600 rounded-lg font-semibold">Xóa</button>
              </td>
            </tr>
          `;
        }).join('');
      } catch (e) {
        console.error(e);
        showToast('Lỗi tải danh sách đơn hàng', 'error');
      }
    }

    async function populateOrderDropdowns() {
      const [cRes, pRes] = await Promise.all([fetch('/api/customers'), fetch('/api/products')]);
      globalCustomers = await cRes.json();
      globalProducts = await pRes.json();

      const custSelect = document.getElementById('o-customer');
      if (!globalCustomers.length) {
        custSelect.innerHTML = '<option value="">-- Cần thêm khách hàng trước --</option>';
      } else {
        custSelect.innerHTML = globalCustomers.map(c => `
          <option value="${c.id}">${c.name} (${c.phone})</option>
        `).join('');
      }

      const prodSelect = document.getElementById('o-product');
      if (!globalProducts.length) {
        prodSelect.innerHTML = '<option value="">-- Cần thêm sản phẩm trước --</option>';
      } else {
        prodSelect.innerHTML = globalProducts.map(p => `
          <option value="${p.id}" data-price="${p.price}" data-type="${p.type}" data-stock="${p.stock}">
            ${p.name} - ${Number(p.price).toLocaleString('vi-VN')}đ [${p.type === 'physical' ? 'Tồn: ' + (p.stock !== null ? p.stock : 'N/A') : 'Số/DV'}]
          </option>
        `).join('');
      }
      onProductSelectChange();
    }

    function onProductSelectChange() {
      const select = document.getElementById('o-product');
      const opt = select.selectedOptions[0];
      const hint = document.getElementById('o-stock-hint');
      if (!opt) return;

      const type = opt.getAttribute('data-type');
      const stock = opt.getAttribute('data-stock');
      if (type === 'physical') {
        hint.innerHTML = `<span class="text-blue-700">📦 Hàng vật lý — Tồn kho hiện có: <strong>${stock !== 'null' ? stock : 'Chưa nhập'}</strong> (sẽ tự động trừ khi tạo đơn)</span>`;
      } else {
        hint.innerHTML = `<span class="text-purple-700">⚡ Sản phẩm ${type === 'digital' ? 'kỹ thuật số' : 'dịch vụ'} — KHÔNG giới hạn tồn kho (không trừ kho)</span>`;
      }
      calculateOrderAmount();
    }

    function calculateOrderAmount() {
      const select = document.getElementById('o-product');
      const opt = select.selectedOptions[0];
      if (!opt) return;
      const unitPrice = parseInt(opt.getAttribute('data-price') || 0);
      const qty = parseInt(document.getElementById('o-quantity').value || 1);
      document.getElementById('o-amount').value = unitPrice * qty;
    }

    async function openOrderModal() {
      document.getElementById('order-modal-title').textContent = 'Tạo Đơn Hàng Mới';
      document.getElementById('form-order').reset();
      document.getElementById('o-id').value = '';
      document.getElementById('o-status').value = 'pending';
      await populateOrderDropdowns();
      document.getElementById('modal-order').classList.remove('hidden');
    }

    async function editOrder(o) {
      document.getElementById('order-modal-title').textContent = 'Chỉnh Sửa Đơn Hàng #' + o.id;
      await populateOrderDropdowns();
      document.getElementById('o-id').value = o.id;
      document.getElementById('o-customer').value = o.customer_id;
      document.getElementById('o-product').value = o.product_id;
      document.getElementById('o-quantity').value = o.quantity;
      document.getElementById('o-amount').value = o.amount;
      document.getElementById('o-status').value = o.status;
      document.getElementById('o-code').value = o.payment_code || '';
      document.getElementById('o-note').value = o.note || '';
      onProductSelectChange();
      document.getElementById('modal-order').classList.remove('hidden');
    }

    async function saveOrder(e) {
      e.preventDefault();
      const id = document.getElementById('o-id').value;
      const customerId = parseInt(document.getElementById('o-customer').value);
      const productId = parseInt(document.getElementById('o-product').value);

      if (!customerId || !productId) {
        alert('Vui lòng chọn khách hàng và sản phẩm!');
        return;
      }

      const payload = {
        customer_id: customerId,
        product_id: productId,
        quantity: parseInt(document.getElementById('o-quantity').value),
        amount: parseInt(document.getElementById('o-amount').value),
        status: document.getElementById('o-status').value,
        payment_code: document.getElementById('o-code').value.trim() || null,
        note: document.getElementById('o-note').value
      };

      const url = id ? `/api/orders/${id}` : '/api/orders';
      const method = id ? 'PUT' : 'POST';
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok) {
        showToast(id ? 'Đã cập nhật đơn hàng!' : 'Đã tạo đơn hàng mới! (Tồn kho đã tự động cập nhật)');
        closeModal('modal-order');
        loadOrders();
        loadProducts(); // refresh products in case stock changed
      } else {
        showToast(data.error || 'Lỗi khi lưu đơn hàng', 'error');
      }
    }

    async function markOrderPaid(orderId) {
      if (!confirm(`Kích hoạt xác nhận thanh toán thành công bằng tay cho Đơn hàng #${orderId}?`)) return;
      const res = await fetch(`/api/orders/${orderId}/mark-paid`, { method: 'POST' });
      const data = await res.json();
      if (res.ok) {
        showToast(`Đơn hàng #${orderId} đã được duyệt thanh toán THÀNH CÔNG!`);
        loadOrders();
      } else {
        showToast(data.error || 'Lỗi khi duyệt thanh toán', 'error');
      }
    }

    async function deleteOrder(id) {
      if (!confirm('Bạn có chắc muốn xóa đơn hàng này? Lưu ý số lượng kho sẽ không tự động hoàn trả.')) return;
      const res = await fetch(`/api/orders/${id}`, { method: 'DELETE' });
      if (res.ok) {
        showToast('Đã xóa đơn hàng');
        loadOrders();
      } else {
        const data = await res.json();
        showToast(data.error || 'Không thể xóa đơn hàng', 'error');
      }
    }

    // Khởi động
    document.addEventListener('DOMContentLoaded', () => {
      loadProducts();
    });
  </script>
</body>
</html>
"""

# ─────────────────────────────────────────
# ROUTES & APIS
# ─────────────────────────────────────────
@app.route('/')
def home():
    return redirect('/admin')

@app.route('/admin')
def admin_page():
    return render_template_string(HTML_PAGE)

# ----------------- PRODUCTS CRUD -----------------
@app.route('/api/products', methods=['GET'])
def list_products():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products ORDER BY id DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json or {}
    name = data.get('name')
    ptype = data.get('type', 'physical')
    price = data.get('price', 0)
    description = data.get('description', '')
    stock = data.get('stock')

    if not name or price is None:
        return jsonify({'error': 'Tên và giá sản phẩm là bắt buộc'}), 400

    if ptype not in ('physical', 'digital', 'service'):
        return jsonify({'error': 'Loại sản phẩm không hợp lệ'}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, type, price, description, stock) VALUES (?,?,?,?,?)",
        (name, ptype, price, description, stock)
    )
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return jsonify({'id': pid, 'message': 'Tạo sản phẩm thành công'}), 201

@app.route('/api/products/<int:pid>', methods=['PUT'])
def update_product(pid):
    data = request.json or {}
    name = data.get('name')
    ptype = data.get('type')
    price = data.get('price')
    description = data.get('description')
    stock = data.get('stock')

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE products SET name = ?, type = ?, price = ?, description = ?, stock = ? WHERE id = ?",
        (name, ptype, price, description, stock, pid)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Cập nhật sản phẩm thành công'})

@app.route('/api/products/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM products WHERE id = ?", (pid,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Đã xóa sản phẩm'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Không thể xóa vì sản phẩm này đã có trong đơn hàng'}), 400

# ----------------- CUSTOMERS CRUD -----------------
@app.route('/api/customers', methods=['GET'])
def list_customers():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers ORDER BY id DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/customers', methods=['POST'])
def create_customer():
    data = request.json or {}
    name = data.get('name')
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    zalo = data.get('zalo', '').strip()
    note = data.get('note', '')

    if not name or not phone:
        return jsonify({'error': 'Tên và số điện thoại là bắt buộc'}), 400

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO customers (name, email, phone, zalo, note) VALUES (?,?,?,?,?)",
            (name, email, phone, zalo, note)
        )
        conn.commit()
        cid = cur.lastrowid
        conn.close()
        return jsonify({'id': cid, 'message': 'Thêm khách hàng thành công'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': f'Số điện thoại {phone} đã tồn tại trên hệ thống'}), 400

@app.route('/api/customers/<int:cid>', methods=['PUT'])
def update_customer(cid):
    data = request.json or {}
    name = data.get('name')
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    zalo = data.get('zalo', '').strip()
    note = data.get('note', '')

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE customers SET name = ?, email = ?, phone = ?, zalo = ?, note = ? WHERE id = ?",
            (name, email, phone, zalo, note, cid)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Cập nhật thông tin khách hàng thành công'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': f'Số điện thoại {phone} bị trùng lặp'}), 400

@app.route('/api/customers/<int:cid>', methods=['DELETE'])
def delete_customer(cid):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM customers WHERE id = ?", (cid,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Đã xóa khách hàng'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Không thể xóa vì khách hàng này đã có đơn hàng'}), 400

# ----------------- ORDERS CRUD -----------------
@app.route('/api/orders', methods=['GET'])
def list_orders():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.*, 
               c.name AS customer_name, c.phone AS customer_phone, c.email AS customer_email,
               p.name AS product_name, p.type AS product_type
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.id
        LEFT JOIN products p ON o.product_id = p.id
        ORDER BY o.id DESC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json or {}
    customer_id = data.get('customer_id')
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    amount = int(data.get('amount', 0))
    status = data.get('status', 'pending')
    payment_code = data.get('payment_code')
    note = data.get('note', '')

    if not customer_id or not product_id:
        return jsonify({'error': 'Cần chọn khách hàng và sản phẩm'}), 400

    conn = get_db()
    cur = conn.cursor()

    # 1. Kiểm tra loại sản phẩm & tồn kho
    cur.execute("SELECT id, name, type, stock FROM products WHERE id = ?", (product_id,))
    prod = cur.fetchone()
    if not prod:
        conn.close()
        return jsonify({'error': 'Sản phẩm không tồn tại'}), 404

    prod_type = prod['type']
    current_stock = prod['stock']

    # 2. Quy tắc: Nếu sản phẩm vật lý -> tự động trừ tồn kho
    if prod_type == 'physical':
        if current_stock is not None:
            if current_stock < quantity:
                conn.close()
                return jsonify({'error': f'Số lượng tồn kho không đủ (Hiện còn: {current_stock}, yêu cầu: {quantity})'}), 400
            new_stock = current_stock - quantity
            cur.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))
    # Sản phẩm số (digital) hoặc dịch vụ (service): KHÔNG trừ tồn kho

    # Tự động tạo payment code nếu chưa có
    if not payment_code:
        import random, string
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        payment_code = f"NANO{suffix}"

    paid_at = datetime.now().isoformat() if status == 'success' else None

    cur.execute("""
        INSERT INTO orders (customer_id, product_id, quantity, amount, status, payment_code, note, paid_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (customer_id, product_id, quantity, amount, status, payment_code, note, paid_at))
    conn.commit()
    oid = cur.lastrowid
    conn.close()

    return jsonify({
        'id': oid,
        'payment_code': payment_code,
        'message': f'Tạo đơn hàng #{oid} thành công' + (' (Đã trừ tồn kho)' if prod_type == 'physical' else '')
    }), 201

@app.route('/api/orders/<int:oid>', methods=['PUT'])
def update_order(oid):
    data = request.json or {}
    customer_id = data.get('customer_id')
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    amount = int(data.get('amount', 0))
    status = data.get('status', 'pending')
    payment_code = data.get('payment_code')
    note = data.get('note', '')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT status, paid_at FROM orders WHERE id = ?", (oid,))
    existing = cur.fetchone()
    paid_at = existing['paid_at'] if existing else None
    if status == 'success' and not paid_at:
        paid_at = datetime.now().isoformat()

    cur.execute("""
        UPDATE orders 
        SET customer_id = ?, product_id = ?, quantity = ?, amount = ?, status = ?, payment_code = ?, note = ?, paid_at = ?
        WHERE id = ?
    """, (customer_id, product_id, quantity, amount, status, payment_code, note, paid_at, oid))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Cập nhật đơn hàng thành công'})

@app.route('/api/orders/<int:oid>/mark-paid', methods=['POST'])
def mark_order_paid(oid):
    """Kích hoạt thanh toán thành công thủ công (admin click nút duyệt)"""
    conn = get_db()
    cur = conn.cursor()
    now_str = datetime.now().isoformat()
    cur.execute("UPDATE orders SET status = 'success', paid_at = ? WHERE id = ?", (now_str, oid))
    conn.commit()
    conn.close()
    return jsonify({'message': f'Đơn hàng #{oid} đã được kích hoạt thành công!', 'paid_at': now_str})

@app.route('/api/orders/<int:oid>', methods=['DELETE'])
def delete_order(oid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM orders WHERE id = ?", (oid,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Đã xóa đơn hàng'})

if __name__ == '__main__':
    print("Khởi động server Admin tại: http://localhost:5000/admin")
    app.run(host='0.0.0.0', port=5000, debug=False)
