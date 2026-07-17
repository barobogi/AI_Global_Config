import os
import json
import asyncio
from playwright.async_api import async_playwright

COOKIE_PATH = r"D:\AI\.secrets\byteplus_cookies.json"

async def main():
    os.makedirs(os.path.dirname(COOKIE_PATH), exist_ok=True)
    
    print("BytePlus 수동 로그인 및 쿠키 저장 스크립트 시작 (구글 감지 우회 적용)")
    async with async_playwright() as p:
        # 자동화 브라우저 표시(AutomationControlled) 기능 해제
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # navigator.webdriver 값을 undefined로 덮어씌워 봇 감지 우회
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        page = await context.new_page()
        
        # BytePlus 로그인 페이지 이동
        await page.goto("https://console.byteplus.com/login")
        
        print("\n[안내] 우회 옵션이 적용된 브라우저가 실행되었습니다.")
        print("구글 로그인 버튼을 눌러 다시 시도해 주세요.")
        print("로그인이 성공적으로 완료되면 콘솔 창으로 돌아와 [Enter] 키를 눌러주세요.")
        
        # 사용자 대기
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, input, "로그인을 마치셨다면 Enter를 누르세요...")
        
        # 쿠키 획득 및 저장
        cookies = await context.cookies()
        with open(COOKIE_PATH, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
            
        print(f"\n[성공] 쿠키 파일이 안전하게 저장되었습니다: {COOKIE_PATH}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
