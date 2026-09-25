#!/usr/bin/env python3
"""
list-images.py — Quét, phân tích và lập chỉ mục toàn bộ ảnh sản phẩm trong thư mục product-photos/
Hỗ trợ đọc kích thước, tỷ lệ khung hình (Aspect Ratio), dung lượng, và tự động phân loại vai trò
ảnh (Hero Box, Blister Pack, Detail Label, Texture) phục vụ nạp vào Pipeline Video AI.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from PIL import Image

# Cấu hình UTF-8 cho Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def detect_aspect_ratio(w: int, h: int) -> str:
    """Xác định tỷ lệ khung hình gần đúng"""
    ratio = w / h if h > 0 else 1.0
    if 0.95 <= ratio <= 1.05:
        return "1:1 (Square)"
    elif 0.53 <= ratio <= 0.60:
        return "9:16 (Vertical TikTok/Reels)"
    elif 1.70 <= ratio <= 1.82:
        return "16:9 (Landscape HD)"
    elif 0.70 <= ratio <= 0.80:
        return "3:4 (Portrait)"
    elif 1.30 <= ratio <= 1.38:
        return "4:3 (Standard)"
    else:
        return f"{w}:{h} ({ratio:.2f})"


def guess_image_role(filename: str, width: int, height: int) -> str:
    """Tự động đoán vai trò ảnh dựa trên tên file và tỷ lệ"""
    fn_lower = filename.lower()
    if any(k in fn_lower for k in ["hero", "box", "hop", "chinh", "front"]):
        return "Hero Packaging (Bao bì chính diện)"
    elif any(k in fn_lower for k in ["blister", "vi", "pack", "tray"]):
        return "Blister Pack (Vỉ sản phẩm kim loại)"
    elif any(k in fn_lower for k in ["tablet", "vien", "keo", "cacao", "texture"]):
        return "Tablet Texture (Chi tiết viên nhai cacao)"
    elif any(k in fn_lower for k in ["label", "nhan", "thanhphan", "ingredient"]):
        return "Detail Label (Cận cảnh nhãn & thành phần)"
    elif any(k in fn_lower for k in ["lifestyle", "koc", "be", "me"]):
        return "Lifestyle Context (Đời sống KOC)"
    else:
        # Phân loại mặc định theo tỷ lệ
        ratio = width / height if height > 0 else 1.0
        if ratio < 0.8:
            return "Vertical Product Hero"
        elif ratio > 1.2:
            return "Wide Commercial Staging"
        else:
            return "Standard Showcase Item"


def scan_product_photos(photos_dir: Path) -> list:
    """Quét tất cả các file ảnh hợp lệ trong thư mục"""
    valid_extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}
    results = []

    if not photos_dir.exists():
        return results

    files = sorted(list(photos_dir.iterdir()))
    for idx, f in enumerate(files, 1):
        if f.is_file() and f.suffix.lower() in valid_extensions:
            try:
                with Image.open(f) as img:
                    w, h = img.size
                    fmt = img.format
                
                size_mb = f.stat().st_size / (1024 * 1024)
                aspect = detect_aspect_ratio(w, h)
                role = guess_image_role(f.name, w, h)

                results.append({
                    "id": idx,
                    "filename": f.name,
                    "filepath": str(f.resolve()),
                    "relative_path": str(f),
                    "width": w,
                    "height": h,
                    "aspect_ratio": aspect,
                    "format": fmt,
                    "size_mb": round(size_mb, 2),
                    "suggested_role": role,
                    "suitable_for_stream45": (w >= 768 and h >= 768)
                })
            except Exception as e:
                # Bỏ qua file lỗi không mở được bằng PIL
                continue

    return results


def main():
    parser = argparse.ArgumentParser(description="Quét và phân tích danh sách ảnh sản phẩm cho Video AI")
    parser.add_argument("--dir", type=str, default=None, help="Đường dẫn thư mục chứa ảnh (mặc định product-photos/)")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả định dạng JSON thuần")
    parser.add_argument("--output", type=str, default=None, help="Ghi kết quả ra file JSON")
    args = parser.parse_args()

    # Tìm thư mục ảnh
    if args.dir:
        photos_dir = Path(args.dir)
    else:
        # Thử các đường dẫn mặc định
        script_dir = Path(__file__).resolve().parent
        skill_dir = script_dir.parent
        possible_dirs = [
            skill_dir / "product-photos",
            skill_dir.parent / "Ảnh sản phẩm",
            Path.cwd() / "product-photos",
            Path.cwd() / "skills" / "tao-video-ai" / "product-photos"
        ]
        photos_dir = next((d for d in possible_dirs if d.exists()), skill_dir / "product-photos")

    images = scan_product_photos(photos_dir)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(images, f, ensure_ascii=False, indent=2)

    if args.json:
        print(json.dumps(images, ensure_ascii=False, indent=2))
    else:
        print(f"\n==================== DANH SÁCH ẢNH SẢN PHẨM ({len(images)} ẢNH) ====================")
        print(f"Thư mục quét: {photos_dir.resolve()}\n")
        if not images:
            print("(!) Không tìm thấy ảnh sản phẩm hợp lệ trong thư mục.")
            print("    Vui lòng thêm ảnh (.png, .jpg, .webp) vào thư mục: " + str(photos_dir))
        else:
            print(f"{'ID':<4} | {'Tên File':<25} | {'Kích thước':<12} | {'Tỷ lệ':<16} | {'Dung lượng':<10} | {'Vai Trò Gợi Ý'}")
            print("-" * 105)
            for img in images:
                dims = f"{img['width']}x{img['height']}"
                size = f"{img['size_mb']} MB"
                print(f"{img['id']:<4} | {img['filename'][:25]:<25} | {dims:<12} | {img['aspect_ratio'][:16]:<16} | {size:<10} | {img['suggested_role']}")
        print("========================================================================\n")


if __name__ == "__main__":
    main()
