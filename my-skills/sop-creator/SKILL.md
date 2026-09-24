---
name: sop-creator
description: Chuyên gia bóc tách nghiệp vụ thực tế và tạo quy trình vận hành tiêu chuẩn (SOP) nội bộ cho doanh nghiệp. Thiết kế đặc thù để cả con người (nhân viên, quản lý) và máy (AI Agent, tự động hóa) đều hiểu, thực thi và phối hợp nhịp nhàng (Human-in-the-loop). Sử dụng khi người dùng muốn "tạo SOP", "viết SOP", "chuẩn hóa quy trình", "quy trình nội bộ", "bóc tách nghiệp vụ", "SOP tư vấn", "SOP chốt đơn", "SOP chăm sóc khách hàng", "quy trình cho AI và người", hoặc khi cần biến một công việc làm tay lộn xộn thành tài liệu hướng dẫn từng bước rõ ràng, đo lường được.
---

# SOP Creator — Bộ Quy Trình Vận Hành Tiêu Chuẩn Cho Người & AI

## 1. Mục đích & Vai trò
Biến mọi nghiệp vụ kinh doanh, vận hành, bán hàng và kỹ thuật của doanh nghiệp thành **Quy trình Thao tác Chuẩn (SOP - Standard Operating Procedure)**.

Điểm khác biệt cốt lõi: SOP được viết theo chuẩn **Dual Human-AI Architecture**:
- **Nhân sự (Con người):** Đọc là hiểu ngay việc cần làm, không cần đào tạo phức tạp, làm đúng từng bước.
- **AI Agent (Hệ thống):** Đọc được cấu trúc logic (Trigger -> Conditions -> Actions -> Hand-off -> Verification) để chuyển hóa trực tiếp thành kịch bản tự động hóa hoặc prompt vận hành.

---

## 2. Quy trình 3 Bước Khi Nhận Yêu Cầu

### Bước 1: Tiếp nhận & Làm rõ (Clarify)
Nếu người dùng cung cấp thông tin sơ sài, hãy đặt tối đa **3 câu hỏi nhanh** trước khi viết:
1. **Kết quả đầu ra mong muốn là gì?** (Ví dụ: Chốt được đơn hàng có địa chỉ + SĐT, hoặc Đơn hàng được giao cho bưu tá).
2. **Ai tham gia vào quy trình này?** (Nhân viên sale, dược sĩ, bot AI, hay kho vận?).
3. **Hiện tại đang làm thủ công thế nào?** (Công cụ, tài liệu, bước đang làm).

*(Nếu người dùng đã cung cấp đủ ngữ cảnh từ các tài liệu có sẵn trong hệ thống như `brand_voice`, `my-business.md`, `knowledge-base.md` → Bỏ qua câu hỏi và viết ngay).*

### Bước 2: Bóc tách & Chuẩn hóa theo Khung 8 Phần
Áp dụng khung cấu trúc ở **Mục 3** để viết tài liệu SOP hoàn chỉnh.

### Bước 3: Rà soát & Kiểm thử tính khả thi
- Từng bước có gán rõ vai trò (Ai làm) không?
- Câu từ có ngắn gọn, hành động dứt khoát không?
- Các trường hợp lỗi/ngoại lệ có hướng xử lý cụ thể không?

---

## 3. Khung Cấu Trúc Chuẩn Của 1 Bản SOP (8 Phần)

Mỗi bản SOP xuất ra bắt buộc phải có đầy đủ 8 phần sau:

