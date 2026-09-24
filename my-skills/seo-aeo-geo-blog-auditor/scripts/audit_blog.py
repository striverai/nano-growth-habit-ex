#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blog SEO, AEO & GEO Auditor Script (Level 3 Claude Skill)
Tác giả: Chuyên viên Tối ưu Nội dung AI Search (Anthropic Skill Specification)
Mục đích: Tự động phân tích, chấm điểm và kiểm toán bài viết blog chuẩn SEO, AEO, GEO trước khi đăng.
"""

import sys
import re
import argparse
import json
from pathlib import Path

# Cấu hình UTF-8 cho Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Danh sách từ cấm theo Brand Voice (brain.db)
FORBIDDEN_WORDS = [
    "thần dược", "cam kết 100%", "tuyệt hảo", 
    "đột phá vĩ đại", "đỉnh cao", "thay đổi cuộc đời",
    "chữa khỏi hoàn toàn", "bí quyết thần thánh"
]

# Thực thể uy tín thường dùng trong kiểm định GEO
AUTHORITY_ENTITIES = [
    "gmp", "nhật bản", "bộ y tế", "who", "fda", 
    "nghiên cứu", "lâm sàng", "viện", "chứng nhận", 
    "nano", "canxi", "vitamin d3", "mk7", "chỉ số"
]

def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tách Frontmatter nếu có
    frontmatter = {}
    body = content
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        body = fm_match.group(2)
        for line in fm_text.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                frontmatter[k.strip().lower()] = v.strip().strip('"').strip("'")

    return frontmatter, body, content

def audit_seo(frontmatter, body, keyword):
    score = 0
    details = []
    
    # 1. H1 & Title
    h1_matches = re.findall(r'^#\s+(.+)$', body, re.MULTILINE)
    h1_title = h1_matches[0] if h1_matches else frontmatter.get("title", "")
    
    if h1_title:
        h1_kw = keyword.lower() in h1_title.lower() if keyword else True
        h1_len = len(h1_title)
        if h1_kw and (40 <= h1_len <= 80):
            score += 5
            details.append(("SEO-01", 5, 5, f"H1/Title tối ưu tốt ({h1_len} ký tự, chứa từ khóa)."))
        elif h1_kw:
            score += 3.5
            details.append(("SEO-01", 3.5, 5, f"H1/Title chứa từ khóa nhưng độ dài ({h1_len} ký tự) chưa tối ưu (chuẩn: 50-70)."))
        else:
            score += 2
            details.append(("SEO-01", 2, 5, "H1/Title thiếu từ khóa chính."))
    else:
        details.append(("SEO-01", 0, 5, "Không tìm thấy thẻ H1 trong bài viết!"))

    # 2. Meta Description
    meta_desc = frontmatter.get("meta_description", "")
    if meta_desc:
        meta_kw = keyword.lower() in meta_desc.lower() if keyword else True
        meta_len = len(meta_desc)
        if meta_kw and (120 <= meta_len <= 165):
            score += 5
            details.append(("SEO-02", 5, 5, f"Meta description chuẩn ({meta_len} ký tự, có từ khóa)."))
        elif meta_kw:
            score += 3
            details.append(("SEO-02", 3, 5, f"Meta description có từ khóa nhưng độ dài ({meta_len} ký tự) ngoài khoảng 130-160."))
        else:
            score += 2
            details.append(("SEO-02", 2, 5, "Meta description thiếu từ khóa chính."))
    else:
        score += 1
        details.append(("SEO-02", 1, 5, "Chưa khai báo meta_description trong Frontmatter."))

    # 3. Heading Structure (H2, H3)
    h2_matches = re.findall(r'^##\s+(.+)$', body, re.MULTILINE)
    h3_matches = re.findall(r'^###\s+(.+)$', body, re.MULTILINE)
    
    if len(h2_matches) >= 3:
        h2_with_kw = [h for h in h2_matches if keyword.lower() in h.lower()] if keyword else h2_matches
        if len(h2_with_kw) >= 1:
            score += 5
            details.append(("SEO-03", 5, 5, f"Cấu trúc Heading tốt ({len(h2_matches)} H2, {len(h3_matches)} H3, có H2 chứa từ khóa)."))
        else:
            score += 3.5
            details.append(("SEO-03", 3.5, 5, f"Có {len(h2_matches)} H2 nhưng chưa có H2 nào chứa từ khóa chính."))
    elif len(h2_matches) >= 1:
        score += 2
        details.append(("SEO-03", 2, 5, f"Số lượng H2 ít ({len(h2_matches)} H2). Cần tối thiểu 3 H2 để phân tầng nội dung."))
    else:
        details.append(("SEO-03", 0, 5, "Thiếu hoàn toàn thẻ H2."))

    # 4. Keyword Distribution & Density
    words = re.findall(r'\b\w+\b', body)
    total_words = len(words)
    first_150_words = " ".join(words[:150]).lower()
    
    if keyword and total_words > 0:
        kw_count = len(re.findall(re.escape(keyword.lower()), body.lower()))
        density = (kw_count * len(keyword.split()) / total_words) * 100
        in_first_150 = keyword.lower() in first_150_words
        
        kw_score = 0
        notes = []
        if in_first_150:
            kw_score += 2.5
            notes.append("Từ khóa xuất hiện trong 150 từ đầu")
        else:
            notes.append("Từ khóa KHÔNG xuất hiện trong 150 từ đầu")
            
        if 0.7 <= density <= 3.0:
            kw_score += 2.5
            notes.append(f"Mật độ từ khóa lý tưởng ({density:.1f}%, {kw_count} lần)")
        elif density < 0.7:
            kw_score += 1.0
            notes.append(f"Mật độ từ khóa hơi thấp ({density:.1f}%, {kw_count} lần)")
        else:
            kw_score += 1.0
            notes.append(f"Cảnh báo nhồi từ khóa ({density:.1f}%, {kw_count} lần)")
            
        score += kw_score
        details.append(("SEO-04", kw_score, 5, "; ".join(notes)))
    else:
        score += 3
        details.append(("SEO-04", 3, 5, "Không có từ khóa để đo lường mật độ."))

    # 5. Word Count
    if total_words >= 1200:
        score += 5
        details.append(("SEO-05", 5, 5, f"Độ dài bài viết rất tốt ({total_words} từ)."))
    elif total_words >= 800:
        score += 3.5
        details.append(("SEO-05", 3.5, 5, f"Độ dài bài viết tạm ổn ({total_words} từ). Nên mở rộng thêm trên 1.200 từ."))
    elif total_words >= 400:
        score += 2
        details.append(("SEO-05", 2, 5, f"Bài viết còn ngắn ({total_words} từ). Thiếu chiều sâu cạnh tranh."))
    else:
        score += 0.5
        details.append(("SEO-05", 0.5, 5, f"Bài viết quá ngắn ({total_words} từ)."))

    # 6. Links & Alt Images
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', body)
    images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', body)
    
    link_score = 0
    if len(links) >= 2:
        link_score += 3
    elif len(links) >= 1:
        link_score += 1.5
        
    if len(images) >= 1:
        has_alt = any(len(alt.strip()) > 0 for alt, src in images)
        link_score += 2 if has_alt else 1
    else:
        link_score += 1 # Cho điểm chuẩn bị layout
        
    score += link_score
    details.append(("SEO-06", link_score, 5, f"Có {len(links)} liên kết và {len(images)} hình ảnh/vị trí ảnh."))

    return score, details, total_words

def audit_aeo(body):
    score = 0
    details = []

    # 1. Direct Answer Box (Khối tóm tắt trả lời trực tiếp đầu bài)
    # Tìm blockquote dạng > **...** hoặc đoạn văn ngắn trước H2 đầu tiên
    first_h2_pos = body.find("## ")
    pre_h2_text = body[:first_h2_pos] if first_h2_pos != -1 else body[:500]
    
    has_answer_box = bool(re.search(r'>\s*.*?(tóm tắt|câu trả lời|trả lời trực tiếp|đáp|answer)', pre_h2_text, re.IGNORECASE))
    if has_answer_box:
        score += 10
        details.append(("AEO-01", 10, 10, "Có Direct Answer Box nổi bật ở đầu bài sẵn sàng cho Featured Snippets."))
    elif "> " in pre_h2_text:
        score += 7
        details.append(("AEO-01", 7, 10, "Có khối trích dẫn ở đầu bài nhưng chưa định dạng rõ từ khóa tóm tắt câu trả lời."))
    else:
        score += 3
        details.append(("AEO-01", 3, 10, "Thiếu Direct Answer Box ở đầu bài. Cần bổ sung hộp tóm tắt 40-60 từ."))

    # 2. Definition Capsules dưới H2
    h2_sections = re.split(r'\n##\s+', body)[1:]
    capsule_count = 0
    for sec in h2_sections:
        lines = [line.strip() for line in sec.splitlines() if line.strip() and not line.startswith('#')]
        if lines:
            first_line = lines[0]
            # Kiểm tra nếu dòng đầu ngắn, định nghĩa dứt khoát hoặc là blockquote
            if first_line.startswith('>') or (len(first_line.split()) <= 45 and not first_line.startswith('-')):
                capsule_count += 1
                
    if capsule_count >= 2:
        score += 8
        details.append(("AEO-02", 8, 8, f"Có {capsule_count} đoạn định nghĩa ngắn trực diện dưới các H2."))
    elif capsule_count == 1:
        score += 5
        details.append(("AEO-02", 5, 8, f"Có 1 đoạn định nghĩa trực diện dưới H2. Nên tăng cường thêm dưới các H2 khác."))
    else:
        score += 2
        details.append(("AEO-02", 2, 8, "Các H2 bắt đầu bằng đoạn văn dài, thiếu câu trả lời ngắn dứt khoát cho AI Voice."))

    # 3. FAQ Section & Schema Q&A
    has_faq_heading = bool(re.search(r'##\s+.*?(câu hỏi thường gặp|faq|hỏi đáp)', body, re.IGNORECASE))
    qa_pairs = re.findall(r'(Q\d*:|\*\*Câu hỏi|\*\*Hỏi:).*?\n.*?(A\d*:|\*\*Trả lời:|\*\*Đáp:)', body, re.IGNORECASE)
    h3_in_faq = len(re.findall(r'###\s+.*\?', body))
    
    total_questions = max(len(qa_pairs), h3_in_faq)
    if has_faq_heading and total_questions >= 3:
        score += 8
        details.append(("AEO-03", 8, 8, f"Có khối FAQ chuẩn cấu trúc với {total_questions} câu hỏi đáp cụ thể."))
    elif has_faq_heading and total_questions >= 1:
        score += 5
        details.append(("AEO-03", 5, 8, f"Có mục FAQ nhưng số lượng câu hỏi ít ({total_questions} câu). Khuyến nghị 3-5 câu."))
    elif total_questions >= 2:
        score += 4
        details.append(("AEO-03", 4, 8, "Có các câu hỏi đáp rải rác nhưng chưa gom thành khối FAQ Schema tập trung."))
    else:
        score += 1
        details.append(("AEO-03", 1, 8, "Thiếu mục FAQ - Đánh mất cơ hội lớn xếp hạng People Also Ask."))

    # 4. Bullet & Numbered lists
    list_items = re.findall(r'^\s*([-*]|\d+\.)\s+.+$', body, re.MULTILINE)
    if len(list_items) >= 6:
        score += 4
        details.append(("AEO-04", 4, 4, f"Cấu trúc danh sách rất tốt ({len(list_items)} mục bullet/numbered)."))
    elif len(list_items) >= 3:
        score += 2.5
        details.append(("AEO-04", 2.5, 4, f"Có {len(list_items)} mục danh sách. Nên bổ sung thêm để dễ quét ý."))
    else:
        score += 1
        details.append(("AEO-04", 1, 4, "Ít danh sách liệt kê. Văn bản có xu hướng tạo thành khối khó đọc lướt."))

    return score, details

def audit_geo(body):
    score = 0
    details = []

    # 1. Named Entity Density (Mật độ thực thể định danh)
    lower_body = body.lower()
    found_entities = [e for e in AUTHORITY_ENTITIES if e in lower_body]
    if len(found_entities) >= 7:
        score += 8
        details.append(("GEO-01", 8, 8, f"Mật độ thực thể khoa học rất cao ({len(found_entities)} thực thể: {', '.join(found_entities[:5])}...)."))
    elif len(found_entities) >= 4:
        score += 5.5
        details.append(("GEO-01", 5.5, 8, f"Mật độ thực thể khá ({len(found_entities)} thực thể). Bổ sung thêm thuật ngữ chuyên môn."))
    else:
        score += 2.5
        details.append(("GEO-01", 2.5, 8, f"Mật độ thực thể nghèo nàn ({len(found_entities)} thực thể). Khó để AI Overviews trích dẫn."))

    # 2. Quantitative Data (Số liệu định lượng, %, mg, tuổi)
    stats_matches = re.findall(r'\b\d+([.,]\d+)?\s*(%|mg|ml|cm|tuổi|năm|tháng|lần|g)\b', body, re.IGNORECASE)
    standalone_numbers = re.findall(r'\b\d{2,}\b', body)
    total_stats = len(stats_matches) + len(standalone_numbers)
    
    if total_stats >= 10:
        score += 8
        details.append(("GEO-02", 8, 8, f"Dữ liệu định lượng phong phú ({total_stats} chỉ số/con số thực tế)."))
    elif total_stats >= 5:
        score += 5.5
        details.append(("GEO-02", 5.5, 8, f"Có {total_stats} con số định lượng. Cần thêm hàm lượng, tỷ lệ chính xác."))
    else:
        score += 2
        details.append(("GEO-02", 2, 8, f"Quá ít số liệu định lượng ({total_stats} số). Bài viết còn mang tính định tính."))

    # 3. Markdown Comparison Table
    tables = re.findall(r'\|.*?\n\|[-:\s|]+\|\n(\|.*?\n)+', body)
    if len(tables) >= 1:
        score += 8
        details.append(("GEO-03", 8, 8, f"Có {len(tables)} bảng dữ liệu so sánh Markdown. Điểm cộng xuất sắc cho LLMs parse dữ liệu."))
    else:
        score += 1
        details.append(("GEO-03", 1, 8, "Thiếu bảng so sánh dữ liệu (Markdown table). AI Overviews rất ưu tiên trích xuất bảng."))

    # 4. Authority Citations & Standards
    has_citations = any(kw in lower_body for kw in ["nghiên cứu", "chứng nhận", "bộ y tế", "tiêu chuẩn", "gmp", "nhật bản", "báo cáo"])
    if has_citations:
        score += 6
        details.append(("GEO-04", 6, 6, "Có trích dẫn nguồn uy tín và tiêu chuẩn kiểm định rõ ràng."))
    else:
        score += 1
        details.append(("GEO-04", 1, 6, "Thiếu trích dẫn nguồn uy tín, cơ quan kiểm định hoặc nghiên cứu bảo chứng."))

    return score, details

def audit_brand_voice(body):
    score = 0
    details = []

    # 1. Câu ngắn, gãy gọn (Average Sentence Length)
    sentences = [s.strip() for s in re.split(r'[.!?]\s+', body) if len(s.strip()) > 5]
    if sentences:
        avg_sentence_len = sum(len(s.split()) for s in sentences) / len(sentences)
        if avg_sentence_len <= 22:
            score += 4
            details.append(("BV-01", 4, 4, f"Nhịp điệu câu văn rất tốt (TB {avg_sentence_len:.1f} từ/câu - chuẩn văn phong gãy gọn)."))
        elif avg_sentence_len <= 30:
            score += 2.5
            details.append(("BV-01", 2.5, 4, f"Độ dài câu trung bình hơi dài ({avg_sentence_len:.1f} từ/câu). Nên ngắt bớt câu phức."))
        else:
            score += 1
            details.append(("BV-01", 1, 4, f"Câu văn rườm rà ({avg_sentence_len:.1f} từ/câu). Cần ngắt ngắn câu theo Brand Voice."))
    else:
        score += 2
        details.append(("BV-01", 2, 4, "Chưa đủ dữ liệu câu văn."))

    # 2. Forbidden Fluff Words
    found_forbidden = [w for w in FORBIDDEN_WORDS if w in body.lower()]
    if not found_forbidden:
        score += 4
        details.append(("BV-02", 4, 4, "Không phát hiện từ sáo rỗng hoặc thuật ngữ PR giả tạo (Tuyệt vời)."))
    else:
        penalty = min(4, len(found_forbidden) * 2)
        actual_score = max(0, 4 - penalty)
        score += actual_score
        details.append(("BV-02", actual_score, 4, f"CẢNH BÁO: Phát hiện {len(found_forbidden)} từ cấm Brand Voice: {', '.join(found_forbidden)}."))

    # 3. CTA chân thành
    has_cta = bool(re.search(r'(kêu gọi|hành động|cta|liên hệ|tư vấn|lời khuyên|kết luận|chăm sóc)', body[-600:], re.IGNORECASE))
    if has_cta:
        score += 2
        details.append(("BV-03", 2, 2, "Có phần kết luận và định hướng hành động (CTA) rõ ràng."))
    else:
        score += 0.5
        details.append(("BV-03", 0.5, 2, "Phần kết bài chưa có lời kêu gọi hành động cụ thể."))

    return score, details

def main():
    parser = argparse.ArgumentParser(description="Kiểm toán bài viết blog chuẩn SEO, AEO, GEO trước khi đăng.")
    parser.add_argument("file", help="Đường dẫn tới file markdown bài viết (.md)")
    parser.add_argument("-k", "--keyword", help="Từ khóa chính (Focus Keyword)", default=None)
    parser.add_argument("--json", action="store_true", help="Xuất kết quả dưới định dạng JSON")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ LỖI: Không tìm thấy file tại '{file_path}'", file=sys.stderr)
        sys.exit(2)

    frontmatter, body, content = parse_markdown(file_path)
    focus_kw = args.keyword or frontmatter.get("focus_keyword", "")

    # Thực hiện 4 bài kiểm tra
    seo_score, seo_details, total_words = audit_seo(frontmatter, body, focus_kw)
    aeo_score, aeo_details = audit_aeo(body)
    geo_score, geo_details = audit_geo(body)
    bv_score, bv_details = audit_brand_voice(body)

    total_score = round(seo_score + aeo_score + geo_score + bv_score, 1)

    # Đánh giá chung
    if total_score >= 85:
        verdict = "PASS (ĐẠT CHUẨN XUẤT BẢN)"
        badge = "🟢"
    elif total_score >= 70:
        verdict = "REVISE (CẦN TỐI ƯU TRƯỚC KHI ĐĂNG)"
        badge = "🟡"
    else:
        verdict = "FAIL (CHƯA ĐẠT CHUẨN)"
        badge = "🔴"

    if args.json:
        result = {
            "file": str(file_path),
            "focus_keyword": focus_kw,
            "total_words": total_words,
            "total_score": total_score,
            "verdict": verdict,
            "pillars": {
                "seo": {"score": round(seo_score, 1), "max": 30, "details": seo_details},
                "aeo": {"score": round(aeo_score, 1), "max": 30, "details": aeo_details},
                "geo": {"score": round(geo_score, 1), "max": 30, "details": geo_details},
                "brand_voice": {"score": round(bv_score, 1), "max": 10, "details": bv_details}
            }
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # In báo cáo Terminal trực quan
    print("\n" + "=" * 75)
    print(f"       📊 BÁO CÁO KIỂM ĐỊNH BÀI VIẾT BLOG: SEO - AEO - GEO")
    print("=" * 75)
    print(f"📄 Bài viết:      {file_path.name}")
    print(f"🔑 Từ khóa chính: '{focus_kw if focus_kw else '(Chưa thiết lập)'}'")
    print(f"📝 Tổng số từ:    {total_words} từ")
    print(f"🏆 Tổng điểm:     {total_score}/100 điểm  {badge} {verdict}")
    print("-" * 75)

    print(f"\n1️⃣ TRỤ CỘT SEO TRUYỀN THỐNG ({round(seo_score, 1)}/30 điểm):")
    for code, sc, max_sc, desc in seo_details:
        icon = "✅" if sc == max_sc else ("⚠️" if sc > 0 else "❌")
        print(f"   [{code}] {icon} ({sc}/{max_sc}đ) {desc}")

    print(f"\n2️⃣ TRỤ CỘT AEO - CÔNG CỤ TRẢ LỜI TRỰC TIẾP ({round(aeo_score, 1)}/30 điểm):")
    for code, sc, max_sc, desc in aeo_details:
        icon = "✅" if sc == max_sc else ("⚠️" if sc > 0 else "❌")
        print(f"   [{code}] {icon} ({sc}/{max_sc}đ) {desc}")

    print(f"\n3️⃣ TRỤ CỘT GEO - TRÍCH DẪN NGUỒN AI OVERVIEWS ({round(geo_score, 1)}/30 điểm):")
    for code, sc, max_sc, desc in geo_details:
        icon = "✅" if sc == max_sc else ("⚠️" if sc > 0 else "❌")
        print(f"   [{code}] {icon} ({sc}/{max_sc}đ) {desc}")

    print(f"\n4️⃣ TRỤ CỘT BRAND VOICE & TRẢI NGHIỆM ĐỌC ({round(bv_score, 1)}/10 điểm):")
    for code, sc, max_sc, desc in bv_details:
        icon = "✅" if sc == max_sc else ("⚠️" if sc > 0 else "❌")
        print(f"   [{code}] {icon} ({sc}/{max_sc}đ) {desc}")

    print("\n" + "-" * 75)
    print("📋 HÀNH ĐỘNG KHUYẾN NGHỊ (ACTION ITEMS):")
    action_items = []
    for group in [seo_details, aeo_details, geo_details, bv_details]:
        for code, sc, max_sc, desc in group:
            if sc < max_sc:
                action_items.append(f"- [{code}] {desc}")
    
    if action_items:
        for item in action_items[:5]:  # Top 5 khuyến nghị hàng đầu
            print(f"   👉 {item}")
    else:
        print("   🎉 Bài viết hoàn hảo mọi tiêu chí! Bạn có thể tự tin xuất bản ngay.")
    print("=" * 75 + "\n")

    # Exit code phản ánh kết quả kiểm định
    sys.exit(0 if total_score >= 85 else 1)

if __name__ == "__main__":
    main()
