import os
import json
import datetime
import urllib.request
from googleapiclient.discovery import build
from youtube_uploader import get_authenticated_service

TELEGRAM_TOKEN   = "8850996295:AAHXKedqZflR71jhDTR0MKutjxBdHWfxNAo"
TELEGRAM_CHAT_ID = "465471725"

def _send_telegram(msg: str):
    try:
        payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data=payload, headers={"Content-Type": "application/json"}, method="POST",
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"[Telegram] 알림 실패: {e}")

def run_publisher():
    print("=== YouTube Auto Publisher ===")
    
    # 0 = 월요일, 1 = 화요일, 2 = 수요일, 3 = 목요일, 4 = 금요일, 5 = 토요일, 6 = 일요일
    today_weekday = datetime.datetime.today().weekday()
    
    target_type = None
    target_count = 1
    
    if today_weekday in [1, 3]:  # 화(1), 목(3)
        print("오늘은 쇼츠 발행일(화/목)입니다.")
        target_type = "shorts"
    elif today_weekday == 5:  # 토(5)
        print("오늘은 본편 발행일(토)입니다.")
        target_type = "full"
    else:
        print("오늘은 발행일이 아닙니다. 스케줄러를 종료합니다.")
        return

    queue_file = os.path.join(os.path.dirname(__file__), "publish_queue.json")
    if not os.path.exists(queue_file):
        print("대기열(publish_queue.json)이 없습니다.")
        return

    with open(queue_file, "r", encoding="utf-8") as f:
        try:
            queue_data = json.load(f)
        except json.JSONDecodeError:
            print("큐 파일 형식이 잘못되었습니다.")
            return

    target_list_key = "pending_shorts" if target_type == "shorts" else "pending_full"
    pending_list = queue_data.get(target_list_key, [])
    
    if not pending_list:
        print(f"발행 대기 중인 {target_type} 영상이 없습니다!")
        _send_telegram(f"⚠️ <b>유튜브 스케줄러 경고</b>\n오늘 발행해야 할 <b>{target_type}</b> 영상이 대기열에 없습니다. 업로드를 확인해주세요.")
        return

    # 첫 번째 영상을 발행
    video_to_publish = pending_list.pop(0)
    video_id = video_to_publish["video_id"]
    title = video_to_publish["title"]
    
    print(f"발행 대상 선정: {title} ({video_id})")
    
    try:
        youtube = get_authenticated_service()
        # privacyStatus 를 public 으로 업데이트
        body = {
            "id": video_id,
            "status": {
                "privacyStatus": "public"
            }
        }
        
        request = youtube.videos().update(
            part="status",
            body=body
        )
        response = request.execute()
        
        print(f"영상 공개 전환 완료! Response: {response.get('status', {})}")
        
        # 상태 업데이트 및 published 목록으로 이동
        video_to_publish["status"] = "public"
        video_to_publish["published_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        queue_data.setdefault("published", []).append(video_to_publish)
        
        # 큐 저장
        with open(queue_file, "w", encoding="utf-8") as f:
            json.dump(queue_data, f, ensure_ascii=False, indent=4)
            
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        _send_telegram(
            f"🚀 <b>유튜브 예약 자동 발행 완료</b>\n"
            f"구분: {target_type.upper()}\n"
            f"제목: {title}\n"
            f"링크: {video_url}"
        )
        
    except Exception as e:
        print(f"발행 중 오류 발생: {e}")
        # 오류 발생 시 다시 pending list의 맨 앞에 복구
        pending_list.insert(0, video_to_publish)
        with open(queue_file, "w", encoding="utf-8") as f:
            json.dump(queue_data, f, ensure_ascii=False, indent=4)
            
        _send_telegram(f"❌ <b>유튜브 자동 발행 실패</b>\n제목: {title}\n에러: {e}")

if __name__ == "__main__":
    run_publisher()
