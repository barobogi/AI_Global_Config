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

    print("BytePlus 전송 버튼 정밀 분석 시작")
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
        await page.goto("https://console.byteplus.com/ark/region:ap-southeast-1/overview", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        
        try:
            checkbox_selector = "text=I am a developer using BytePlus"
            if await page.locator(checkbox_selector).count() > 0:
                await page.locator(checkbox_selector).click()
                await page.wait_for_timeout(1000)
                await page.locator("button:has-text('confirm')").click()
                await page.wait_for_timeout(2000)
        except Exception:
            pass

        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1000)

        await page.locator("text=Playground").first.click()
        await page.wait_for_timeout(4000)
        
        image_tab = page.locator("div, span, button").filter(has_text="Image").first
        await image_tab.click()
        await page.wait_for_timeout(4000)
        
        # ProseMirror 에디터 주변의 모든 버튼을 탐색하여 로깅
        buttons_info = await page.evaluate("""() => {
            const editor = document.querySelector('.tiptap.ProseMirror');
            if (!editor) return '에디터를 찾을 수 없음';
            
            // 에디터의 부모 컨테이너(보통 입력 카드 컴포넌트)
            let parent = editor.parentElement;
            // 위로 4단계까지 부모를 찾아 올라가며 그 안의 모든 버튼을 탐색
            for (let i = 0; i < 4; i++) {
                if (parent && parent.parentElement) {
                    parent = parent.parentElement;
                }
            }
            
            const buttons = parent.querySelectorAll('button');
            const result = [];
            buttons.forEach((btn, idx) => {
                const rect = btn.getBoundingClientRect();
                result.push({
                    index: idx,
                    tagName: btn.tagName,
                    className: btn.className,
                    id: btn.id,
                    text: btn.innerText,
                    html: btn.outerHTML.substring(0, 200), // 앞부분 200자만
                    disabled: btn.disabled,
                    x: rect.x,
                    y: rect.y,
                    width: rect.width,
                    height: rect.height
                });
            });
            return result;
        }""")
        
        print("--- 에디터 부근 버튼 스캔 결과 ---")
        if isinstance(buttons_info, str):
            print(buttons_info)
        else:
            for btn in buttons_info:
                print(f"[{btn['index']}] Text: '{btn['text']}', Disabled: {btn['disabled']}, Class: {btn['className']}")
                print(f"    Coords: x={btn['x']}, y={btn['y']}, w={btn['width']}, h={btn['height']}")
                print(f"    HTML: {btn['html']}")
                print("-" * 50)
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
