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

    print("BytePlus Seedream 이미지 생성 자동화 (XPath 버튼 클릭 및 생성 검증) 테스트")
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
        print("Overview 페이지로 이동...")
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
        await page.locator("text=Playground").first.click()
        await page.wait_for_timeout(4000)
        
        # 상단 "Image" 탭 클릭
        image_tab = page.locator("div, span, button").filter(has_text="Image").first
        await image_tab.click()
        await page.wait_for_timeout(4000)
        
        # Tiptap ProseMirror 입력창 타겟팅 및 프롬프트 입력
        print("Tiptap 에디터에 포커싱 후 타이핑...")
        try:
            editor = page.locator(".tiptap.ProseMirror")
            await editor.click()
            await page.wait_for_timeout(1000)
            
            prompt = "A cybernetic green frog sitting on a gold coin, 3d render, high detail, masterpiece"
            await page.keyboard.type(prompt)
            await page.wait_for_timeout(2000)
            
            # XPath를 이용하여 에디터의 부모 컨테이너 내부에 존재하는 버튼 매칭
            # ProseMirror 클래스를 가진 div의 조상 div들 중에서 버튼을 가지고 있는 범위를 타겟팅
            print("XPath 기반 전송 버튼 탐색...")
            submit_btn = page.locator("xpath=//div[contains(@class, 'ProseMirror')]/ancestor::div[contains(@class, 'card') or contains(@class, 'input') or contains(@class, 'container') or position() < 5]//button").last
            
            # 만약 위 XPath가 실패할 경우, 텍스트 상자 주변의 모든 버튼을 후보로 찾음
            if await submit_btn.count() > 0:
                print("조상 영역에서 매핑된 버튼 발견. 클릭 진행...")
                await submit_btn.click()
            else:
                # 대안: 전체 버튼 중 입력창 높이(Y좌표) 부근에 있는 보라색 화살표 버튼을 클릭
                print("XPath 버튼 발견 실패, 대체 수단으로 Control+Enter 전송 시도...")
                await page.keyboard.press("Control+Enter")
                await page.wait_for_timeout(1000)
                # 여전히 격발이 안 되었다면 Enter만 입력
                await page.keyboard.press("Enter")
                
            await page.wait_for_timeout(5000)
            
            # 생성 중 화면 스크린샷
            generating_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generating.png"
            await page.screenshot(path=generating_screenshot)
            print(f"생성 중 화면 스크린샷 저장: {generating_screenshot}")
            
            # 완전히 생성될 때까지 대기 (약 25초 - 이미지 생성에 필요한 일반적 시간)
            print("완성 대기 중 (25초)...")
            await page.wait_for_timeout(25000)
            
            # 완성 화면 캡처
            done_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_done.png"
            await page.screenshot(path=done_screenshot)
            print(f"완성 화면 스크린샷 저장: {done_screenshot}")
            
        except Exception as e:
            print(f"이미지 생성 작업 중 오류 발생: {e}")
            await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generate_error.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
