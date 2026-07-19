# test_subtitle.py — 씬 1개 자막 테스트 렌더링
import sys, textwrap, numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from PIL import Image as PILImage
from moviepy import ImageClip, TextClip, CompositeVideoClip

IMG = r"D:\AI\63_youtube_creator\pipeline\images\scene_01.jpg"
OUT = r"D:\AI\63_youtube_creator\pipeline\output\test_subtitle.mp4"
TEXT = "안녕하세요. 저희 채널 쇼츠에서 에이아이 세 명이 알아서 코딩하고 렌더링하는 모습, 신기하게 보셨나요?"

W, H = 1920, 1080
pil_img = PILImage.open(IMG).resize((W, H), PILImage.LANCZOS)
img_clip = ImageClip(np.array(pil_img)).with_duration(3)

wrapped = "\n".join(textwrap.wrap(TEXT, width=25)) + "\n "
font_size = int(H * 0.06)
subtitle_y = int(H * 0.83)

txt_clip = TextClip(
    font=r"C:\Windows\Fonts\malgun.ttf",
    text=wrapped,
    font_size=font_size,
    color="white",
    stroke_color="black",
    stroke_width=2,
    method="label",
    text_align="center"
).with_position(('center', subtitle_y)).with_duration(3)

video = CompositeVideoClip([img_clip, txt_clip])
video.write_videofile(OUT, fps=24, codec="libx264")
print(f"완료: {OUT}")
print(f"이미지 크기: {W}x{H}, 폰트: {font_size}px, 자막 y: {subtitle_y}")
