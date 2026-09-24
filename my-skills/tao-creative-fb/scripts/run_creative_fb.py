#!/usr/bin/env python3
"""
run_creative_fb.py — Điều phối toàn bộ luồng của skill tao-creative-fb:
- Mode 1: Content Free (Organic Facebook Page: 3 ý tưởng -> chọn -> gen ảnh + caption -> preview -> post)
- Mode 2: Creative Ads (3 bộ ghép cặp Ảnh Ads + Ad Copy cho 3 angles: Pain Point, Solution, Social Proof)
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Cấu hình UTF-8 cho Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Đảm bảo import được các module trong cùng thư mục scripts
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from gen_image import generate_image
from gen_caption import generate_caption
from post_facebook import post_to_facebook

# Danh sách 3 ý tưởng chuẩn cho Mode 1
ORGANIC_IDEAS = [
    {
        "id": 1,
        "title": "Bác bỏ ngộ nhận: Canxi là gạch vữa, Hormone GH mới là thợ xây",
        "angle": "Khoa học tăng chiều cao & vai trò kích hoạt tuyến yên ban đêm",
        "prompt_template": "A warm and cozy Japanese-style modern bedroom setting at night. A happy 10-year-old Asian child in comfortable pajamas smiling cheerfully, holding two delicious dark chocolate-flavored chewable tablets in their hand before going to sleep. On the bedside wooden table, a sleek minimalist bottle of Japanese health supplement and a glass of warm water. Soft warm golden lighting, realistic photography, authentic family moment, 1024x1024 square composition, 8k resolution, shot on 50mm lens.",
        "caption_key": "idea_1"
    },
    {
        "id": 2,
        "title": "Chấm dứt cuộc chiến ép con nuốt thuốc: 2 viên nhai cacao con tự giác",
        "angle": "Đồng cảm nỗi khổ cha mẹ & trải nghiệm nhai socola ngon miệng",
        "prompt_template": "Macro commercial product shot of two rich cocoa-scented chewable calcium tablets resting on an artisan handcrafted Japanese ceramic dish. Fresh natural ingredients and cocoa beans in soft background. Clean white and warm beige aesthetic, photorealistic, 1024x1024.",
        "caption_key": "idea_2"
    },
    {
        "id": 3,
        "title": "Bí quyết canxi chuẩn Nhật không nóng trong, không lo táo bón",
        "angle": "Cơ chế bột canxi vỏ trứng hữu cơ kết hợp CPP hòa tan tối đa",
        "prompt_template": "Candid documentary photography of an Asian mother joyfully measuring her 12-year-old son's height against a clean wooden wall with marked height notches. Bright soft natural morning sunlight streaming through the window, clean minimalist Japanese home interior, 1024x1024.",
        "caption_key": "idea_3"
    }
]

# Cấu hình 3 bộ cho Mode 2
ADS_ANGLES = [
    {
        "set_num": 1,
        "angle": "pain_point",
        "name": "BỘ 1 — ANGLE PAIN POINT (Nỗi đau con thấp còi & Lỡ tuổi vàng)",
        "prompt": "Emotional, dramatic portrait of a 13-year-old Asian teenager standing slightly hesitant beside a classroom growth chart, looking thoughtfully at the height marks. Soft cinematic lighting with deep shadows highlighting introspection. Significant clean negative empty space occupying the upper 35% of the frame for advertising text overlay. Ultra-realistic commercial photography, 1024x1024.",
        "quality": "medium"
    },
    {
        "set_num": 2,
        "angle": "solution",
        "name": "BỘ 2 — ANGLE SOLUTION (Đột phá Alpha-GPC kích hoạt Hormone GH)",
        "prompt": "Premium commercial hero shot of the Japanese dietary supplement bottle 'Nano Growth Habit EX' with elegant minimalist typography, positioned on a sleek dark slate pedestal. Dynamic subtle glowing golden energy rings symbolizing deep sleep night-time GH growth hormone activation. Beside the bottle are two appetizing chocolate chewable tablets. Clean negative space on the left 30% for headline text. Cinematic lighting, luxury aesthetic, photorealistic 8k, 1024x1024.",
        "quality": "medium"
    },
    {
        "set_num": 3,
        "angle": "social_proof",
        "name": "BỘ 3 — ANGLE SOCIAL PROOF (Bằng chứng thực tế mẹ và con bứt phá)",
        "prompt": "High-energy, joyful lifestyle photo of a modern Vietnamese mother and her tall 14-year-old daughter giving a high-five in front of their living room height chart showing significant vertical growth marks. Both radiate genuine happiness, health, and confidence. Clean bright composition, natural interior, ample negative space at the top third for promotional banner. Award-winning commercial photography, 1024x1024.",
        "quality": "medium"
    }
]


def execute_mode_2_ads(output_dir: str = "output/creative_ads") -> list:
    """
    MODE 2: Sản xuất đồng thời 3 BỘ CREATIVE ADS (Ảnh Ads + Ad Copy ghép cặp).
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    results = []

    print("\n" + "="*80)
    print("🚀 BẮT ĐẦU SẢN XUẤT 3 BỘ CREATIVE ADS (MODE 2 - THỦ CÔNG CHO ADS MANAGER)")
    print("="*80 + "\n")

    for item in ADS_ANGLES:
        set_idx = item["set_num"]
        angle_name = item["angle"]
        set_title = item["name"]

        print(f"▶ ĐANG XỬ LÝ: {set_title}")
        print(f"   [1/2] Đang tạo Ảnh Ads (Quality: {item['quality']}, 1024x1024, chừa khoảng trống cho Text Overlay)...")
        img_file = out_path / f"ad_set_{set_idx}_{angle_name}.png"
        img_result = generate_image(
            prompt=item["prompt"],
            quality=item["quality"],
            size="1024x1024",
            output_file=str(img_file)
        )

        print(f"   [2/2] Đang viết Ad Copy chuyển đổi cao (~80-150 từ, Hook mạnh + USP + Hard CTA)...")
        copy_file = out_path / f"ad_set_{set_idx}_{angle_name}.txt"
        copy_result = generate_caption(
            mode="ads",
            angle=angle_name
        )
        with open(copy_file, "w", encoding="utf-8") as f:
            f.write(copy_result)

        bundle = {
            "set_number": set_idx,
            "title": set_title,
            "angle": angle_name,
            "image_path": str(img_file),
            "ad_copy": copy_result,
            "ad_copy_file": str(copy_file)
        }
        results.append(bundle)

        print(f"   ✅ Hoàn thành {set_title}!")
        print("-" * 70)

    # Xuất báo cáo tổng hợp 3 bộ
    print("\n" + "="*80)
    print("🎉 HOÀN THÀNH SẢN XUẤT ĐỦ 3 BỘ CREATIVE ADS GHÉP CẶP:")
    print("="*80)
    for b in results:
        print(f"\n📦 {b['title']}")
        print(f"🖼️ Ảnh Ads: {b['image_path']}")
        print(f"📝 Ad Copy ({len(b['ad_copy'].split())} từ):")
        print("--- [BẮT ĐẦU COPY] ---")
        print(b["ad_copy"])
        print("--- [KẾT THÚC COPY] ---\n")

    return results


