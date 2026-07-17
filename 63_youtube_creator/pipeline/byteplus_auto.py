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
        
        # 1. Overview 대시보드로 이동
        print("Overview 페이지로 이동 중...")
        await page.goto("https://console.byteplus.com/ark/region:ap-southeast-1/overview", wait_until="networkidle")
        await page.wait_for_timeout(5000)
        
        # 2. 동의 팝업 처리
        try:
            checkbox_selector = "text=I am a developer using BytePlus"
            if await page.locator(checkbox_selector).count() > 0:
                print("약관 동의 팝업 감지. 체크박스 클릭...")
                await page.locator(checkbox_selector).click()
                await page.wait_for_timeout(1000)
                
                confirm_btn = "button:has-text('confirm')"
                if await page.locator(confirm_btn).count() > 0:
                    await page.locator(confirm_btn).click()
                    print("confirm 버튼 클릭 완료.")
                    await page.wait_for_timeout(3000)
        except Exception as e:
            print(f"동의 팝업 처리 오류: {e}")

        # 3. 비기너 가이드 팝업 닫기 (Escape 키 전송)
        print("비기너 가이드 팝업 닫기 시도 (Escape 키)...")
        try:
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(2000)
            
            # Escape로 안 닫힐 것을 대비해 가이드 팝업 내 닫기(X) 버튼 감지 및 클릭도 병행
            # "ModelArk 3.0 Beginner Guide" 다이얼로그 안의 svg 버튼 등
            close_btn = page.locator("div[role='dialog'] button").first
            if await close_btn.count() > 0 and await close_btn.is_visible():
                print("다이얼로그 닫기 버튼(X) 감지. 클릭...")
                await close_btn.click()
                await page.wait_for_timeout(2000)
        except Exception as e:
            print(f"가이드 팝업 닫기 시도 오류: {e}")

        # 4. 왼쪽 메뉴에서 Playground 클릭
        print("Playground 메뉴 클릭 시도...")
        try:
            playground_menu = "text=Playground"
            await page.locator(playground_menu).first.click()
            await page.wait_for_timeout(5000)
            print(f"Playground 이동 성공. 현재 URL: {page.url}")
            
            # 스크린샷 저장
            screenshot_playground = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_playground_real.png"
            await page.screenshot(path=screenshot_playground)
            print(f"Playground 내부 스크린샷 저장: {screenshot_playground}")
        except Exception as e:
            print(f"Playground 메뉴 클릭 실패: {e}")
            await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_playground_click_error_2.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
