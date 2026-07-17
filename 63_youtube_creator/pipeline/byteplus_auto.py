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

    print("BytePlus Seedream 이미지 생성 자동화 테스트 시작")
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
        
        # 상단 "Image" 탭 클릭하여 Seedream 진입
        print("상단 Image 탭 클릭 중...")
        image_tab = page.locator("div, span, button").filter(has_text="Image").first
        await image_tab.click()
        await page.wait_for_timeout(4000)
        
        # 프롬프트 입력 영역 탐색 및 텍스트 주입
        print("프롬프트 입력 중...")
        try:
            # placeholder 속성을 포함하는 textarea나 div를 찾음
            prompt_input = page.locator("textarea, [placeholder*='Enter your prompt']").first
            await prompt_input.click()
            await prompt_input.fill("A cybernetic green frog sitting on a gold coin, 3d render, high detail, masterpiece")
            await page.wait_for_timeout(1000)
            
            # 생성(전송) 버튼 클릭 또는 Enter 전송
            # 여기서는 Enter 키를 눌러 생성 명령 전송
            print("엔터 전송하여 이미지 생성 격발...")
            await prompt_input.press("Enter")
            await page.wait_for_timeout(5000)
            
            # 생성 대기 상태 캡처
            generating_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generating.png"
            await page.screenshot(path=generating_screenshot)
            print(f"생성 중 화면 스크린샷 저장: {generating_screenshot}")
            
            # 완전히 생성될 때까지 충분히 대기 (약 20초)
            print("완성 대기 중 (20초)...")
            await page.wait_for_timeout(20000)
            
            # 완성 화면 캡처
            done_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_done.png"
            await page.screenshot(path=done_screenshot)
            print(f"완성 화면 스크린샷 저장: {done_screenshot}")
            
        except Exception as e:
            print(f"이미지 생성 조작 실패: {e}")
            await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generate_error.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
