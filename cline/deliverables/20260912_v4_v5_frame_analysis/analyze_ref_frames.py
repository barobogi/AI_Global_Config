"""v4/v5 비교 프레임 상세 분석"""
from PIL import Image
import numpy as np
import os

base = r"D:\AI\cline\2026-08-30\16_shorts_upgrade\output\ref_frames_v5"

names = ["v4_f03", "v5_f03", "v4_f04", "v5_f04", "v4_f05", "v5_f05"]

for name in names:
    p = os.path.join(base, name + ".png")
    img = Image.open(p)
    arr = np.array(img)
    h, w, _ = arr.shape
    print(f"=== {name} ({w}x{h}) ===")
    # 구간별 평균 밝기 (위에서 아래로 10등분)
    for i in range(10):
        y0 = int(h * i / 10)
        y1 = int(h * (i + 1) / 10)
        region = arr[y0:y1, :, :]
        gray = region.mean(axis=2)
        print(f"  행 {i*10:2d}-{(i+1)*10:2d}%: 밝기={gray.mean():.1f}, R={region[:,:,0].mean():.0f}, G={region[:,:,1].mean():.0f}, B={region[:,:,2].mean():.0f}")
    # 배경 영역 색상 분포 (하단 40%)
    bg = arr[int(h * 0.6):, :, :]
    print(f"  배경(60-100%): R={bg[:,:,0].mean():.0f} G={bg[:,:,1].mean():.0f} B={bg[:,:,2].mean():.0f}")
    for c, cn in enumerate(["R", "G", "B"]):
        print(f"  배경 {cn}: std={bg[:,:,c].std():.1f}")
    print()
