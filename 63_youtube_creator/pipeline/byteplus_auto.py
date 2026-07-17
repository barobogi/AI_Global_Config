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

    print("BytePlus Seedream 이미지 생성 자동화 (ProseMirror 이벤트 우회 적용)")
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
            editor = page.locator(".tiptap.ProseMirror")
            print("에디터 포커싱...")
            await editor.click()
            await page.wait_for_timeout(1000)
            
            prompt = "A cybernetic green frog sitting on a gold coin, 3d render, high detail, masterpiece"
            
            # JS를 사용해 ProseMirror 에디터 내용 주입 및 input 이벤트 강제 트리거
            print("JS 기반 ProseMirror 상태 주입 및 이벤트 강제 격발...")
            await page.evaluate("""(text) => {
                const editorEl = document.querySelector('.tiptap.ProseMirror');
                if (!editorEl) return;
                
                // 1. ProseMirror 자체 에디터 뷰(view)가 노출되어 있는 경우
                if (editorEl.pmView) {
                    const view = editorEl.pmView;
                    const state = view.state;
                    const tr = state.tr.insertText(text);
                    view.dispatch(tr);
                } else {
                    // 2. 일반 DOM 주입 및 이벤트 트리거
                    editorEl.innerHTML = `<p>${text}</p>`;
                    editorEl.dispatchEvent(new Event('input', { bubbles: true }));
                    editorEl.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }""", prompt)
            await page.wait_for_timeout(1000)
            
            # 에디터가 활성화 상태로 감지하도록 키보드 스페이스 한 칸 입력 추가 격발
            await page.keyboard.type(" ")
            await page.wait_for_timeout(1000)
            
            # 전송 버튼 활성화 상태 체크 (최대 5초 대기)
            submit_btn = page.locator("[data-testid='image-sender-submit-button']")
            print("전송 버튼 활성화 여부 확인 중...")
            for i in range(10):
                is_disabled = await submit_btn.evaluate("btn => btn.disabled")
                if not is_disabled:
                    print("전송 버튼 활성화 완료!")
                    break
                print(f"버튼 대기 중 ({i+1}/10)...")
                await page.wait_for_timeout(500)
            
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
            
        except Exception as e:
            print(f"작업 처리 중 오류 발생: {e}")
            await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generate_error.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
