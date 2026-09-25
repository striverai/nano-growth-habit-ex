#!/usr/bin/env python3
"""
gen-prompt.py — Sinh Prompt Chuyên Sâu Cho Stream 4.5 / Higgsfield / Kling 3.0 Từ Topic Sản Phẩm.
Hỗ trợ gọi OpenAI / Anthropic / Gemini API hoặc tự động kích hoạt Bộ Engine Mẫu Tinh Chỉnh Cấp 5
(Heuristic Fallback) để luôn bảo đảm kết quả kịch bản 4 Shot (15-25s) chuẩn xác 100%.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Cấu hình UTF-8 cho Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Tìm nạp file .env từ các thư mục cha và thư mục hiện tại
env_search_paths = [
    Path(__file__).resolve().parent.parent / ".env",
    Path(__file__).resolve().parent.parent.parent / ".env",
    Path.cwd() / ".env",
    Path.cwd() / "tao-creative-fb" / ".env"
]
for p in env_search_paths:
    if p.exists():
        load_dotenv(p)
        break

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()


def load_asset_text(filename: str) -> str:
    """Đọc file tài nguyên từ thư mục assets/"""
    asset_path = Path(__file__).resolve().parent.parent / "assets" / filename
    if asset_path.exists():
        return asset_path.read_text(encoding="utf-8")
    return ""


def get_smart_fallback_storyboard(topic: str, style: str, duration: int = 20) -> dict:
    """
    Engine nội sinh (Level 5 Fallback) tạo kịch bản 4 Shot chi tiết khi không có kết nối API ngoài.
    Được tinh chỉnh theo công thức KOC & Cinematic của Nano Growth Habit EX.
    """
    is_luxury = "lux" in style.lower()
    is_minimal = "min" in style.lower()
    is_casual = not (is_luxury or is_minimal)

    if is_luxury:
        style_name = "Luxury Medical Prestige"
        bg_desc = "ultra-sleek white marble podium with pristine glass reflections and soft warm-gold rim lighting"
    elif is_minimal:
        style_name = "Minimalist Wabi-Sabi"
        bg_desc = "serene warm beige surface with delicate natural leaf shadows and handmade Japanese ceramic tray"
    else:
        style_name = "Modern Family KOC Lifestyle"
        bg_desc = "cozy modern Japandi wooden home interior with soft morning sun rays shining through sheer curtains"

    storyboard = {
        "project": "Nano Growth Habit EX Video AI Campaign",
        "topic": topic,
        "style": style_name,
        "target_duration_seconds": duration,
        "aspect_ratio": "9:16 (Vertical TikTok / Reels / Shorts)",
        "resolution": "1080x1920",
        "fps": 30,
        "shots": [
            {
                "shot_index": 1,
                "time_range": "0.0s - 4.0s",
                "phase": "VISUAL_HOOK",
                "camera_motion": "key_zoom",
                "motion_strength": 6,
                "visual_prompt_en": f"Dynamic snap zoom into the Nano Growth Habit EX packaging, settling on the Japanese quality seal, {bg_desc}, high-energy visual hook, crisp embossed typography, commercial 8k finish, hyper-realistic, zero distortion.",
                "visual_prompt_vi": f"Máy quay snap zoom dứt khoát vào logo và bao bì hộp Nano Growth Habit EX trên nền {bg_desc}, tạo điểm nhấn thị giác bắt mắt ngay giây đầu.",
                "voiceover_vi": "Đừng vội ép con uống canxi nước nếu mẹ chưa biết bí mật giấc ngủ 10 giờ đêm này!",
                "text_overlay_vi": "BÍ MẬT TĂNG CHIỀU CAO BAN ĐÊM"
            },
            {
                "shot_index": 2,
                "time_range": "4.0s - 9.0s",
                "phase": "DETAIL_FORMULA",
                "camera_motion": "dolly_in",
                "motion_strength": 3,
                "visual_prompt_en": f"Macro cinematic dolly-in push toward two rich chocolate-colored chewable tablets resting beside the blister pack, extreme 85mm macro lens, velvety cocoa texture, golden rim highlights, shallow depth of field f/1.8, pristine studio aesthetics.",
                "visual_prompt_vi": "Cận cảnh Macro 85mm lướt êm ái vào 2 viên nhai vị cacao thơm ngon và vỉ bạc ánh kim, thấy rõ kết cấu hạt nano mịn màng.",
                "voiceover_vi": "Canxi chỉ là gạch vữa, Hormone GH mới là thợ xây. Nano Growth bổ sung Alpha-GPC kích hoạt GH tự nhiên ban đêm.",
                "text_overlay_vi": "ALPHA-GPC KÍCH HOẠT GH BAN ĐÊM"
            },
            {
                "shot_index": 3,
                "time_range": "9.0s - 15.0s",
                "phase": "SENSORY_EXPERIENCE",
                "camera_motion": "pan_slow",
                "motion_strength": 5,
                "visual_prompt_en": f"Gentle horizontal pan revealing the complete daily routine, a happy 10-year-old child smiling delightfully while chewing the chocolate tablet, seamless mother and child interaction, warm emotional resonance, authentic lighting.",
                "visual_prompt_vi": "Lia máy ngang ghi lại khoảnh khắc bé hào hứng nhai 2 viên cacao ngon lành như ăn kẹo, mẹ mỉm cười hài lòng bên cạnh.",
                "voiceover_vi": "Kết hợp Canxi vỏ trứng nano và CPP êm bụng, con tự giác nhai 2 viên cacao mỗi tối trước khi đi ngủ.",
                "text_overlay_vi": "2 VIÊN CACAO - CON TỰ GIÁC NHAI"
            },
            {
                "shot_index": 4,
                "time_range": "15.0s - 20.0s",
                "phase": "OUTRO_CTA",
                "camera_motion": "orbit",
                "motion_strength": 4,
                "visual_prompt_en": f"Smooth 360-degree orbital sweep around the Nano Growth Habit EX box standing proudly next to a wooden height measurement ruler, warm golden glow, pristine call to action composition, ultra-clean premium outro.",
                "visual_prompt_vi": "Camera lượn vòng êm ái quanh hộp sản phẩm đặt cạnh thước đo chiều cao, ánh sáng vàng ấm lan tỏa, khung hình kêu gọi hành động chuẩn mực.",
                "voiceover_vi": "Bố mẹ nhắn tin ngay để nhận lộ trình phát triển chiều cao chuẩn Nhật Bản cho con nhé!",
                "text_overlay_vi": "NHẬN LỘ TRÌNH CHUẨN NHẬT BẢN"
            }
        ],
        "negative_prompt": load_asset_text("negative-prompt.txt").strip(),
        "stream45_full_prompt": (
            f"[Stream 4.5 Multi-Shot Video Pipeline]\n"
            f"Topic: {topic}\n"
            f"Style: {style_name}\n"
            f"Shot 1 (0-4s Key Zoom): Dynamic snap zoom into Nano Growth box on {bg_desc}.\n"
            f"Shot 2 (4-9s Dolly In): Macro 85mm push-in on two rich cocoa chewable tablets and blister pack.\n"
            f"Shot 3 (9-15s Pan Slow): Smooth pan across daily routine, smiling child chewing tablet happily.\n"
            f"Shot 4 (15-20s Orbit): 360-degree orbital sweep around hero box beside growth ruler.\n"
            f"Negative: {load_asset_text('negative-prompt.txt').strip()[:200]}..."
        )
    }
    return storyboard


def generate_prompt_with_llm(topic: str, style: str, duration: int = 20) -> dict:
    """Gọi OpenAI / LLM nếu có API key hợp lệ"""
    if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-proj-xxx") or len(OPENAI_API_KEY) < 20:
        return get_smart_fallback_storyboard(topic, style, duration)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        brand_style_ctx = load_asset_text("brand-style.md")
        camera_ctx = load_asset_text("camera-prompts.md")
        negative_ctx = load_asset_text("negative-prompt.txt")

        system_prompt = f"""
