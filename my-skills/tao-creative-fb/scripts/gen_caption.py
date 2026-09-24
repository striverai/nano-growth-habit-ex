#!/usr/bin/env python3
"""
gen_caption.py — Viết caption và ad copy chuẩn Brand Voice Nano Growth Habit EX.
Hỗ trợ Mode 1 (Organic Fanpage) và Mode 2 (Creative Ads: Pain Point / Solution / Social Proof).
Độ dài ~80-150 từ, format hook + body + CTA, có cơ chế retry và fallback chất lượng cao khi DRY_RUN.
"""

import os
import sys
import time
import argparse
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

# Hệ thống tri thức Brand Voice chuẩn từ brain.db
BRAND_KNOWLEDGE = {
    "positioning": "Canxi chỉ là gạch vữa, Hormone tăng trưởng (GH) mới là thợ xây: Nano Growth Habit EX đánh thức chiều cao từ bên trong với 2 viên nhai chuẩn Nhật mỗi tối.",
    "core_usps": [
        "Hoạt chất Alpha-GPC chuẩn Nhật kích hoạt tuyến yên tiết hormone tăng trưởng GH nội sinh lúc ngủ sâu (11h đêm - 3h sáng).",
        "Canxi hữu cơ bột vỏ trứng kết hợp CPP (Casein Phosphopeptide) hòa tan tối đa, êm bụng, không nóng trong, không lo táo bón.",
        "Phức hợp Protetite (collagen và khoáng chất) giúp xương dài và đặc.",
        "2 viên nhai vị cacao thơm ngon như kẹo socola, trẻ 6-18 tuổi tự giác nhai mỗi tối không cần ép nuốt."
    ],
    "pricing_math": "1 lọ 120 viên dùng trọn vẹn 2 tháng, tính ra chỉ ~20.000đ/ngày — bằng đúng hộp sữa tươi.",
    "rules": "Câu ngắn gãy gọn (2-3 câu/đoạn). Thẳng thắn, giàu năng lượng, thực tế. Tuyệt đối không dùng từ sáo rỗng: synergy, tối ưu hóa trải nghiệm, kính chào quý khách."
}

