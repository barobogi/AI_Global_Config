import os
import json
from PIL import Image, ImageDraw, ImageFont

# 로컬 설정 파일 로드
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)["youtube_pipeline"]

VISUAL = config["visual_settings"]
WIDTH, HEIGHT = VISUAL["resolution"]

# 폰트 로드 (기본 폰트 폴더 또는 특정 경로 필요)
# TODO: D2Coding 등 지정된 폰트 파일(.ttf)이 실제 경로에 있어야 함
# 여기서는 테스트를 위해 시스템 기본 폰트로 대체 처리할 수 있도록 구현
def get_font(size):
    try:
        # Windows의 맑은 고딕 등을 대체재로 임시 사용, 실제로는 D2Coding.ttf 경로 지정 필요
        font_name = VISUAL["font_name"]
        return ImageFont.truetype("malgun.ttf", size) # D2Coding이 없을 경우를 대비한 하드코딩 회피
    except Exception:
        return ImageFont.load_default()

def draw_waveform(draw, wave_data, accent_color, width, height):
    """하단에 오디오 웨이브폼 바 그리기"""
    if not wave_data.any():
        return
        
    num_bars = len(wave_data)
    bar_width = (width * 0.8) / num_bars
    max_bar_height = height * 0.2
    
    start_x = width * 0.1
    base_y = height * 0.85
    
    for i, amplitude in enumerate(wave_data):
        # 진폭에 비례하는 바 높이 계산
        bar_height = amplitude * max_bar_height
        
        x1 = start_x + (i * bar_width)
        y1 = base_y - bar_height
        x2 = x1 + (bar_width * 0.6) # 막대 사이 간격 0.4
        y2 = base_y + bar_height # 위아래 대칭
        
        draw.rectangle([x1, y1, x2, y2], fill=accent_color)

def create_frame(text, wave_data, frame_index, total_frames):
    """Pillow를 사용하여 단일 프레임 이미지 객체 생성"""
    # 1. 배경 생성 (코니 설정색)
    img = Image.new('RGB', (WIDTH, HEIGHT), color=VISUAL["bg_color"])
    draw = ImageDraw.Draw(img)
    
    # 2. 텍스트 타이핑 이펙트 처리 (프레임 진행도에 따라 글씨가 나타남)
    # total_frames 대비 frame_index 비율로 보여줄 글자 수 계산
    progress = frame_index / max(1, total_frames)
    chars_to_show = int(len(text) * progress)
    visible_text = text[:chars_to_show]
    
    # 3. 텍스트 그리기 (중앙 정렬)
    font = get_font(80) # 글자 크기 80
    
    # getbbox()로 텍스트 크기 계산
    bbox = draw.textbbox((0, 0), visible_text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (WIDTH - text_w) / 2
    y = (HEIGHT - text_h) / 2.5 # 약간 위쪽 중앙
    
    draw.text((x, y), visible_text, font=font, fill="#ffffff") # 글씨는 흰색
    
    # 4. 하단 웨이브폼 그리기 (코니 포인트 컬러)
    draw_waveform(draw, wave_data, VISUAL["accent_color"], WIDTH, HEIGHT)
    
    return np.array(img) # MoviePy가 사용할 수 있도록 numpy 배열로 반환

if __name__ == "__main__":
    import numpy as np
    # 간단한 단일 프레임 테스트 렌더링
    test_wave = np.random.rand(50) # 랜덤 파형 50개
    test_img_array = create_frame("이것은 타이핑 이펙트 테스트입니다.", test_wave, 20, 40)
    
    # numpy 배열을 다시 이미지로 변환하여 저장
    test_img = Image.fromarray(test_img_array)
    test_img.save("test_frame.png")
    print("테스트 프레임 저장 완료: test_frame.png")
