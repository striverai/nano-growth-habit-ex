#!/usr/bin/env python3
"""
gen_image.py — Sinh ảnh cho Facebook Post / Ads qua OpenAI Image API.
Hỗ trợ model gpt-image-1, chất lượng low/medium, kích thước 1024x1024.
Có cơ chế retry 1 lần khi lỗi và hỗ trợ DRY_RUN.
"""

import os
import sys
import time
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

# Cấu hình UTF-8 cho Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Tải cấu hình từ .env
env_paths = [
    Path(__file__).parent / ".env",
    Path(__file__).parent.parent / ".env",
    Path.cwd() / ".env",
    Path.cwd() / "my-skills" / "tao-creative-fb" / ".env"
]
for ep in env_paths:
    if ep.exists():
        load_dotenv(ep)
        break

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DRY_RUN = os.getenv("DRY_RUN", "false").lower() in ("true", "1", "yes")


def create_placeholder_image(output_path: Path, prompt_text: str):
    """Tạo file ảnh mockup quảng cáo 1024x1024 thực tế, chất lượng cao bằng Pillow khi DRY_RUN."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    from PIL import Image, ImageDraw, ImageFont, ImageFilter

    # Khởi tạo canvas 1024x1024
    width, height = 1024, 1024
    
    # Xác định theme màu dựa trên tên file hoặc prompt
    prompt_lower = prompt_text.lower()
    if "pain" in str(output_path).lower() or "dramatic" in prompt_lower or "pain" in prompt_lower:
        bg_top = (30, 25, 45)
        bg_bottom = (15, 12, 22)
        badge_bg = (218, 41, 28)
        headline = "ĐỪNG ĐỂ CON LỠ MẤT 2 NĂM TUỔI VÀNG!"
        subhead = "Canxi chỉ là gạch vữa — Hormone GH mới là thợ xây"
        tag = "CẢNH BÁO TĂNG TRƯỞNG"
        angle_label = "BỘ 1 — ANGLE PAIN POINT"
    elif "solution" in str(output_path).lower() or "solution" in prompt_lower:
        bg_top = (11, 25, 44)
        bg_bottom = (19, 75, 112)
        badge_bg = (255, 152, 0)
        headline = "ĐỘT PHÁ TĂNG CHIỀU CAO CHUẨN NHẬT"
        subhead = "Đánh thức Hormone GH ban đêm với 2 viên nhai cacao"
        tag = "CÔNG NGHỆ ALPHA-GPC"
        angle_label = "BỘ 2 — ANGLE SOLUTION"
    else:
        bg_top = (15, 62, 55)
        bg_bottom = (8, 32, 28)
        badge_bg = (76, 175, 80)
        headline = "HƠN 1.200 PHỤ HUYNH TIN CHỌN"
        subhead = "Con tự giác nhai mỗi tối — Cao lớn vững vàng"
        tag = "HIỆU QUẢ THỰC TẾ"
        angle_label = "BỘ 3 — ANGLE SOCIAL PROOF"

    # Tạo gradient background
    base_img = Image.new("RGB", (width, height), bg_top)
    draw = ImageDraw.Draw(base_img)
    for y in range(height):
        r = int(bg_top[0] + (bg_bottom[0] - bg_top[0]) * (y / height))
        g = int(bg_top[1] + (bg_bottom[1] - bg_top[1]) * (y / height))
        b = int(bg_top[2] + (bg_bottom[2] - bg_top[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Ghép ảnh sản phẩm nếu có trong thư mục 'Ảnh sản phẩm'
    prod_candidates = [
        Path("Ảnh sản phẩm/2026.04.16 GH 5.png"),
        Path("Ảnh sản phẩm/2026.04.17 GH 6.png"),
        Path("../../Ảnh sản phẩm/2026.04.16 GH 5.png"),
        Path("../Ảnh sản phẩm/2026.04.16 GH 5.png")
    ]
    hero_path = None
    for p in prod_candidates:
        if p.exists():
            hero_path = p
            break

    if hero_path:
        try:
            prod_img = Image.open(hero_path).convert("RGBA")
            # Resize cân đối vào giữa khung hình
            target_w = 540
            aspect = prod_img.height / prod_img.width
            target_h = int(target_w * aspect)
            prod_resized = prod_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            # Dán sản phẩm vào giữa
            offset_x = (width - target_w) // 2
            offset_y = height - target_h - 110
            base_img.paste(prod_resized, (offset_x, offset_y), prod_resized)
        except Exception:
            pass

    # Vẽ thông điệp và typography quảng cáo
    draw = ImageDraw.Draw(base_img)
    font_path = "C:/Windows/Fonts/arial.ttf"
    try:
        font_tag = ImageFont.truetype(font_path, 22)
        font_head = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 40)
        font_sub = ImageFont.truetype(font_path, 26)
        font_badge = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 24)
        font_footer = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
    except Exception:
        font_tag = font_head = font_sub = font_badge = font_footer = ImageFont.load_default()

    # 1. Tag trên cùng
    draw.rectangle([(60, 45), (420, 90)], fill=badge_bg)
    draw.text((80, 53), tag, font=font_tag, fill=(255, 255, 255))

    # 2. Headline chính
    draw.text((60, 110), headline, font=font_head, fill=(255, 255, 255))

    # 3. Subhead
    draw.text((60, 175), subhead, font=font_sub, fill=(240, 240, 240))

    # 4. Badges cam kết bên góc
    badges = [
        "✓ 100% Chuẩn Nhật Bản",
        "✓ Canxi Vỏ Trứng + CPP (Êm bụng)",
        "✓ 2 Viên Nhai Vị Cacao Thơm Ngon",
        "✓ Tiết Kiệm: ~20k/ngày"
    ]
    by = 240
    for b in badges:
        draw.rectangle([(60, by), (460, by + 42)], fill=(0, 0, 0, 160))
        draw.text((75, by + 8), b, font=font_badge, fill=(255, 220, 100))
        by += 52

    # 5. Thanh Footer CTA
    draw.rectangle([(0, height - 90), (width, height)], fill=(218, 41, 28))
    draw.text((width // 2 - 290, height - 60), "👉 MUA 2 TẶNG 1 — TƯ VẤN 1-1 MIỄN PHÍ CÙNG DƯỢC SĨ", font=font_footer, fill=(255, 255, 255))

    base_img.save(output_path, "PNG", quality=95)
    print(f"[ĐÃ TẠO ẢNH CREATIVE 1024x1024] Lưu tại: {output_path} ({angle_label})")
    return str(output_path)


def generate_image(prompt: str, quality: str = "low", size: str = "1024x1024", output_file: str = "output/image.png") -> str:
    """
    Gọi OpenAI Image API để sinh ảnh.
    - Model: gpt-image-1 (hoặc dall-e-3 fallback nếu gpt-image-1 chưa hỗ trợ trên tài khoản)
    - Quality: low (Mode 1 - Content Free) hoặc medium (Mode 2 - Creative Ads)
    - Retry: Thử lại 1 lần nếu gặp lỗi kết nối/API.
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if DRY_RUN or not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-proj-xxx"):
        print(f"[THÔNG BÁO] DRY_RUN={DRY_RUN} hoặc chưa cấu hình OPENAI_API_KEY thật.")
        return create_placeholder_image(output_path, prompt)

    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Đảm bảo model gpt-image-1, fallback sang dall-e-3 nếu cần
    models_to_try = ["gpt-image-1", "dall-e-3"]
    max_retries = 2

    for attempt in range(1, max_retries + 1):
        for model_name in models_to_try:
            try:
                print(f"[OpenAI Image] Đang sinh ảnh với model={model_name}, quality={quality}, lần thử {attempt}...")
                
                # Tham số cho gpt-image-1 / dall-e-3
                kwargs = {
                    "model": model_name,
                    "prompt": prompt,
                    "n": 1,
                    "size": size,
                }
                # Quality chuẩn của API
                if quality in ["low", "standard"]:
                    kwargs["quality"] = "standard" if model_name == "dall-e-3" else quality
                elif quality in ["medium", "hd"]:
                    kwargs["quality"] = "hd" if model_name == "dall-e-3" else quality

                response = client.images.generate(**kwargs)
                image_url = response.data[0].url

                # Tải ảnh về lưu vào output_path
                img_res = requests.get(image_url, timeout=30)
                if img_res.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(img_res.content)
                    print(f"[THÀNH CÔNG] Đã lưu ảnh về: {output_path}")
                    return str(output_path)
                else:
                    raise Exception(f"Lỗi tải ảnh từ URL: HTTP {img_res.status_code}")

            except Exception as e:
                print(f"[CẢNH BÁO] Model {model_name} thất bại (Lần {attempt}): {e}")
                if model_name == models_to_try[-1] and attempt < max_retries:
                    print("[RETRY] Đang chờ 3 giây để thử lại lần 2...")
                    time.sleep(3)
                elif model_name == models_to_try[-1] and attempt == max_retries:
                    print(f"[LỖI] Đã thử lại 1 lần nhưng vẫn thất bại hoàn toàn: {e}")
                    raise e


def main():
    parser = argparse.ArgumentParser(description="Sinh ảnh bằng OpenAI Image API cho Facebook")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt mô tả hình ảnh cần sinh")
    parser.add_argument("--quality", type=str, default="low", choices=["low", "medium", "standard", "hd"], help="Chất lượng ảnh")
    parser.add_argument("--size", type=str, default="1024x1024", help="Kích thước ảnh")
    parser.add_argument("--output", type=str, default="output/fb_image.png", help="Đường dẫn file lưu ảnh")
    args = parser.parse_args()

    try:
        saved_path = generate_image(
            prompt=args.prompt,
            quality=args.quality,
            size=args.size,
            output_file=args.output
        )
        print(f"IMAGE_PATH={saved_path}")
    except Exception as err:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
