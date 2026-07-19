import time
from playwright.sync_api import sync_playwright

def test_scrape():
    video_id = "L94yAQR9VvA"
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            locale="ko-KR"
        )
        page = context.new_page()
        
        # 네트워크 응답 가로채기
        transcript_data = []
        def handle_response(response):
            if "api/timedtext" in response.url:
                print(f"\n[가로채기 성공] 자막 URL: {response.url[:100]}...\n")
                try:
                    text = response.text()
                    transcript_data.append(text)
                except Exception as e:
                    print("응답 읽기 실패:", e)
                    
        page.on("response", handle_response)
        
        print(f"[{video_id}] 접속 중...")
        page.goto(url, wait_until="networkidle")
        
        print("더보기 버튼 클릭 시도...")
        try:
            expand_btn = page.locator("tp-yt-paper-button#expand").first
            if expand_btn.is_visible():
                expand_btn.click()
                time.sleep(1)
        except Exception as e:
            print("더보기 실패:", e)
            
        print("스크립트 표시 버튼 클릭 시도...")
        try:
            transcript_btn = page.locator("button:has-text('스크립트 표시')").first
            if transcript_btn.is_visible():
                transcript_btn.click()
                print("스크립트 버튼 클릭! API 응답 대기 중 (5초)...")
                page.wait_for_timeout(5000)
            else:
                print("스크립트 표시 버튼 안 보임.")
        except Exception as e:
            print("스크립트 버튼 실패:", e)
            
        if transcript_data:
            print(f"성공적으로 자막을 가로챘습니다! (길이: {len(transcript_data[0])})")
            print(transcript_data[0][:300])
        else:
            print("자막 API 요청이 없었습니다.")
            
        browser.close()

if __name__ == "__main__":
    test_scrape()
