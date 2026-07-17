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

    print("BytePlus 전송 버튼 DOM 분석 시작")
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
        await page.goto("https://console.byteplus.com/ark/region:ap-southeast-1/overview", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        
        # 가이드/팝업 닫기
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1000)

        await page.locator("text=Playground").first.click()
        await page.wait_for_timeout(4000)
        
        image_tab = page.locator("div, span, button").filter(has_text="Image").first
        await image_tab.click()
        await page.wait_for_timeout(5000)
        
        # 예제 이미지 클릭
        example_img = page.locator("xpath=//div[contains(text(), 'Try the following example')]/following-sibling::div//img").first
        if await example_img.count() > 0:
            await example_img.evaluate("el => el.click()")
            await page.wait_for_timeout(2000)
            
        # 프롬프트 영역 주변의 모든 button, svg, span 요소를 분석
        buttons_info = await page.evaluate("""() => {
            const btns = document.querySelectorAll('button, div[role="button"], span');
            const result = [];
            btns.forEach(btn => {
                // 특정 아이콘을 포함하거나 텍스트가 가격 표시 근처인 것 필터링
                const text = btn.innerText || '';
                const html = btn.outerHTML || '';
                const testId = btn.getAttribute('data-testid') || '';
                
                // 전송 버튼과 연관 있어 보이는 클래스나 testid, html 수집
                if (testId.includes('sender') || testId.includes('submit') || html.includes('USD') || html.includes('svg')) {
                    if (result.length < 30) {
                        result.push({
                            tagName: btn.tagName,
                            className: btn.className,
                            dataTestId: testId,
                            text: text.substring(0, 100),
                            htmlSnippet: html.substring(0, 200)
                        });
                    }
                }
            });
            return result;
        }""")
        
        print("--- Playground 전송 버튼 의심 리스트 ---")
        for idx, btn in enumerate(buttons_info):
            print(f"[{idx}] Tag: <{btn['tagName']}> Class: '{btn['className']}' TestId: '{btn['dataTestId']}'")
            print(f"    Text: {btn['text']}")
            print(f"    HTML Snippet: {btn['htmlSnippet']}")
            print("-" * 50)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
