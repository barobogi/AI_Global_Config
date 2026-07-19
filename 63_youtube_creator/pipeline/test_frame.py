from moviepy import ColorClip, TextClip, CompositeVideoClip
import textwrap
import os

W, H = 1920, 1080
# 가장 긴 텍스트 중 하나로 테스트 (3줄 분량)
text = "오늘은 그 세 명의 에이아이가 어떻게 하나의 팀으로 뭉치게 되었는지, 그 비하인드 스토리를 들려드리려 합니다. 아주 길게 텍스트를 작성해봅니다."

wrapped_text = "\n".join(textwrap.wrap(text, width=35)) + "\n "

font_size = int(H * 0.055)
txt_clip = TextClip(
    font=r"C:\Windows\Fonts\malgun.ttf",
    text=wrapped_text,
    font_size=font_size,
    color="white",
    stroke_color="black",
    stroke_width=2,
    method="label",
    text_align="center"
)

subtitle_y = H - txt_clip.size[1] - 60
txt_clip = txt_clip.with_position(('center', subtitle_y))

bg = ColorClip(size=(W, H), color=(0, 0, 0))
comp = CompositeVideoClip([bg, txt_clip]).with_duration(1)
comp.save_frame("test_frame.png", t=0)

print(f"해상도: {W}x{H}")
print(f"텍스트 블록 크기: {txt_clip.size}")
print(f"텍스트 Y좌표 (상단): {subtitle_y}")
print(f"텍스트 Y좌표 (하단 끝점): {subtitle_y + txt_clip.size[1]}")
print(f"하단 마진(여백): {H - (subtitle_y + txt_clip.size[1])}px")
