import os
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

COOKIE_PATH = r"D:\AI\.secrets\byteplus_cookies.json"

async def main():
    if not os.path.exists(COOKIE_PATH):
        print(f"오류: 쿠키 파일을 찾을 수 없습니다. 경로: {COOKIE_PATH}")
        return

    print("BytePlus Playground 접속 테스트 시작 (Playwright)")
    async with async_playwright() as p:
        # 우회 옵션 적용 및 헤드리스 브라우저 실행
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # navigator.webdriver 우회 주입
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Load cookies
        try:
            with open(COOKIE_PATH, "r", encoding="utf-8") as f:
                cookies = json.load(f)
                await context.add_cookies(cookies)
            print("쿠키 로드 성공")
        except Exception as e:
            print(f"쿠키 로드 실패: {e}")

        page = await context.new_page()
        
        # 1. 로그인 여부 확인을 위해 메인 콘솔로 접근
        print("BytePlus 콘솔 메인 페이지로 이동 중...")
        await page.goto("https://console.byteplus.com/", wait_until="networkidle")
        await page.wait_for_timeout(5000)
        
        # 현재 URL 확인
        current_url = page.url
        print(f"현재 URL: {current_url}")
        
        # 스크린샷 저장
        screenshot_path = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_console_main.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        await page.screenshot(path=screenshot_path)
        print(f"메인 페이지 스크린샷 저장: {screenshot_path}")

        # 2. ModelArk 또는 Playground 주소 후보군 접근
        # (통상적인 BytePlus AI/ModelArk Playground 주소로 이동 시도)
        playground_url = "https://console.byteplus.com/ark/playground"
        print(f"Playground 후보 주소로 이동 중: {playground_url}")
        try:
            await page.goto(playground_url, wait_until="networkidle", timeout=45000)
            await page.wait_for_timeout(5000)
            print(f"이동 후 URL: {page.url}")
            screenshot_playground = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_playground.png"
            await page.screenshot(path=screenshot_playground)
            print(f"Playground 페이지 스크린샷 저장: {screenshot_playground}")
        except Exception as e:
            print(f"Playground 이동 오류: {e}")
            # 대체 스크린샷 저장
            err_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_playground_error.png"
            await page.screenshot(path=err_screenshot)
            print(f"에러 시점 스크린샷 저장: {err_screenshot}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
