#!/usr/bin/env python3
"""
get_weekly_video_topic.py — Đọc kế hoạch nội dung tuần (weekly-content-planner)
và tự động chọn 1 Topic chuẩn cho Video AI (lịch Thứ 3 hoặc Thứ 6).
"""

import os
import sys
import json
import datetime
import argparse
from pathlib import Path

# Cấu hình UTF-8 cho Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


DEFAULT_VIDEO_TOPICS = {
    "tuesday": {
        "day_name": "Thứ 3",
        "pillar": "Giáo dục / Myth Buster (Vạch trần sai lầm)",
        "topic": "Đừng nhồi thêm canxi nếu con bạn vẫn chưa cao — Bí mật kích hoạt Hormone GH ban đêm",
        "hook": "Đừng ép con uống canxi vô cơ nếu mẹ chưa biết sự thật 90% phụ huynh mắc phải này!",
        "style": "casual",
        "angle": "Khoa học tăng chiều cao & vai trò Alpha-GPC kích hoạt tuyến yên ban đêm",
        "voiceover": "Canxi chỉ là gạch vữa, Hormone GH mới là thợ xây. Nano Growth kết hợp Alpha-GPC và Canxi nano vỏ trứng êm bụng, 2 viên nhai cacao con tự giác mỗi tối.",
        "text_overlay": "BÍ MẬT TĂNG CHIỀU CAO BAN ĐÊM"
    },
    "friday": {
        "day_name": "Thứ 6",
        "pillar": "Uy quyền / Chuyên sâu & Chuẩn Nhật (Authority & Medical Proof)",
        "topic": "3 tiêu chuẩn khắt khe để một viên Nano Canxi được cấp phép tại Nhật Bản",
        "hook": "Tại sao người Nhật không cho con uống canxi liều cao bừa bãi? Đây là câu trả lời!",
        "style": "luxury",
        "angle": "Nhà máy Nichiei Asia đạt chuẩn GMP Nhật Bản và giấy phép Cục An Toàn Thực Phẩm",
        "voiceover": "Đạt chuẩn GMP Nhật Bản và kiểm định nghiêm ngặt, Nano Growth Habit EX bảo chứng chất lượng với công thức hấp thu tối đa, không lắng cặn.",
        "text_overlay": "CHUẨN Y KHOA NHẬT BẢN"
    }
}


def get_topic_for_today(day_override: str = None) -> dict:
    """Tự động phát hiện ngày trong tuần hoặc nhận chỉ định"""
    today_weekday = datetime.datetime.now().weekday()  # 0: Monday, 1: Tuesday, 4: Friday...
    
    if day_override:
        day_key = day_override.lower()
    else:
        # Nếu là thứ 3 (weekday=1) -> tuesday, nếu là thứ 6 (weekday=4) -> friday
        if today_weekday == 1:
            day_key = "tuesday"
        elif today_weekday == 4:
            day_key = "friday"
        else:
            # Nếu chạy các ngày khác trong tuần, mặc định luân phiên chọn slot gần nhất
            day_key = "tuesday" if today_weekday < 3 else "friday"

    selected = DEFAULT_VIDEO_TOPICS.get(day_key, DEFAULT_VIDEO_TOPICS["tuesday"])
    
    # Thử quét thư mục weekly-content-planner xem có file kế hoạch động nào không
    skills_root = Path(__file__).resolve().parent.parent.parent
    possible_plan_files = [
        skills_root / "weekly-content-planner" / "output" / "weekly_plan_latest.json",
        Path.cwd() / "weekly-content-planner" / "output" / "weekly_plan_latest.json"
    ]
    for pf in possible_plan_files:
        if pf.exists():
            try:
                with open(pf, "r", encoding="utf-8") as f:
                    plan_data = json.load(f)
                    # Tìm slot video trong plan_data
                    for day_plan in plan_data.get("days", []):
                        if day_plan.get("format", "").lower() in ["video", "reels", "tiktok"] or day_plan.get("day", "").lower() == day_key:
                            selected["topic"] = day_plan.get("topic", selected["topic"])
                            selected["hook"] = day_plan.get("hook", selected["hook"])
                            break
            except Exception:
                pass

    return selected


def main():
    parser = argparse.ArgumentParser(description="Chọn Topic Video AI từ Content Plan Tuần")
    parser.add_argument("--day", choices=["tuesday", "friday"], default=None, help="Chỉ định slot Thứ 3 hoặc Thứ 6")
    parser.add_argument("--json", action="store_true", help="Xuất JSON thuần")
    args = parser.parse_args()

    topic_info = get_topic_for_today(args.day)

    if args.json:
        print(json.dumps(topic_info, ensure_ascii=False, indent=2))
    else:
        print("\n==================== TOPIC VIDEO TUẦN NÀY ĐƯỢC CHỌN ====================")
        print(f"Lịch phát sóng : {topic_info['day_name']} (9:00 Sáng)")
        print(f"Trụ cột        : {topic_info['pillar']}")
        print(f"Chủ đề chính   : {topic_info['topic']}")
        print(f"Góc tiếp cận   : {topic_info['angle']}")
        print(f"Phong cách     : {topic_info['style'].upper()}")
        print(f"Hook 3s đầu    : \"{topic_info['hook']}\"")
        print("========================================================================\n")


if __name__ == "__main__":
    main()
