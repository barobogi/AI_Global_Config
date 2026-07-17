import os
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

COOKIE_PATH = r"D:\AI\.secrets\byteplus_cookies.json"

async def main():
    if not os.path.exists(COOKIE_PATH):
        print(f"오류: 쿠키 파일을 찾을 수 없습니다. 경로: {COOKIE_PATH}")
        print("먼저 브라우저를 띄워 쿠키를 저장하는 과정이 필요합니다.")
        return

    print("BytePlus 자동화 테스트 시작 (Playwright)")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Load cookies
        try:
            with open(COOKIE_PATH, "r", encoding="utf-8") as f:
                cookies = json.load(f)
                await context.add_cookies(cookies)
            print("쿠키 로드 완료")
        except Exception as e:
            print(f"쿠키 로드 실패: {e}")

        page = await context.new_page()
        print("BytePlus 페이지로 이동 중...")
        
        # BytePlus Video/Image automation URL
        await page.goto("https://console.byteplus.com/login")

        # Wait to check if login is successful via cookies
        await page.wait_for_timeout(5000)
        
        # Take a screenshot to verify login state
        screenshot_path = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_login_test.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        await page.screenshot(path=screenshot_path)
        print(f"스크린샷 저장 완료 (로그인 상태 확인용): {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
