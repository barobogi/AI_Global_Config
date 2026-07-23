import sys
import os
import cv2
from google import genai
from google.genai import types

def check_video_visuals(video_path):
    print(f"[{video_path}] 시각 품질(폰트 깨짐) 검증 시작...")
    
    if not os.path.exists(video_path):
        print(f"오류: 파일을 찾을 수 없습니다 -> {video_path}")
        sys.exit(1)
        
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("오류: 비디오를 열 수 없습니다.")
        sys.exit(1)
        
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if total_frames == 0:
        print("오류: 비디오에 프레임이 없습니다.")
        sys.exit(1)
        
    # 중간중간 3개의 프레임 추출
    frame_indices = [int(total_frames * 0.25), int(total_frames * 0.5), int(total_frames * 0.75)]
    extracted_images = []
    
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            img_path = f"temp_frame_{idx}.jpg"
            cv2.imwrite(img_path, frame)
            extracted_images.append(img_path)
            
    cap.release()
    
    if not extracted_images:
        print("오류: 프레임을 추출하지 못했습니다.")
        sys.exit(1)
        
    print(f"총 {len(extracted_images)}장의 프레임을 추출하여 Gemini Vision API로 전송합니다.")
    
    # Gemini API 호출
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("오류: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
        sys.exit(1)
        
    client = genai.Client()
    
    prompt = """
    이 이미지는 유튜브 영상의 프레임입니다. 화면 하단에 자막이 있습니다.
    자막을 주의 깊게 읽어보세요.
    만약 자막 글씨가 물음표(???)나 네모 상자 모양(ToFu)으로 심각하게 깨져서 출력되었다면 'FAIL'을 반환하세요.
    글씨가 정상적인 한국어 문장으로 잘 읽힌다면 'PASS'를 반환하세요.
    응답은 오직 'PASS' 또는 'FAIL' 두 단어 중 하나만 출력하세요.
    """
    
    all_passed = True
    
    for img_path in extracted_images:
        print(f"  - {img_path} 검증 중...")
        # Upload file to Gemini
        try:
            uploaded_file = client.files.upload(file=img_path)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[uploaded_file, prompt]
            )
            result = response.text.strip().upper()
            print(f"    결과: {result}")
            
            if "FAIL" in result:
                all_passed = False
                
        except Exception as e:
            print(f"    Gemini API 호출 중 오류 발생: {e}")
            all_passed = False
            
        finally:
            # Clean up
            if os.path.exists(img_path):
                os.remove(img_path)
                
    if all_passed:
        print(f"\n[최종 결과] PASS: 폰트 깨짐이 발견되지 않았습니다. 정상입니다.")
        sys.exit(0)
    else:
        print(f"\n[최종 결과] FAIL: 폰트 깨짐(ToFu) 현상이 감지되었습니다. 렌더링 스크립트의 폰트를 점검하세요.")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="영상 시각 품질(폰트 깨짐) 검증기")
    parser.add_argument("video_path", help="검증할 영상 파일 경로")
    args = parser.parse_args()
    
    # stdout 인코딩 강제 설정 (이모지 및 한글 출력 에러 방지)
    import sys
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    
    check_video_visuals(args.video_path)
