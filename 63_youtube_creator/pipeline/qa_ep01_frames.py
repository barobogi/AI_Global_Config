import cv2
import sys
import os

def check_text_overflow(video_path):
    print(f"=== EP01 본편 시각 품질 자동 검증 시작 ===")
    print(f"대상 영상: {video_path}")
    
    if not os.path.exists(video_path):
        print("오류: 영상을 찾을 수 없습니다.")
        return False

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("오류: 영상을 열 수 없습니다.")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"해상도: {width}x{height}, 총 프레임: {frame_count}")

    # Safe Zone: 하단 5% 영역 (y좌표 1026 ~ 1080)
    # 텍스트는 무조건 H - txt_clip.h - 60 에 위치하므로 하단 5%에는 흰색 텍스트가 없어야 정상임.
    safe_zone_top = int(height * 0.95)
    
    overflow_detected = False
    checked_frames = 0
    
    # 1초마다 1프레임씩 추출하여 검사
    step = int(fps) if fps > 0 else 24
    
    for i in range(0, frame_count, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            continue
            
        checked_frames += 1
        
        # 하단 5% 영역 크롭
        bottom_region = frame[safe_zone_top:height, 0:width]
        
        # 그레이스케일 변환 및 이진화 (흰색 텍스트 픽셀 감지)
        gray = cv2.cvtColor(bottom_region, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        
        # 흰색 픽셀 개수 계산
        white_pixels = cv2.countNonZero(thresh)
        
        # 노이즈를 고려하여 100개 이상의 순백색 픽셀이 하단 5%에 있으면 오버플로우로 간주
        if white_pixels > 100:
            print(f"[경고] 프레임 {i}에서 텍스트 오버플로우 감지! (침범 픽셀 수: {white_pixels})")
            cv2.imwrite("overflow_debug_raw.png", bottom_region)
            cv2.imwrite("overflow_debug_thresh.png", thresh)
            overflow_detected = True
            break
            
    cap.release()
    
    if overflow_detected:
        print("❌ 검증 실패: 자막 텍스트가 하단 Safe Zone(5%)을 침범했습니다. 렌더링 좌표 수정이 필요합니다.")
        return False
    else:
        print(f"✅ 검증 통과: 총 {checked_frames}개 샘플 프레임 검사 완료. 하단 텍스트 잘림/오버플로우 없음.")
        return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        vid = sys.argv[1]
    else:
        vid = r"D:\AI\63_youtube_creator\pipeline\output\Main_EP01_AI_Governance.mp4"
    
    success = check_text_overflow(vid)
    sys.exit(0 if success else 1)