# Template nội dung chuẩn thực chiến phòng khi offline hoặc DRY_RUN
FALLBACK_TEMPLATES = {
    "organic": {
        "idea_1": (
            "Uống bao nhiêu canxi mà quên điều này thì con vẫn thấp bé!\n\n"
            "Thật ra, nhiều mẹ cứ nghĩ con thấp là do thiếu canxi, rồi mua đủ loại canxi nạp vào. Nhưng canxi chỉ như đống gạch vữa đổ trước sân thôi. Nếu thiếu 'người thợ xây' là Hormone Tăng Trưởng (GH) mở đĩa sụn, gạch nhiều mấy xương cũng không dài ra được.\n\n"
            "Chưa kể canxi vô cơ rất dễ gây nóng trong, táo bón khiến con sợ hãi mỗi lần uống. Đơn giản thôi mẹ ơi: chọn dòng kích hoạt hormone GH tự nhiên lúc con ngủ sâu, kết hợp canxi vỏ trứng êm ru hệ tiêu hóa.\n\n"
            "Mẹ để lại bình luận độ tuổi và chiều cao hiện tại của con, em cùng dược sĩ xem giúp lộ trình phù hợp nhé!"
        ),
        "idea_2": (
            "Mỗi tối lại một trận chiến ép con nuốt thuốc viên to đùng?\n\n"
            "Em hiểu cảm giác của các mẹ: mua lọ canxi tiền triệu về mà con ngửi thấy mùi tanh nồng là lắc đầu nguầy nguậy, ép mãi con khóc mẹ bực.\n\n"
            "Sản phẩm tốt nhất cho con chính là thứ con tự giác dùng mỗi ngày mà không cần nhắc. Với Nano Growth Habit EX, con chỉ cần nhai 2 viên thơm lừng vị cacao mỗi tối trước khi đi ngủ, ngon như ăn kẹo socola.\n\n"
            "Vừa kích hoạt hormone tăng trưởng GH ban đêm, vừa êm bụng không táo bón. Mẹ nào đang đau đầu vì con sợ uống canxi thì nhắn ngay cho em chia sẻ kinh nghiệm nhé!"
        ),
        "idea_3": (
            "Vì sao canxi chuẩn Nhật lại không gây nóng trong hay táo bón?\n\n"
            "Nhiều mẹ chia sẻ cứ cho con uống canxi là vài ngày sau con bắt đầu khó tiêu, nổi mụn, táo bón. Nguyên nhân vì các hạt canxi thông thường bị kết tủa tự do tại ruột non do không tan hết.\n\n"
            "Chuẩn khoa học Nhật Bản giải quyết triệt để vấn đề này bằng bộ đôi: Canxi hữu cơ bột vỏ trứng tự nhiên kết hợp CPP (Casein Phosphopeptide). CPP đóng vai trò như chiếc màng bảo vệ giữ canxi luôn ở trạng thái hòa tan tối đa, giúp ruột non hấp thu êm ru.\n\n"
            "Bổ sung canxi là phải khỏe và thoải mái từ bên trong. Mẹ cần tham khảo bảng thành phần chi tiết cứ nhắn tin cho Page em gửi ngay nha!"
        )
    },
    "ads": {
        "pain_point": (
            "Đừng để con lỡ mất 2 năm tuổi vàng dậy thì chỉ vì bổ sung canxi sai cách!\n\n"
            "Nhiều cha mẹ thấy con thấp hơn bạn cùng lứa thì sốt ruột mua canxi về nhồi nhét. Nhưng nạp canxi vô cơ không hấp thu hết chỉ khiến con thêm táo bón, nóng trong, mà đĩa sụn xương vẫn 'ngủ quên'.\n\n"
            "Sự thật là: Canxi chỉ là gạch vữa, Hormone Tăng Trưởng (GH) mới là thợ xây. Nano Growth Habit EX chuẩn Nhật bổ sung Alpha-GPC kích hoạt chính tuyến yên tiết GH mạnh mẽ trong giấc ngủ đêm, cùng canxi hữu cơ vỏ trứng êm bụng tuyệt đối.\n\n"
            "Tính ra chỉ ~20.000đ/ngày, bằng đúng hộp sữa tươi để đổi lấy vóc dáng tự tin cả đời cho con.\n\n"
            "👉 Đặt ngay hôm nay để nhận Ưu Đãi Mua 2 Tặng 1 + Thước đo chiều cao Nhật Bản độc quyền!"
        ),
        "solution": (
            "Đột phá tăng chiều cao chuẩn Nhật: Đánh thức Hormone Tăng Trưởng tự nhiên mỗi đêm!\n\n"
            "Không cần ép con nuốt từng viên nén thô cứng hay siro nồng mùi. Với Nano Growth Habit EX, con tự giác nhai 2 viên vị cacao thơm ngon mỗi tối như một món thưởng.\n\n"
            "3 sức mạnh vượt trội trong 1 giải pháp:\n"
            "1. Hoạt chất Alpha-GPC kích hoạt tuyến yên tiết hormone GH nội sinh ban đêm.\n"
            "2. Canxi vỏ trứng + CPP chống lắng cặn, chống táo bón, êm ru tiêu hóa.\n"
            "3. Phức hợp Protetite nuôi dưỡng khung xương vừa dài vừa đặc chắc.\n\n"
            "1 lọ 120 viên con nhai trọn 2 tháng. Đầu tư đúng thời điểm vàng, con cao lớn vững vàng!\n\n"
            "👉 Bấm 'Gửi Tin Nhắn' ngay để Dược sĩ chuyên môn lên phác đồ tăng trưởng cá nhân hóa cho con!"
        ),
        "social_proof": (
            "'Con em trước đây sợ canxi lắm, giờ tối nào cũng tự giác xin mẹ 2 viên cacao rồi mới chịu đi ngủ!'\n\n"
            "Đó là chia sẻ của mẹ Lan (Hà Nội) sau 2 tháng đồng hành cùng Nano Growth Habit EX. Trước đây mua canxi xách tay viên to bắt con nuốt thì con trốn, lại hay kêu ấm ách bụng táo bón.\n\n"
            "Chuyển sang Nano Growth chuẩn Nhật chính ngạch, con mê tít vị socola, tiêu hóa nhẹ tênh. Sau 1 liệu trình, thước đo dán tường của con đã nhích lên rõ rệt trong sự ngỡ ngàng của cả nhà!\n\n"
            "Hơn 1.200 phụ huynh thông thái đã tin chọn Nano Growth Habit EX cho con trong giai đoạn 6-18 tuổi.\n\n"
            "👉 Nhận tư vấn 1-1 miễn phí từ Dược sĩ và nhận trọn bộ cẩm nang phát triển chiều cao Nhật Bản ngay hôm nay!"
        )
    }
}