```markdown
# [MÃ-SOP] TÊN QUY TRÌNH
- Phiên bản: v1.0 | Ngày hiệu lực: [Ngày]
- Người phụ trách: [Chức danh] | Agent thực thi: [Tên Agent nếu có]
- Chu kỳ đánh giá: [Hàng tháng / Hàng quý]

---

### 1. MỤC TIÊU & TIÊU CHUẨN HOÀN THÀNH (Definition of Done)
- Mục tiêu chính: [Đo lường được bằng số hoặc trạng thái cụ thể]
- Tiêu chuẩn hoàn thành: [Điều kiện bắt buộc để coi quy trình đã kết thúc thành công]

### 2. PHÂN VAI TRÁCH NHIỆM (RACI Matrix Thu Nhỏ)
- [Con người 1]: Chịu trách nhiệm chính (A - Accountable) cho việc...
- [AI Agent / Hệ thống]: Tự động thực thi (R - Responsible) các bước...
- [Quản lý / CEO]: Được thông báo (I - Informed) khi phát sinh ngoại lệ...

### 3. ĐIỀU KIỆN KÍCH HOẠT & ĐẦU VÀO (Trigger & Inputs)
- Tín hiệu kích hoạt (Trigger): [Sự kiện bắt đầu: Khách nhắn tin, Webhook đơn hàng mới...]
- Dữ liệu đầu vào (Inputs): [Thông tin bắt buộc phải có trước khi thực hiện: Tên, SĐT, Nhu cầu...]

### 4. CÁC BƯỚC THỰC THI CHI TIẾT (Step-by-Step Execution)
[Liệt kê theo số thứ tự Bước 1, Bước 2, Bước 3... Kèm rõ vai trò thực thi và thời gian chuẩn SLA]
- **Bước X: [Tên bước]** (Người làm / AI làm - SLA: [Thời gian])
  - Hành động: [Động từ dứt khoát, câu ngắn < 20 từ]
  - Điều kiện rẽ nhánh (nếu có):
    - NẾU [Điều kiện A] -> Thực hiện [Hành động A]
    - NẾU [Điều kiện B] -> Thực hiện [Hành động B]

### 5. XỬ LÝ NGOẠI LỆ & RỦI RO (Edge Cases & Fallbacks)
- Trường hợp 1: [Lỗi hệ thống / Khách không phản hồi / Thông tin sai lệch]
  - Cách xử lý: [Hành động phục hồi cụ thể]
- Trường hợp 2: [AI không chắc chắn / Vượt quá thẩm quyền]
  - Điểm bàn giao (Hand-off): Chuyển giao ngay cho [Con người] qua [Kênh liên lạc].

### 6. DỮ LIỆU ĐẦU RA & BÀN GIAO (Outputs & Deliverables)
- Dữ liệu được lưu trữ tại: [Tên bảng Database, Google Sheet, CRM...]
- Thông báo gửi đến: [Kênh Telegram, Email, Notification...]

### 7. CÔNG CỤ & TÀI NGUYÊN HỖ TRỢ (Tools & Templates)
- Mẫu tin nhắn / Kịch bản thoại: [Đính kèm mẫu ngắn gọn]
- Công cụ sử dụng: [Phần mềm, MCP Tool, Thiết bị...]

### 8. BẢNG KIỂM TRA CHẤT LƯỢNG (QA Checklist)
- [ ] Tiêu chí kiểm tra 1
- [ ] Tiêu chí kiểm tra 2
- [ ] Tiêu chí kiểm tra 3
```

---

## 4. Nguyên Tắc Soạn Thảo (Writing Rules)

1. **Ngắn gọn, thực chiến:**
   - Mỗi câu dưới 20 từ. Mỗi đoạn từ 1 đến 3 câu.
   - Luôn bắt đầu mỗi bước bằng một **Động từ hành động** (Ví dụ: *"Kiểm tra...", "Nhập...", "Gửi...", "Xác nhận..."*).
2. **Phân định rõ Con Người vs Máy:**
   - Việc lặp lại, kiểm tra dữ liệu, gửi thông báo -> Giao cho **AI Agent**.
   - Việc ra quyết định nhạy cảm, đồng cảm sâu, xử lý khiếu nại gay gắt -> Giao cho **Con người**.
3. **Không dùng từ ngữ mơ hồ:**
   - Không viết: *"Tư vấn nhiệt tình, chu đáo"* -> Viết: *"Phản hồi trong 3 phút, chào hỏi theo mẫu và hỏi tuổi của bé"*.
   - Không viết: *"Kiểm tra cẩn thận"* -> Viết: *"Đối chiếu số điện thoại đủ 10 số và khớp với mã đơn hàng"*.
4. **Quy tắc chuyển giao an toàn (Safe Hand-off):**
   - Khi AI không chắc chắn (độ tin cậy < 85%) hoặc khách hàng yêu cầu gặp người thật, AI phải lập tức gắn thẻ và thông báo cho nhân sự trực tiếp.

---

## 5. Ví Dụ Mẫu (Examples)

### Ví dụ 1: SOP Tư Vấn & Chốt Đơn Qua Fanpage (Sản phẩm Nano Growth Habit EX)

