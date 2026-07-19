import urllib.request
import xml.etree.ElementTree as ET
import re
from playwright.sync_api import sync_playwright

def clean_xml_transcript(xml_data):
    try:
        root = ET.fromstring(xml_data)
        text_lines = []
        for text_elem in root.findall('text'):
            if text_elem.text:
                clean_text = text_elem.text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
                clean_text = re.sub(r'<[^>]+>', '', clean_text)
                text_lines.append(clean_text.strip())
        return " ".join(text_lines)
    except Exception as e:
        print(f"XML 파싱 오류: {e}")
        return None

def test_scrape():
    video_id = "L94yAQR9VvA"
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        print(f"[{video_id}] 페이지 접속 중...")
        page.goto(url, wait_until="domcontentloaded")
        
        page.wait_for_function("typeof ytInitialPlayerResponse !== 'undefined'", timeout=15000)
        player_response = page.evaluate("ytInitialPlayerResponse")
        
        captions = player_response.get("captions", {})
        track_list = captions.get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
        
        if track_list:
            subtitle_url = track_list[0].get("baseUrl")
            print(f"추출된 URL: {subtitle_url[:50]}...")
            
            # 여기서 핵심: 브라우저 환경 내부에서 fetch를 실행하여 botguard 토큰과 헤더를 그대로 활용!
            print("브라우저 내에서 fetch 실행 중...")
            xml_data = page.evaluate(f'''async () => {{
                const res = await fetch("{subtitle_url}");
                if (!res.ok) throw new Error("Status: " + res.status);
                return await res.text();
            }}''')
            
            clean_text = clean_xml_transcript(xml_data)
            print("--- 자막 샘플 ---")
            print(clean_text[:500])
        else:
            print("자막 트랙 없음")
            
        browser.close()

if __name__ == "__main__":
    test_scrape()
