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

    print("BytePlus Playground 탭 클릭 및 상세 확인 테스트 시작")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, http://go.microsoft.com/fwlink/?LinkID=286172) Chrome/120.0.0.0 Safari/537.36"
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
        
        # 1. 상단 "Image" 탭 클릭 시도
        print("상단 Image 탭 클릭 시도...")
        try:
            # Featured / Text / Image / Video 중 Image 매칭
            # 텍스트가 정확히 'Image'인 요소를 찾거나 혹은 div/span 중 클릭
            image_tab = page.locator("div, span, button").filter(has_text="Image").first
            await image_tab.click()
            await page.wait_for_timeout(3000)
            
            # 스크린샷 저장
            screenshot_image = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_playground_image_tab.png"
            await page.screenshot(path=screenshot_image)
            print(f"Image 탭 스크린샷 저장: {screenshot_image}")
        except Exception as e:
            print(f"Image 탭 클릭 실패: {e}")

        # 2. 상단 "Video" 탭 클릭 시도
        print("상단 Video 탭 클릭 시도...")
        try:
            video_tab = page.locator("div, span, button").filter(has_text="Video").first
            await video_tab.click()
            await page.wait_for_timeout(3000)
            
            # 스크린샷 저장
            screenshot_video = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_playground_video_tab.png"
            await page.screenshot(path=screenshot_video)
            print(f"Video 탭 스크린샷 저장: {screenshot_video}")
        except Exception as e:
            print(f"Video 탭 클릭 실패: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
