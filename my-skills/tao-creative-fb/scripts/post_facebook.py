#!/usr/bin/env python3
"""
post_facebook.py — Đăng đồng thời CẢ ẢNH VÀ CAPTION lên Facebook Page qua Graph API.
Endpoint: https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos
Hỗ trợ upload ảnh từ URL hoặc từ file local, tự động bắt lỗi chi tiết từ Meta Graph API
và hỗ trợ chế độ kiểm thử DRY_RUN an toàn.
"""

import os
import sys
import json
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

FB_PAGE_ID = os.getenv("FB_PAGE_ID", "").strip()
FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN", "").strip()
DRY_RUN = os.getenv("DRY_RUN", "false").lower() in ("true", "1", "yes")


def post_to_facebook(image_path_or_url: str, caption_text: str, dry_run: bool = False) -> dict:
    """
    Đăng ảnh và caption cùng lúc lên Facebook Page.
    - image_path_or_url: Đường dẫn file ảnh local hoặc URL ảnh online.
    - caption_text: Nội dung văn bản đính kèm ảnh.
    - dry_run: Nếu True, không gọi Facebook API mà chỉ mô phỏng và lưu log.
    """
    is_dry = dry_run or DRY_RUN or not FB_PAGE_ID or not FB_PAGE_TOKEN or FB_PAGE_TOKEN.startswith("EAAxxx")

    if is_dry:
        print("\n==================== [FB POST - DRY RUN MODE] ====================")
        print(f"📌 Chế độ: GIẢ LẬP ĐĂNG BÀI (Không gửi API thực tế tới Facebook)")
        print(f"🆔 Page ID: {FB_PAGE_ID or '[Chưa cấu hình / Demo Page]'}")
        print(f"🖼️ Ảnh đính kèm: {image_path_or_url}")
        print(f"📝 Caption bài đăng ({len(caption_text.split())} từ):")
        print("------------------------------------------------------------------")
        print(caption_text.strip())
        print("------------------------------------------------------------------")
        
        # Ghi log lưu trữ cục bộ
        log_dir = Path("output")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "published_history_dryrun.jsonl"
        mock_result = {
            "status": "success_simulated",
            "dry_run": True,
            "id": "mock_photo_100293847561029",
            "post_id": f"{FB_PAGE_ID or '123456789'}_100293847561029",
            "image": str(image_path_or_url),
            "caption_preview": caption_text[:100] + "..."
        }
        with open(log_file, "a", encoding="utf-8") as lf:
            lf.write(json.dumps(mock_result, ensure_ascii=False) + "\n")
        
        print(f"✅ [GIẢ LẬP THÀNH CÔNG] Đã ghi nhận bài đăng vào: {log_file}")
        print("==================================================================\n")
        return mock_result

    # GỌI FACEBOOK GRAPH API THẬT
    api_url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos"
    print(f"[Facebook API] Đang kết nối tới endpoint: {api_url}...")

    payload = {
        "caption": caption_text,
        "access_token": FB_PAGE_TOKEN
    }

    try:
        if image_path_or_url.startswith("http://") or image_path_or_url.startswith("https://"):
            # Ảnh là URL trực tuyến
            payload["url"] = image_path_or_url
            response = requests.post(api_url, data=payload, timeout=60)
        else:
            # Ảnh là file local trên ổ cứng
            local_img = Path(image_path_or_url)
            if not local_img.exists():
                raise FileNotFoundError(f"Không tìm thấy file ảnh tại đường dẫn: {image_path_or_url}")
            
            with open(local_img, "rb") as img_file:
                files = {"source": img_file}
                response = requests.post(api_url, data=payload, files=files, timeout=60)

        res_data = response.json()

        if response.status_code == 200 and "id" in res_data:
            photo_id = res_data.get("id")
            post_id = res_data.get("post_id", f"{FB_PAGE_ID}_{photo_id}")
            print(f"🎉 [ĐĂNG BÀI THÀNH CÔNG!] Photo ID: {photo_id} | Post ID: {post_id}")
            print(f"🔗 Xem bài đăng: https://facebook.com/{post_id}")
            return {"status": "success", "id": photo_id, "post_id": post_id}
        else:
            # Xử lý lỗi trả về từ Graph API
            err = res_data.get("error", {})
            err_msg = err.get("message", "Lỗi không xác định từ Facebook API")
            err_code = err.get("code", "N/A")
            err_type = err.get("type", "N/A")
            print(f"\n❌ [LỖI FACEBOOK GRAPH API] Code: {err_code} ({err_type})", file=sys.stderr)
            print(f"Chi tiết: {err_msg}", file=sys.stderr)
            raise RuntimeError(f"Facebook Graph API Error ({err_code}): {err_msg}")

    except Exception as e:
        print(f"\n❌ [LỖI NGOẠI LỆ KHI ĐĂNG BÀI]: {e}", file=sys.stderr)
        raise e


def main():
    parser = argparse.ArgumentParser(description="Đăng ảnh và caption đồng thời lên Facebook Page qua Graph API")
    parser.add_argument("--image", type=str, required=True, help="Đường dẫn file ảnh local hoặc URL ảnh")
    parser.add_argument("--caption", type=str, default="", help="Đường dẫn tới file chứa caption text")
    parser.add_argument("--caption-text", type=str, default="", help="Chuỗi văn bản caption trực tiếp")
    parser.add_argument("--dry-run", action="store_true", help="Bật chế độ chạy thử nghiệm giả lập")
    args = parser.parse_args()

    # Xác định nội dung caption
    caption_content = ""
    if args.caption_text:
        caption_content = args.caption_text
    elif args.caption:
        cap_file = Path(args.caption)
        if cap_file.exists():
            with open(cap_file, "r", encoding="utf-8") as f:
                caption_content = f.read()
        else:
            print(f"Lỗi: Không tìm thấy file caption tại {args.caption}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Lỗi: Bắt buộc phải cung cấp --caption (file) hoặc --caption-text (chuỗi)", file=sys.stderr)
        sys.exit(1)

    try:
        result = post_to_facebook(
            image_path_or_url=args.image,
            caption_text=caption_content,
            dry_run=args.dry_run
        )
        print(f"RESULT={json.dumps(result)}")
    except Exception as err:
        print(f"FATAL ERROR: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
