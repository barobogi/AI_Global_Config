from moviepy import VideoFileClip
from PIL import Image
import os

def extract_frames():
    video_path = r"D:\AI\63_youtube_creator\pipeline\output\Main_EP02_System_Evolution.mp4"
    if not os.path.exists(video_path):
        print(f"Video not found: {video_path}")
        return
        
    video = VideoFileClip(video_path)
    
    # Scene 01 is usually at the beginning (0 ~ 36초).
    # 5초, 15초, 25초 대의 프레임을 추출하여 텍스트가 누적되는지 확인합니다.
    times = [5, 15, 25]
    
    print("프레임 추출 시작...")
    for i, t in enumerate(times):
        if t < video.duration:
            frame = video.get_frame(t)
            img = Image.fromarray(frame)
            out_path = rf"D:\AI\63_youtube_creator\pipeline\output\ep02_proof_frame_{t}s.jpg"
            img.save(out_path)
            print(f"프레임 저장 완료: {out_path}")
        else:
            print(f"타임스탬프 {t}s 가 비디오 전체 길이보다 깁니다.")
            
    video.close()
    print("프레임 추출 완료.")

if __name__ == "__main__":
    extract_frames()
