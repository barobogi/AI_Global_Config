import urllib.request
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

QUEUE_FILE = r"D:\AI\25_auto_pobbagi\youtube_queue.json"
CHANNELS_FILE = r"D:\AI\25_auto_pobbagi\channels.json"

# 기본 감시 채널 목록 (예시: 기술노트 with 알렉 등)
DEFAULT_CHANNELS = {
    "UCd1-XlZkK5D8ZgUvXqH-r2A": "기술노트 with 알렉", # 예시 채널 ID
    "UC_x5XG1OV2P6uZZ5FSM9Ttw": "Google Developers"
}

def load_json(filepath, default_val):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_val

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def fetch_channel_rss(channel_id):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            return xml_data
    except Exception as e:
        print(f"[오류] 채널 {channel_id} RSS 수집 실패: {e}")
        return None

def parse_rss_for_videos(xml_data):
    videos = []
    if not xml_data:
        return videos
    
    root = ET.fromstring(xml_data)
    # XML 네임스페이스 정의 (Atom 피드 및 유튜브 네임스페이스)
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'yt': 'http://www.youtube.com/xml/schemas/2015'
    }
    
    for entry in root.findall('atom:entry', ns):
        video_id = entry.find('yt:videoId', ns).text
        title = entry.find('atom:title', ns).text
        link = entry.find('atom:link', ns).attrib['href']
        published = entry.find('atom:published', ns).text
        
        videos.append({
            "video_id": video_id,
            "title": title,
            "link": link,
            "published": published
        })
    return videos

def run_watcher():
    print(f"=== 유튜브 RSS 자동 감시 시작 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    
    channels = load_json(CHANNELS_FILE, DEFAULT_CHANNELS)
    queue = load_json(QUEUE_FILE, {"pending": [], "processed": []})
    
    processed_ids = set(queue.get("processed", []))
    pending_ids = set(v["video_id"] for v in queue.get("pending", []))
    
    new_videos_found = 0
    
    for channel_id, channel_name in channels.items():
        print(f"[{channel_name}] 채널 RSS 분석 중...")
        xml_data = fetch_channel_rss(channel_id)
        videos = parse_rss_for_videos(xml_data)
        
        for vid in videos:
            vid_id = vid["video_id"]
            if vid_id not in processed_ids and vid_id not in pending_ids:
                vid["channel_name"] = channel_name
                vid["status"] = "pending"
                vid["added_at"] = datetime.now().isoformat()
                queue["pending"].append(vid)
                pending_ids.add(vid_id)
                new_videos_found += 1
                print(f"  + 신규 영상 감지: {vid['title']}")
                
    if new_videos_found > 0:
        save_json(QUEUE_FILE, queue)
        print(f"총 {new_videos_found}개의 신규 영상을 뽀개기 대기열(Queue)에 추가했습니다.")
    else:
        print("신규 영상이 없습니다.")
        
    print("=== 감시 종료 ===")

if __name__ == "__main__":
    # 실행 시 즉시 감시
    run_watcher()
