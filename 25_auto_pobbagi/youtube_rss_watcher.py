import urllib.request
import xml.etree.ElementTree as ET
import json
import os
import subprocess
from datetime import datetime

QUEUE_FILE = r"D:\AI\25_auto_pobbagi\youtube_queue.json"
CHANNELS_FILE = r"D:\AI\25_auto_pobbagi\channels.json"
QUOTA = 15       # 일일 총 할당량
PER_CHANNEL = 3  # 채널당 최대 등록 수

DEFAULT_CHANNELS = {
    "UCd1-XlZkK5D8ZgUvXqH-r2A": "기술노트 with 알렉",
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
    
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"[오류] XML 파싱 실패: {e}")
        return videos
        
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'yt': 'http://www.youtube.com/xml/schemas/2015'
    }
    
    for entry in root.findall('atom:entry', ns):
        try:
            video_id = entry.find('yt:videoId', ns).text
            title = entry.find('atom:title', ns).text
            videos.append({"video_id": video_id, "title": title})
        except Exception as e:
            print(f"[오류] 엔트리 파싱 실패: {e}")
            continue
            
    return videos

def fetch_fallback_videos(channel_id, count=3):
    # yt-dlp를 이용해 채널의 전체 영상 중 인기순으로 상위 가져오기 (Fallback)
    # --playlist-end 30 으로 대략 가져온 뒤 처리.
    print(f"  [Fallback] {channel_id} 채널에서 과거 명작 발굴 중...")
    cmd = [
        "yt-dlp",
        "--print", "%(id)s|%(title)s",
        "--playlist-end", "10",
        "--extractor-args", "youtube:player_client=default", 
        f"https://www.youtube.com/channel/{channel_id}"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        videos = []
        for line in result.stdout.strip().split('\n'):
            if '|' in line:
                vid_id, title = line.split('|', 1)
                videos.append({"video_id": vid_id, "title": title})
        return videos
    except Exception as e:
        print(f"  [Fallback 오류] {e}")
        return []

def safe_print(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('utf-8', errors='replace').decode('ascii', errors='replace'))

def run_watcher():
    print(f"=== 유튜브 RSS 자동 감시 시작 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    
    channels = load_json(CHANNELS_FILE, DEFAULT_CHANNELS)
    queue = load_json(QUEUE_FILE, {"pending": [], "processed": [], "waiting_review": []})
    
    processed_raw = queue.get("processed", [])
    processed_ids = set(
        v["video_id"] if isinstance(v, dict) else v for v in processed_raw
    )
    pending_ids = set(v["video_id"] for v in queue.get("pending", []))
    review_ids = set(v["video_id"] for v in queue.get("waiting_review", []))
    
    all_known_ids = processed_ids | pending_ids | review_ids
    
    new_videos_found = 0
    
    # 1차: RSS로 신작 수집 (채널당 최대 PER_CHANNEL개)
    for channel_id, channel_name in channels.items():
        if new_videos_found >= QUOTA:
            break

        print(f"[{channel_name}] 신규 영상 감지 중...")
        xml_data = fetch_channel_rss(channel_id)
        videos = parse_rss_for_videos(xml_data)

        channel_count = 0
        for vid in videos:
            vid_id = vid["video_id"]
            if vid_id not in all_known_ids and new_videos_found < QUOTA and channel_count < PER_CHANNEL:
                vid["channel_name"] = channel_name
                vid["status"] = "pending"
                queue["pending"].append(vid)
                all_known_ids.add(vid_id)
                new_videos_found += 1
                channel_count += 1
                safe_print(f"  + 신규 영상 추가: {vid['title']}")

    # 2차: 할당량 미달 시 Fallback (채널당 PER_CHANNEL 이내)
    if new_videos_found < QUOTA:
        print(f"할당량({QUOTA}개) 미달. 과거 명작 발굴(Fallback)을 시작합니다...")
        for channel_id, channel_name in channels.items():
            if new_videos_found >= QUOTA:
                break

            fallback_videos = fetch_fallback_videos(channel_id)
            channel_count = 0
            for vid in fallback_videos:
                vid_id = vid["video_id"]
                if vid_id not in all_known_ids and new_videos_found < QUOTA and channel_count < PER_CHANNEL:
                    vid["channel_name"] = channel_name
                    vid["status"] = "pending"
                    vid["fallback"] = True
                    queue["pending"].append(vid)
                    all_known_ids.add(vid_id)
                    new_videos_found += 1
                    channel_count += 1
                    safe_print(f"  + 명작 발굴 추가: {vid['title']}")
                    
    save_json(QUEUE_FILE, queue)
    print(f"총 {new_videos_found}개의 영상을 뽀개기 큐에 등록했습니다.")
    print("=== 감시 및 큐잉 완료 ===")

if __name__ == "__main__":
    run_watcher()