```markdown
# SOP-SALES-01: QUY TRÌNH TƯ VẤN & CHỐT ĐƠN QUA FANPAGE
- Áp dụng: Đội ngũ Tư vấn viên & AI Chatbot Fanpage
- Thời gian SLA phản hồi: Dưới 3 phút

---

### 1. MỤC TIÊU & ĐỊNH NGHĨA HOÀN THÀNH
- Mục tiêu: Chuyển đổi phụ huynh nhắn tin thành đơn hàng hoặc lịch hẹn tư vấn dược sĩ.
- Tiêu chuẩn hoàn thành: Thu thập đủ: Họ tên + SĐT + Tuổi con + Gói sản phẩm + Địa chỉ giao hàng.

### 2. PHÂN VAI THỰC HIỆN
- **AI Chatbot:** Chào hỏi ban đầu, phân loại nhu cầu, thu thập thông tin cơ bản.
- **Tư vấn viên (Người):** Xử lý từ chối chuyên sâu, tư vấn phác đồ và chốt đơn.
- **Dược sĩ chuyên môn:** Hỗ trợ ca bệnh lý phức tạp (bé dị ứng, tiền sử bệnh).

### 3. ĐIỀU KIỆN KÍCH HOẠT & ĐẦU VÀO
- Trigger: Khách hàng gửi tin nhắn mới vào Fanpage hoặc bình luận để lại số điện thoại.
- Dữ liệu đầu vào: Nội dung tin nhắn của khách, ID Facebook khách hàng.

### 4. CÁC BƯỚC THỰC THI CHI TIẾT
- **Bước 1: Tiếp nhận & Phân loại nhu cầu (AI Agent - SLA: 30 giây)**
  - Gửi lời chào ngắn gọn và đặt 1 câu hỏi trọng tâm: *"Chào Ba/Mẹ, bé nhà mình hiện mấy tuổi và cao bao nhiêu cm rồi ạ?"*
  - Ghi nhận thông tin bé vào hệ thống.
- **Bước 2: Đối chiếu thể trạng & Gợi ý lộ trình (Tư vấn viên - SLA: 2 phút)**
  - Tra cứu bảng chuẩn chiều cao theo tuổi (WHO/Viện Dinh Dưỡng).
  - Nêu rõ tình trạng: Bé đang ở chuẩn hay thiếu hụt bao nhiêu cm.
  - Đề xuất lộ trình Nano Canxi chuẩn Nhật:
    - Nếu thiếu nhẹ/duy trì: Gói 1 hộp hoặc 2 hộp.
    - Nếu tiền dậy thì/dậy thì: Gói 3 hộp (Toàn diện).
- **Bước 3: Xử lý băn khoăn & Chốt thông tin (Tư vấn viên - SLA: 3 phút)**
  - NẾU khách sợ táo bón/lắng cặn: Giải thích cơ chế Canxi Nano mịn hấp thu thẳng vào xương + 6 tỷ lợi khuẩn.
  - NẾU khách chê giá cao: Chia nhỏ chi phí theo ngày (~20.000đ/ngày) để bảo vệ giai đoạn vàng duy nhất của con.
  - Xin thông tin nhận hàng: *"Em gửi gói [X] về địa chỉ nào thuận tiện cho Ba/Mẹ nhận ạ?"*
- **Bước 4: Xác nhận & Đẩy dữ liệu (AI Agent - SLA: 1 phút)**
  - Tự động tóm tắt đơn hàng gửi lại khách xác nhận qua tin nhắn.
  - Đẩy bản ghi đơn hàng vào cơ sở dữ liệu `brain.db` (`notified = 0`).

### 5. XỬ LÝ NGOẠI LỆ
- NẾU khách hỏi về bệnh lý mạn tính (thận, tim, dị ứng tảo biển):
  - Chuyển giao ngay cuộc trò chuyện cho Dược sĩ phụ trách ca trực.
  - Nhắn khách: *"Trường hợp của bé cần Dược sĩ chuyên môn đánh giá kỹ, em kết nối Dược sĩ gọi lại cho Ba/Mẹ sau 5 phút nhé."*

### 6. DỮ LIỆU ĐẦU RA
- Đơn hàng mới ghi nhận vào bảng `orders` và khách hàng mới vào `customers`.
- Bắn thông báo Telegram tức thì qua bot `@hnktceoai_bot` cho Quản lý.

### 7. BẢNG KIỂM TRA CHẤT LƯỢNG (QA Checklist)
- [ ] Khách được phản hồi dưới 3 phút từ tin nhắn đầu tiên.
- [ ] Đã khai thác đủ tuổi và tình trạng hiện tại của bé trước khi báo giá.
- [ ] Không đưa ra cam kết quá đà vi phạm nguyên tắc y khoa.
- [ ] Thông tin SĐT và địa chỉ được kiểm tra đúng định dạng trước khi lưu đơn.
```

---

## 6. Xử Lý Tình Huống Thường Gặp (Troubleshooting)

| Tình huống phát sinh | Nguyên nhân | Hướng xử lý của Skill |
|----------------------|-------------|-----------------------|
| Người dùng yêu cầu quá ngắn gọn (Ví dụ: *"Viết SOP đóng gói hàng"*) | Chưa rõ bối cảnh quy mô kho, nhân sự hay công cụ quét mã | Đặt ngay 2–3 câu hỏi định hướng nhanh, hoặc chủ động đưa ra 1 bản SOP khung chuẩn thực chiến để người dùng chỉ việc duyệt |
| Nghiệp vụ có quá nhiều bước phụ phức tạp | Dễ làm tài liệu bị dài dòng, rối mắt | Chia thành các quy trình con (Sub-SOPs) và liên kết với nhau bằng mã SOP |
| Không rõ phần việc nào nên tự động hóa | Doanh nghiệp quen làm tay 100% | Luôn chủ động đề xuất cột mốc nơi AI Agent/Tool có thể can thiệp (như ghi dữ liệu, bắn alert Telegram) để giải phóng sức người |