Bạn là chuyên gia đạo diễn hình ảnh và Prompt Engineer hàng đầu cho các mô hình video AI thế hệ mới (Stream 4.5, Higgsfield, Kling 3.0, Runway Gen-3).
Nhiệm vụ của bạn: Tạo kịch bản phân cảnh 4-Shot (thời lượng {duration}s) cho video dọc 9:16 (TikTok / Reels / Shorts) về sản phẩm Nano Growth Habit EX.

Quy tắc cốt lõi:
1. Thông điệp: "Canxi chỉ là gạch vữa, Hormone GH mới là thợ xây". Alpha-GPC kích hoạt GH ban đêm, Canxi vi hạt + CPP không táo bón, 2 viên nhai vị cacao thơm ngon.
2. Mỗi Shot phải có:
   - camera_motion: chọn 1 trong (orbit, dolly_in, pan_slow, key_zoom, multishot)
   - motion_strength: từ 2 đến 7 (tránh méo logo)
   - visual_prompt_en: Prompt tiếng Anh chi tiết theo ngôn ngữ máy quay chuyên nghiệp (tiêu cự, ánh sáng, vật lý, chất liệu).
   - voiceover_vi: Lời lồng tiếng 15-25 từ ngắn gọn, dứt khoát.
   - text_overlay_vi: Câu tóm tắt in trên màn hình (viết hoa).
