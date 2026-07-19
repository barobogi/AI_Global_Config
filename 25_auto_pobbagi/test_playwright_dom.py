import time
from playwright.sync_api import sync_playwright

def test_scrape():
    video_id = "L94yAQR9VvA"
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 한국어 환경으로 설정
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="ko-KR"
        )
        page = context.new_page()
        
        print(f"[{video_id}] 페이지 접속 중...")
        page.goto(url, wait_until="networkidle")
        
        # 1. 설명란 "더보기" 버튼 클릭 (strict mode 회피를 위해 .first 사용)
        print("설명란 더보기 버튼 찾는 중...")
        try:
            expand_btn = page.locator("tp-yt-paper-button#expand").first
            if expand_btn.is_visible():
                expand_btn.click()
                print("더보기 버튼 클릭 완료.")
                time.sleep(1)
        except Exception as e:
            print(f"더보기 버튼 클릭 실패: {e}")
            
        # 2. "스크립트 표시" 버튼 클릭
        print("스크립트 표시 버튼 찾는 중...")
        try:
            # 다양한 언어 대응 (한국어, 영어)
            transcript_btn = page.locator("button:has-text('스크립트 표시')").first
            if transcript_btn.is_visible():
                transcript_btn.click()
                print("스크립트 표시 버튼 클릭 완료.")
                time.sleep(2)
            else:
                transcript_btn_en = page.locator("button:has-text('Show transcript')").first
                if transcript_btn_en.is_visible():
                    transcript_btn_en.click()
                    print("Show transcript 버튼 클릭 완료.")
                    time.sleep(2)
                else:
                    print("자막 열기 버튼을 찾지 못했습니다.")
        except Exception as e:
            print(f"스크립트 표시 버튼 클릭 실패: {e}")
            
        # 3. 자막 텍스트 추출
        print("자막 컨테이너 탐색 중...")
        try:
            # 자막 패널이 로드될 때까지 대기
            page.wait_for_selector("ytd-transcript-segment-renderer", timeout=10000)
            segments = page.locator("ytd-transcript-segment-renderer .segment-text")
            count = segments.count()
            print(f"자막 조각 수: {count}")
            
            if count > 0:
                texts = []
                for i in range(count):
                    texts.append(segments.nth(i).inner_text())
                
                print("--- 추출된 자막 샘플 ---")
                print(" ".join(texts)[:500] + "...")
                print("-------------------------")
            else:
                print("자막 텍스트를 찾지 못했습니다.")
        except Exception as e:
            print(f"자막 추출 실패: {e}")
            
        browser.close()

if __name__ == "__main__":
    test_scrape()