def execute_mode_1_organic(chosen_idea_id: int = 1, dry_run: bool = True, output_dir: str = "output/organic_post") -> dict:
    """
    MODE 1: Content Free cho Fanpage.
    Bước A: Hiển thị 3 ý tưởng
    Bước B: Gen Full content cho ý tưởng đã chọn (1 ảnh low + 1 caption 80-150 từ)
    Bước C: Hiển thị preview
    Bước D: Post lên Facebook qua /{page-id}/photos
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*80)
    print("📌 BƯỚC A: DANH SÁCH 3 Ý TƯỞNG CONTENT ORGANIC HÀNG NGÀY")
    print("="*80)
    for idea in ORGANIC_IDEAS:
        marker = "👉 [ĐƯỢC CHỌN]" if idea["id"] == chosen_idea_id else "  "
        print(f"{marker} Ý tưởng {idea['id']}: {idea['title']}")
        print(f"      Góc tiếp cận: {idea['angle']}")

    # Lấy ý tưởng được chọn
    selected_idea = next((item for item in ORGANIC_IDEAS if item["id"] == chosen_idea_id), ORGANIC_IDEAS[0])
    print(f"\n⚡ BƯỚC B: TIẾN HÀNH SINH FULL CONTENT CHO Ý TƯỞNG {selected_idea['id']}...")
    
    # 1. Sinh ảnh
    print("   [1/2] Đang tạo ảnh minh họa 1024x1024 (Model: gpt-image-1, Quality: low)...")
    img_path = out_path / f"post_organic_idea_{selected_idea['id']}.png"
    img_res = generate_image(
        prompt=selected_idea["prompt_template"],
        quality="low",
        size="1024x1024",
        output_file=str(img_path)
    )

    # 2. Sinh caption
    print("   [2/2] Đang viết caption brand voice (~80-150 từ, Hook + Body + Soft CTA)...")
    caption_path = out_path / f"post_organic_idea_{selected_idea['id']}.txt"
    caption_text = generate_caption(
        mode="organic",
        topic=selected_idea["caption_key"]
    )
    with open(caption_path, "w", encoding="utf-8") as f:
        f.write(caption_text)

    # Bước C: Preview
    print("\n" + "="*80)
    print("👁️ BƯỚC C: PREVIEW NỘI DUNG BÀI ĐĂNG (ẢNH + CAPTION ĐI KÈM NHAU)")
    print("="*80)
    print(f"🖼️ File Ảnh: {img_path}")
    print(f"📝 Caption bài đăng ({len(caption_text.split())} từ):")
    print("------------------------------------------------------------------")
    print(caption_text)
    print("------------------------------------------------------------------")

    # Bước D: Xuất bản lên FB
    print("\n🚀 BƯỚC D: XUẤT BẢN LÊN FACEBOOK FANPAGE (ĐỒNG THỜI CẢ ẢNH VÀ CAPTION)...")
    fb_res = post_to_facebook(
        image_path_or_url=str(img_path),
        caption_text=caption_text,
        dry_run=dry_run
    )

    return {
        "idea": selected_idea,
        "image_file": str(img_path),
        "caption_file": str(caption_path),
        "caption_text": caption_text,
        "facebook_response": fb_res
    }


def main():
    parser = argparse.ArgumentParser(description="Điều phối tạo content Facebook cho Nano Growth Habit EX")
    parser.add_argument("--mode", type=str, default="ads", choices=["organic", "ads"], help="Chế độ chạy: organic (Mode 1) hoặc ads (Mode 2)")
    parser.add_argument("--idea", type=int, default=1, choices=[1, 2, 3], help="ID ý tưởng cho Mode 1 (1, 2, hoặc 3)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Chạy ở chế độ kiểm thử giả lập")
    args = parser.parse_args()

    if args.mode == "ads":
        execute_mode_2_ads()
    else:
        execute_mode_1_organic(chosen_idea_id=args.idea, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
