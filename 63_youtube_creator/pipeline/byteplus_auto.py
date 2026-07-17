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

    print("BytePlus Seedream 이미지 생성 자동화 (Tiptap 에디터 입력) 테스트 시작")
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
        
        # 상단 "Image" 탭 클릭
        print("상단 Image 탭 클릭 중...")
        image_tab = page.locator("div, span, button").filter(has_text="Image").first
        await image_tab.click()
        await page.wait_for_timeout(4000)
        
        # Tiptap ProseMirror 입력창 타겟팅 및 프롬프트 입력
        print("Tiptap 에디터 입력창에 포커싱 후 프롬프트 타이핑 중...")
        try:
            editor = page.locator(".tiptap.ProseMirror")
            await editor.click()
            await page.wait_for_timeout(1000)
            
            # 실제 키보드로 입력하는 효과
            prompt = "A cybernetic green frog sitting on a gold coin, 3d render, high detail, masterpiece"
            await page.keyboard.type(prompt)
            await page.wait_for_timeout(2000)
            
            # 생성(전송) 버튼 찾기
            # Tiptap 입력 영역 부근의 버튼들 중에서 전송 버튼을 유추
            # 스크린샷 상 보라색 원형 위쪽 화살표 버튼
            print("전송 버튼 탐색 및 클릭 시도...")
            
            # 에디터 부모 노드 내의 모든 버튼 탐색
            # parent: .tiptap.ProseMirror 의 상위 div나 wrapper
            # 혹은 전체 페이지 내 button 중 svg가 포함된 보라색 원형 스타일의 버튼을 찾음
            # 우선, enter 키로 전송이 안 될 때를 대비해 특정 버튼을 찾아 클릭
            button_locator = page.locator("button").filter(has=page.locator("svg"))
            btn_count = await button_locator.count()
            print(f"SVG 포함 버튼 개수: {btn_count}")
            
            # 전송 버튼은 통상 입력창 내의 마지막 또는 특정 보라색 계열일 가능성이 큼
            # 텍스트 입력창 바로 우측 하단에 위치한 버튼 클릭 시도 (일반적으로 마지막 인덱스 부근)
            if btn_count > 0:
                # 마지막 버튼을 클릭해 봅니다 (보통 에디터 끝에 전송 버튼이 붙음)
                await button_locator.last.click()
                print("마지막 SVG 버튼 클릭 완료.")
            else:
                # 버튼을 찾지 못했다면 Enter 전송 시도
                print("버튼 감지 실패, Enter 키 전송 시도...")
                await editor.press("Enter")
                
            await page.wait_for_timeout(5000)
            
            # 생성 중 화면 스크린샷
            generating_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generating.png"
            await page.screenshot(path=generating_screenshot)
            print(f"생성 중 화면 스크린샷 저장: {generating_screenshot}")
            
            # 완전히 생성될 때까지 대기 (약 15초)
            print("완성 대기 중 (15초)...")
            await page.wait_for_timeout(15000)
            
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
