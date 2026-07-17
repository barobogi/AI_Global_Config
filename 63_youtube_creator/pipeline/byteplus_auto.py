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

    print("BytePlus Seedream 최종 이미지 생성 자동화 테스트 시작 (활성화 생략)")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
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
        print("Playground 메뉴 클릭...")
        await page.locator("text=Playground").first.click()
        await page.wait_for_timeout(4000)
        
        # 상단 "Image" 탭 클릭
        print("상단 Image 탭 클릭...")
        image_tab = page.locator("div, span, button").filter(has_text="Image").first
        await image_tab.click()
        await page.wait_for_timeout(5000) # 탭 전환 대기
        
        # 2. 이미지 예제 바인딩 및 생성 진행 (곧바로 직행)
        try:
            print("예제 이미지 바인딩 및 새 프롬프트 주입...")
            example_img = page.locator("xpath=//div[contains(text(), 'Try the following example')]/following-sibling::div//img").first
            if await example_img.count() > 0:
                print("예제 템플릿 이미지 클릭 바인딩...")
                await example_img.evaluate("el => el.click()")
                await page.wait_for_timeout(3000)
            else:
                await page.locator("text=Sketch-to-Image").first.evaluate("el => el.click()")
                await page.wait_for_timeout(3000)
                
            # 텍스트 교체
            editor = page.locator(".tiptap.ProseMirror")
            await editor.click(force=True)
            await page.wait_for_timeout(1000)
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.wait_for_timeout(1000)
            
            prompt = "A cybernetic green frog sitting on a gold coin, 3d render, high detail, masterpiece"
            await page.keyboard.type(prompt, delay=50)
            await page.wait_for_timeout(3000)
            
            # 전송 버튼 클릭
            submit_btn = page.locator("[data-testid='image-sender-submit-button']")
            is_disabled = await submit_btn.evaluate("btn => btn.disabled")
            print(f"전송 버튼 비활성화 상태 (최종): {is_disabled}")
            
            if not is_disabled:
                print("전송 버튼이 활성화되었습니다! 클릭 격발...")
                await submit_btn.evaluate("el => el.click()")
                await page.wait_for_timeout(5000)
                
                # 생성 중 스크린샷
                generating_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generating.png"
                await page.screenshot(path=generating_screenshot)
                print(f"생성 중 화면 스크린샷 저장: {generating_screenshot}")
                
                # 생성 완료 대기 (25초)
                print("생성 완료 대기 중 (25초)...")
                await page.wait_for_timeout(25000)
                
                # 완료 스크린샷
                done_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_done.png"
                await page.screenshot(path=done_screenshot)
                print(f"완성 화면 스크린샷 저장: {done_screenshot}")
            else:
                print("오류: 전송 버튼이 여전히 활성화되지 않았습니다. 현재 화면 상태 저장 중...")
                await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generate_error.png")
                
        except Exception as e:
            print(f"이미지 생성 프로세스 오류: {e}")
            await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generate_error.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
