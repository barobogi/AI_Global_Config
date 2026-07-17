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

    print("BytePlus Playground 접속 및 Seedream 카드 클릭 테스트 시작")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        with open(COOKIE_PATH, "r", encoding="utf-8") as f:
            cookies = json.load(f)
            await context.add_cookies(cookies)

        page = await context.new_page()
        
        # Overview 페이지로 이동
        print("Overview 페이지로 이동 중...")
        await page.goto("https://console.byteplus.com/ark/region:ap-southeast-1/overview", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        
        # 동의 팝업 처리
        try:
            checkbox_selector = "text=I am a developer using BytePlus"
            if await page.locator(checkbox_selector).count() > 0:
                await page.locator(checkbox_selector).click()
                await page.wait_for_timeout(1000)
                await page.locator("button:has-text('confirm')").click()
                await page.wait_for_timeout(2000)
        except Exception:
            pass

        # 비기너 가이드 팝업 닫기 (Escape)
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1000)

        # 왼쪽 메뉴에서 Playground 클릭
        print("Playground 메뉴 클릭 중...")
        await page.locator("text=Playground").first.click()
        await page.wait_for_timeout(4000)
        
        # Dola-Seedream-5.0-pro 카드 클릭 시도
        print("Dola-Seedream-5.0-pro 카드 클릭 중...")
        try:
            # 텍스트가 들어 있는 요소를 직접 타겟팅
            seedream_card = "text=Dola-Seedream-5.0-pro"
            await page.locator(seedream_card).first.click()
            await page.wait_for_timeout(5000)
            print(f"Seedream 클릭 후 URL: {page.url}")
            
            # 스크린샷 저장
            screenshot_seedream = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_detail.png"
            await page.screenshot(path=screenshot_seedream)
            print(f"Seedream 상세 페이지 스크린샷 저장: {screenshot_seedream}")
        except Exception as e:
            print(f"카드 클릭 실패: {e}")
            await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_click_error.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
