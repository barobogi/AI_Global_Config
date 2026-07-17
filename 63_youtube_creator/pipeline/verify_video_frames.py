import cv2
import numpy as np
import sys
import os

SAFE_ZONE_PERCENT = 0.05  # 하단 5%를 Safe Zone으로 설정

def check_video_text_overflow(video_path):
    if not os.path.exists(video_path):
        print(f"오류: 영상을 찾을 수 없습니다 -> {video_path}")
        return False

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("오류: 영상을 열 수 없습니다.")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 1초당 1프레임 추출 설정
    frame_interval = int(fps) if fps > 0 else 30
    
    passed = True
    frame_idx = 0
    checked_frames = 0
    
    print(f"🔍 OpenCV 영상 픽셀 하단 잘림(Descender cutoff) 검증 시작: {os.path.basename(video_path)}")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_idx % frame_interval == 0:
            h, w = frame.shape[:2]
            safe_y_bottom = int(h * (1.0 - SAFE_ZONE_PERCENT))
            
            # 하단 20% 영역만 크롭 (자막 영역 한정 스캔)
            crop_start = int(h * 0.8)
            crop_frame = frame[crop_start:h, :]
            
            gray = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
            
            # 밝은 글씨(흰색) 추출을 위한 Threshold
            _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            max_y_in_crop = 0
            
            for cnt in contours:
                x, y, cw, ch = cv2.boundingRect(cnt)
                if cw * ch < 50:  # 너무 작은 노이즈 무시
                    continue
                
                # 원본 이미지 기준 y 좌표로 변환
                global_y_bottom = crop_start + y + ch
                if global_y_bottom > max_y_in_crop:
                    max_y_in_crop = global_y_bottom

            if max_y_in_crop > safe_y_bottom:
                print(f"❌ [프레임 {frame_idx}] 텍스트 하단 잘림/Safe Zone 침범 감지! (침범 좌표: y={max_y_in_crop}, Safe 기준: y={safe_y_bottom})")
                passed = False
                break
            
            checked_frames += 1

        frame_idx += 1

    cap.release()
    
    if passed:
        print(f"✅ 모든 검사 프레임({checked_frames}장) Safe Zone(5%) 검증 통과! (하단 잘림 없음)")
        return True
    else:
        print("❌ 시각 품질 검증 실패. 조치가 필요합니다.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python verify_video_frames.py <비디오_경로>")
        sys.exit(1)
        
    video_file = sys.argv[1]
    success = check_video_text_overflow(video_file)
    if not success:
        sys.exit(1)
