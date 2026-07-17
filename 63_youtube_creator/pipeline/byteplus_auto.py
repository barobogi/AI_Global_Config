import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import asyncio

async def generate_scene_image(prompt_text, output_path):
    """
    API 정책 위반 및 연동 실패로 인해, E2E 파이프라인 전체 관통 테스트를 위해
    Pillow를 사용한 로컬 Draft(Placeholder) 이미지를 즉석에서 생성합니다.
    """
    print(f"\n========== 임시 이미지 생성 (Offline Draft) ==========")
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    # 1920x1080 어두운 배경 생성
    img = Image.new('RGB', (1920, 1080), color=(40, 44, 52))
    d = ImageDraw.Draw(img)

    # 텍스트 세팅 (기본 폰트 사용)
    try:
        # Windows 기본 폰트 시도
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()

    # 프롬프트 텍스트 줄바꿈 처리
    wrapped_text = textwrap.fill(prompt_text, width=50)
    scene_name = os.path.basename(output_path).replace('.jpg', '')
    text_content = f"[{scene_name}]\n\n{wrapped_text}"

    # 텍스트를 중앙에 배치
    # draw.textbbox 사용 (Pillow 최신 버전)
    bbox = d.textbbox((0, 0), text_content, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (1920 - text_w) / 2
    y = (1080 - text_h) / 2

    # 텍스트 그리기
    d.text((x, y), text_content, font=font, fill=(171, 178, 191), align="center")

    # 저장
    img.save(output_path, quality=90)
    print(f"  - [성공] 임시 프롬프트 이미지 저장 완료: {output_path}")
    
    return True

if __name__ == "__main__":
    print("Offline Draft 모드 단독 테스트 실행")
    result = generate_scene_image(99, "A futuristic robot typing on a computer, highly detailed, 8k resolution")
    print(f"테스트 결과: {result}")
