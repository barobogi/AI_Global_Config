import sys
import os
from googleapiclient.http import MediaFileUpload
# youtube_uploader에서 인증 함수 재사용
from youtube_uploader import get_authenticated_service

def upload_caption(video_id, caption_file):
    youtube = get_authenticated_service()
    
    print(f"[{video_id}] 에 자막({caption_file}) 업로드를 시작합니다...")
    
    # 캡션 추가
    media = MediaFileUpload(caption_file, mimetype='application/octet-stream', resumable=True)
    request = youtube.captions().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "language": "ko",
                "name": "Korean (한국어)",
                "isDraft": False
            }
        },
        media_body=media
    )
    
    try:
        response = request.execute()
        print(f"✅ 자막 업로드 완료! Caption ID: {response['id']}")
    except Exception as e:
        print(f"❌ 자막 업로드 실패: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_srt.py <VIDEO_ID>")
        sys.exit(1)
        
    vid = sys.argv[1]
    srt_path = os.path.join(os.path.dirname(__file__), "output", "crisp_dm_shorts.srt")
    
    if not os.path.exists(srt_path):
        print(f"SRT 파일이 없습니다: {srt_path}")
        print("render_video.py를 다시 실행해서 SRT를 생성하세요.")
        sys.exit(1)
        
    upload_caption(vid, srt_path)