def generate_caption(mode: str = "organic", topic: str = "idea_1", angle: str = "pain_point", custom_prompt: str = "") -> str:
    """
    Sinh caption/ad copy theo đúng brand voice.
    - mode: 'organic' hoặc 'ads'
    - topic: idea_1, idea_2, idea_3 hoặc từ khóa
    - angle: pain_point, solution, social_proof
    """
    # Nếu DRY_RUN hoặc không có OpenAI API Key, trả về nội dung mẫu xuất sắc được chuẩn bị sẵn
    if DRY_RUN or not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-proj-xxx"):
        if mode == "organic":
            key = topic if topic in FALLBACK_TEMPLATES["organic"] else "idea_1"
            return FALLBACK_TEMPLATES["organic"][key]
        else:
            key = angle if angle in FALLBACK_TEMPLATES["ads"] else "pain_point"
            return FALLBACK_TEMPLATES["ads"][key]

    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_instruction = f"""
Bạn là chuyên gia copywriter hàng đầu của thương hiệu Nano Growth Habit EX (Nano Canxi chuẩn Nhật Bản cho trẻ 6-18 tuổi).
Brand Voice cốt lõi:
- {BRAND_KNOWLEDGE['positioning']}
- Điểm khác biệt: {'; '.join(BRAND_KNOWLEDGE['core_usps'])}
- Bài toán chi phí: {BRAND_KNOWLEDGE['pricing_math']}
- Phong cách: {BRAND_KNOWLEDGE['rules']}
- Độ dài bắt buộc: Trong khoảng 80 đến 150 từ.
- Bố cục:
  1. Hook gây chú ý ngay dòng đầu tiên (dưới 15 từ).
  2. Thân bài chia đoạn ngắn (2-3 câu mỗi đoạn), nói bằng sự thật khoa học và trải nghiệm thực tế.
  3. Kêu gọi hành động (CTA) dứt khoát, tự nhiên.
"""

    if mode == "organic":
        user_prompt = f"""
Hãy viết 1 bài đăng Facebook Fanpage organic (bài thường ngày).
Chủ đề: {topic or 'Kiến thức tăng chiều cao và thói quen nhai canxi mỗi tối'}
Yêu cầu:
- Giọng văn gần gũi, chia sẻ như một người bạn/dược sĩ đồng hành cùng cha mẹ.
- Soft CTA (khuyến khích để lại bình luận hoặc nhắn tin tâm sự).
- Độ dài: 80 - 140 từ.
"""
    else:
        user_prompt = f"""
Hãy viết 1 bài quảng cáo Facebook Ads (Creative Ad Copy) chuyển đổi cao.
Góc tiếp cận (Angle): {angle.upper()} (pain_point / solution / social_proof).
Yêu cầu:
- Hook cực mạnh đánh trúng tâm lý phụ huynh có con 6-18 tuổi.
- Đưa bật luận điểm 'Canxi chỉ là gạch vữa, Hormone GH mới là thợ xây' và viên nhai cacao con tự giác.
- Nêu chi phí chỉ ~20k/ngày bằng hộp sữa.
- Hard CTA mạnh mẽ (Bấm nút nhắn tin, nhận ưu đãi).
- Độ dài: 90 - 150 từ.
"""

    max_retries = 2
    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[CẢNH BÁO] OpenAI Chat API thất bại (Lần {attempt}): {e}")
            if attempt < max_retries:
                time.sleep(2)
            else:
                # Fallback an toàn nếu API lỗi
                print("[FALLBACK] Sử dụng template chuẩn nội bộ.")
                if mode == "organic":
                    return FALLBACK_TEMPLATES["organic"].get(topic, FALLBACK_TEMPLATES["organic"]["idea_1"])
                else:
                    return FALLBACK_TEMPLATES["ads"].get(angle, FALLBACK_TEMPLATES["ads"]["pain_point"])


def main():
    parser = argparse.ArgumentParser(description="Sinh caption/ad copy theo Brand Voice Nano Growth EX")
    parser.add_argument("--mode", type=str, default="organic", choices=["organic", "ads"], help="Chế độ sinh nội dung")
    parser.add_argument("--topic", type=str, default="idea_1", help="Chủ đề bài viết hoặc idea_1, idea_2, idea_3")
    parser.add_argument("--angle", type=str, default="pain_point", choices=["pain_point", "solution", "social_proof"], help="Góc tiếp cận cho Ads")
    parser.add_argument("--output", type=str, default="", help="Đường dẫn file để lưu caption")
    args = parser.parse_args()

    caption = generate_caption(
        mode=args.mode,
        topic=args.topic,
        angle=args.angle
    )

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(caption)
        print(f"[THÀNH CÔNG] Đã lưu caption vào: {out_path}")

    print("\n--- CAPTION XUẤT BẢN ---")
    print(caption)
    print("------------------------\n")


if __name__ == "__main__":
    main()
