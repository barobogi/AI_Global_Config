import os
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright

QUEUE_FILE = r"D:\AI\25_auto_pobbagi\youtube_queue.json"
OUTPUT_DIR = r"D:\AI\25_auto_pobbagi\transcripts"

def clean_xml_transcript(xml_data):
    """유튜브에서 받은 XML 자막 데이터를 순수 텍스트로 정제합니다."""
    try:
        root = ET.fromstring(xml_data)
        text_lines = []
        for text_elem in root.findall('text'):
            if text_elem.text:
                # HTML 엔티티 제거 및 불필요한 공백 제거
                clean_text = text_elem.text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
                clean_text = re.sub(r'<[^>]+>', '', clean_text)
                text_lines.append(clean_text.strip())
        return " ".join(text_lines)
    except Exception as e:
        print(f"XML 파싱 오류: {e}")
        return None

def extract_transcript_playwright(video_id):
    """
    Playwright를 사용하여 실제 브라우저를 띄우고, YouTube 봇 차단(429)을 우회합니다.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    output_path = os.path.join(OUTPUT_DIR, f"{video_id}.txt")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"[{video_id}] Playwright 무적 우회 모드로 자막 추출 시도 중...")
    
    with sync_playwright() as p:
        # 헤드리스 모드로 실행 (UI 없이 백그라운드에서 동작)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        try:
            # 타임아웃 30초 설정 및 페이지 로드 대기
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # YouTube는 페이지 내에 ytInitialPlayerResponse 객체를 통해 자막 URL을 제공함
            # 페이지에 객체가 로드될 때까지 짧게 대기
            page.wait_for_function("typeof ytInitialPlayerResponse !== 'undefined'", timeout=15000)
            
            player_response = page.evaluate("ytInitialPlayerResponse")
            
            captions = player_response.get("captions", {})
            if not captions:
                print(f"[{video_id}] 자막이 없는 영상입니다.")
                browser.close()
                return None
                
            track_list = captions.get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
            if not track_list:
                print(f"[{video_id}] 자막 트랙을 찾을 수 없습니다.")
                browser.close()
                return None
                
            # 한국어 자막(ko)을 우선적으로 찾고, 없으면 첫 번째 자막 선택
            selected_track = None
            for track in track_list:
                if track.get("languageCode") == "ko":
                    selected_track = track
                    break
            
            if not selected_track:
                selected_track = track_list[0]
                
            subtitle_url = selected_track.get("baseUrl")
            
            if subtitle_url:
                # Playwright의 APIRequestContext를 사용하여 브라우저 세션(쿠키, 헤더)을 유지한 채로 XML 다운로드
                response = context.request.get(subtitle_url)
                if response.ok:
                    xml_data = response.text()
                    
                    # XML 정제하여 텍스트로 변환
                    clean_text = clean_xml_transcript(xml_data)
                    
                    if clean_text:
                        with open(output_path, "w", encoding="utf-8") as f:
                            f.write(clean_text)
                        print(f"[{video_id}] 자막 추출 완벽 성공! -> {output_path}")
                        browser.close()
                        return output_path
                else:
                    print(f"[{video_id}] 자막 다운로드 실패 (상태 코드: {response.status})")
                    
            print(f"[{video_id}] 자막 URL 추출에 실패했습니다.")
            
        except Exception as e:
            print(f"[{video_id}] Playwright 처리 중 오류 발생: {e}")
            
        browser.close()
        return None

def run_extractor():
    if not os.path.exists(QUEUE_FILE):
        print("대기열 파일이 없습니다.")
        return
        
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)
        
    pending = queue.get("pending", [])
    if not pending:
        print("추출 대기 중인 영상이 없습니다.")
        return
        
    print(f"총 {len(pending)}개의 영상에 대해 Playwright 자막 추출을 시작합니다.")
    
    remaining = []
    for vid in pending:
        video_id = vid["video_id"]
        result_file = extract_transcript_playwright(video_id)
        
        if result_file:
            vid["transcript_path"] = result_file
            vid["status"] = "extracted"
            queue.setdefault("processed", []).append(vid)
        else:
            vid["status"] = "failed"
            remaining.append(vid)
            
    queue["pending"] = remaining
    
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=4)
        
    print("=== Playwright 무적 자막 추출 작업 종료 ===")

if __name__ == "__main__":
    run_extractor()
