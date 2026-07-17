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

    print("BytePlus Seedream 이미지 생성 자동화 (인간 타이핑 모방 딜레이 적용)")
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
        
        # Tiptap 에디터 입력 및 전송 버튼 클릭
        try:
            # 에디터 내부의 실제 paragraph (p) 태그 또는 에디터 본체 포커스
            editor_p = page.locator(".tiptap.ProseMirror p").first
            editor_main = page.locator(".tiptap.ProseMirror")
            
            print("에디터 포커싱 (p 태그 클릭)...")
            if await editor_p.count() > 0:
                await editor_p.click()
            else:
                await editor_main.click()
            await page.wait_for_timeout(1000)
            
            # 실제 인간의 타이핑 속도를 모사하기 위해 글자당 80ms 딜레이 부여
            prompt = "A cybernetic green frog sitting on a gold coin, 3d render, high detail, masterpiece"
            print(f"인간 타이핑 모방 입력 중 (딜레이 80ms): {prompt}")
            await page.keyboard.type(prompt, delay=80)
            await page.wait_for_timeout(2000) # 타이핑 후 상태 변경 대기
            
            # 디버깅용 현재 입력 상태 화면 캡처
            await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_after_typing.png")
            print("타이핑 완료 직후 화면 스크린샷 저장")
            
            # 전송 버튼 활성화 상태 체크 (최대 5초 대기)
            submit_btn = page.locator("[data-testid='image-sender-submit-button']")
            print("전송 버튼 활성화 여부 확인 중...")
            button_activated = False
            for i in range(10):
                is_disabled = await submit_btn.evaluate("btn => btn.disabled")
                if not is_disabled:
                    print("전송 버튼 활성화 완료!")
                    button_activated = True
                    break
                print(f"버튼 대기 중 ({i+1}/10)...")
                # 버튼 비활성화를 풀기 위해 추가적인 스페이스바 입력도 시도해봅니다.
                await page.keyboard.type(" ")
                await page.wait_for_timeout(500)
            
            if button_activated:
                print("전송 버튼 클릭 격발...")
                await submit_btn.click()
                await page.wait_for_timeout(5000)
                
                # 생성 중 화면 스크린샷
                generating_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generating.png"
                await page.screenshot(path=generating_screenshot)
                print(f"생성 중 화면 스크린샷 저장: {generating_screenshot}")
                
                # 생성 대기 (대략 30초)
                print("생성 완료 대기 중 (30초)...")
                await page.wait_for_timeout(30000)
                
                # 완성 화면 캡처
                done_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_done.png"
                await page.screenshot(path=done_screenshot)
                print(f"완성 화면 스크린샷 저장: {done_screenshot}")
            else:
                print("오류: 전송 버튼이 여전히 활성화되지 않았습니다.")
                await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generate_error.png")
            
        except Exception as e:
            print(f"작업 처리 중 오류 발생: {e}")
            await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generate_error.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
