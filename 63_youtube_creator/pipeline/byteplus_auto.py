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

    print("BytePlus Seedream 이미지 생성 자동화 (예제 정밀 바인딩) 테스트")
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
        print("Playground 메뉴 클릭...")
        await page.locator("text=Playground").first.click()
        await page.wait_for_timeout(4000)
        
        # 상단 "Image" 탭 클릭
        print("상단 Image 탭 클릭...")
        image_tab = page.locator("div, span, button").filter(has_text="Image").first
        await image_tab.click()
        await page.wait_for_timeout(4000)
        
        try:
            # 1. 예제 이미지 카드 정밀 타겟팅 및 클릭
            print("예제 이미지 카드 정밀 클릭 시도...")
            # 'Try the following example' 텍스트 아래에 존재하는 그리드 내의 첫 번째 img 태그 타겟팅
            example_img = page.locator("xpath=//div[contains(text(), 'Try the following example')]/following-sibling::div//img").first
            
            if await example_img.count() > 0:
                await example_img.click()
                print("예제 이미지 클릭 성공.")
                await page.wait_for_timeout(3000)
            else:
                print("XPath 예제 이미지를 찾을 수 없어 일반 예제 영역 매핑 시도...")
                # 백업: 단순 텍스트 매칭
                await page.locator("text=Sketch-to-Image").first.click()
                await page.wait_for_timeout(3000)
                
            # 만약 다른 메뉴가 눌려서 팝업이 떴을 경우를 대비해 팝업 닫기 시도
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(1000)
                
            # 2. 에디터 텍스트 비우기 및 새로운 프롬프트 타이핑
            editor = page.locator(".tiptap.ProseMirror")
            print("에디터 포커싱 및 기존 텍스트 전체 선택 후 삭제...")
            await editor.click()
            await page.wait_for_timeout(1000)
            
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.wait_for_timeout(1000)
            
            # 새 프롬프트 입력
            prompt = "A cybernetic green frog sitting on a gold coin, 3d render, high detail, masterpiece"
            print(f"새 프롬프트 입력 중: {prompt}")
            await page.keyboard.type(prompt, delay=50)
            await page.wait_for_timeout(2000)
            
            # 3. 전송 버튼 상태 체크
            submit_btn = page.locator("[data-testid='image-sender-submit-button']")
            is_disabled = await submit_btn.evaluate("btn => btn.disabled")
            print(f"전송 버튼 비활성화 상태: {is_disabled}")
            
            # 스크린샷 캡처
            after_binding_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_after_binding.png"
            await page.screenshot(path=after_binding_screenshot)
            print(f"바인딩 및 입력 완료 후 스크린샷 저장: {after_binding_screenshot}")
            
            # 만약 비활성화가 풀렸다면 클릭하여 이미지 생성 진행
            if not is_disabled:
                print("전송 버튼이 활성화되었습니다! 클릭 격발...")
                await submit_btn.click()
                await page.wait_for_timeout(5000)
                
                # 생성 중 스크린샷
                generating_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generating.png"
                await page.screenshot(path=generating_screenshot)
                print(f"생성 중 화면 스크린샷 저장: {generating_screenshot}")
                
                # 생성 완료 대기 (30초)
                print("생성 완료 대기 중 (30초)...")
                await page.wait_for_timeout(30000)
                
                # 완료 스크린샷
                done_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_done.png"
                await page.screenshot(path=done_screenshot)
                print(f"완성 화면 스크린샷 저장: {done_screenshot}")
            else:
                print("오류: 예제를 바인딩했음에도 전송 버튼이 여전히 활성화되지 않았습니다.")
                
        except Exception as e:
            print(f"작업 처리 중 오류 발생: {e}")
            await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generate_error.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
