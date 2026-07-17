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

    print("BytePlus 'Activate now' 링크 정밀 요소 분석 시작")
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
        
        # 상세 팝업 오픈
        await page.locator("img").first.click()
        await page.wait_for_timeout(2000)
        
        # 'Activate now' 요소를 찾아서 DOM 트리 역추적 및 속성 출력
        element_details = await page.evaluate("""() => {
            const el = document.evaluate("//span[text()='Activate now']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (!el) return '요소를 찾을 수 없음';
            
            const details = [];
            let current = el;
            
            // 위로 5단계 부모 노드까지의 정보를 로깅
            for (let i = 0; i < 5; i++) {
                if (!current) break;
                
                const attrs = {};
                for (let attr of current.attributes) {
                    attrs[attr.name] = attr.value;
                }
                
                details.push({
                    depth: i,
                    tagName: current.tagName,
                    className: current.className,
                    attributes: attrs,
                    text: current.innerText,
                    html: current.outerHTML.substring(0, 300)
                });
                current = current.parentElement;
            }
            return details;
        }""")
        
        print("--- 'Activate now' 요소 및 부모 트리 분석 ---")
        if isinstance(element_details, str):
            print(element_details)
        else:
            for node in element_details:
                print(f"Depth {node['depth']}: <{node['tagName']}> Class: '{node['className']}'")
                print(f"    Attributes: {node['attributes']}")
                print(f"    HTML: {node['html']}")
                print("-" * 50)
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