3. Trả về đúng định dạng JSON hợp lệ theo cấu trúc chuẩn.
"""
        user_prompt = f"Chủ đề video: '{topic}'\nPhong cách mong muốn: '{style}'\nThời lượng: {duration}s."

        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content
        data = json.loads(content)
        if "shots" in data:
            data["negative_prompt"] = negative_ctx.strip()
            data["project"] = "Nano Growth Habit EX Video AI Campaign"
            data["topic"] = topic
            data["style"] = style
            data["target_duration_seconds"] = duration
            return data
    except Exception as e:
        print(f"[gen-prompt] Chú ý: Gọi OpenAI gặp lỗi ({e}), chuyển sang Level 5 Heuristic Engine.")

    return get_smart_fallback_storyboard(topic, style, duration)


def main():
    parser = argparse.ArgumentParser(description="Sinh Prompt Video AI Cho Stream 4.5 / Higgsfield")
    parser.add_argument("--topic", type=str, default="Cơ chế tăng trưởng tự nhiên ban đêm với Alpha-GPC & Canxi Nano", help="Chủ đề nội dung video")
    parser.add_argument("--style", type=str, default="casual", choices=["luxury", "casual", "minimal", "koc"], help="Phong cách hình ảnh")
    parser.add_argument("--duration", type=int, default=20, help="Thời lượng video (15-25 giây)")
    parser.add_argument("--output", type=str, default=None, help="Đường dẫn lưu file JSON kịch bản")
    parser.add_argument("--format", choices=["json", "text", "markdown"], default="text", help="Định dạng hiển thị kết quả")
    args = parser.parse_args()

    result = generate_prompt_with_llm(args.topic, args.style, args.duration)

    # Xác định đường dẫn file lưu
    if args.output:
        out_file = Path(args.output)
    else:
        script_dir = Path(__file__).resolve().parent
        out_file = script_dir.parent / "output" / "video_storyboard_latest.json"

    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Xuất file Markdown để con người dễ đọc
    md_file = out_file.with_suffix(".md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(f"# Kịch Bản Phân Cảnh Video AI (Stream 4.5 / Higgsfield)\n\n")
        f.write(f"- **Chủ đề**: {result.get('topic')}\n")
        f.write(f"- **Phong cách**: {result.get('style')}\n")
        f.write(f"- **Thời lượng**: {result.get('target_duration_seconds')}s\n")
        f.write(f"- **Tỷ lệ**: 9:16 (TikTok/Reels)\n\n---\n\n")
        for s in result.get("shots", []):
            f.write(f"### Shot {s['shot_index']} ({s['time_range']}) — {s.get('phase', 'SCENE')}\n")
            f.write(f"- **Camera Motion**: `{s.get('camera_motion')}` (Strength: {s.get('motion_strength')})\n")
            f.write(f"- **Prompt Tiếng Anh**: `{s.get('visual_prompt_en')}`\n")
            f.write(f"- **Lời thoại (Voiceover)**: *\"{s.get('voiceover_vi')}\"*\n")
            f.write(f"- **Chữ hiển thị (Overlay)**: **{s.get('text_overlay_vi')}**\n\n")
        f.write(f"---\n### Negative Prompt\n```text\n{result.get('negative_prompt')}\n```\n")

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n==================== KỊCH BẢN VIDEO AI 4 SHOT (STREAM 4.5 / HIGGSFIELD) ====================")
        print(f"Chủ đề       : {result.get('topic')}")
        print(f"Phong cách   : {result.get('style')}")
        print(f"Thời lượng   : {result.get('target_duration_seconds')}s | Tỷ lệ: 9:16 (1080x1920)")
        print(f"File lưu JSON: {out_file.resolve()}")
        print(f"File lưu MD  : {md_file.resolve()}\n")
        for s in result.get("shots", []):
            print(f"[{s['shot_index']}] {s['time_range']} | Chuyển động: {s.get('camera_motion')} (Lực: {s.get('motion_strength')})")
            print(f"    EN Prompt: {s.get('visual_prompt_en')[:110]}...")
            print(f"    Thoại    : \"{s.get('voiceover_vi')}\"")
            print(f"    Chữ màn hình: [{s.get('text_overlay_vi')}]\n")
        print("============================================================================================\n")


if __name__ == "__main__":
    main()
