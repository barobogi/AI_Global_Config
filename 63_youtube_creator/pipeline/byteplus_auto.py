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

    print("BytePlus 입력 폼 요소 분석 시작")
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
        
        # 페이지 내의 다양한 입력 요소 로깅
        print("--- 페이지 내 텍스트 입력 가능 요소 스캔 ---")
        
        # contenteditable=true 분석
        ce_count = await page.locator("[contenteditable='true']").count()
        print(f"contenteditable='true' 요소 개수: {ce_count}")
        for i in range(ce_count):
            el = page.locator("[contenteditable='true']").nth(i)
            tag = await el.evaluate("el => el.tagName")
            cls = await el.evaluate("el => el.className")
            placeholder = await el.evaluate("el => el.getAttribute('placeholder')")
            print(f"[{i}] Tag: {tag}, Class: {cls}, Placeholder: {placeholder}")

        # textarea 분석
        ta_count = await page.locator("textarea").count()
        print(f"textarea 요소 개수: {ta_count}")
        for i in range(ta_count):
            el = page.locator("textarea").nth(i)
            cls = await el.evaluate("el => el.className")
            placeholder = await el.evaluate("el => el.getAttribute('placeholder')")
            print(f"[{i}] Class: {cls}, Placeholder: {placeholder}")

        # input 분석
        inp_count = await page.locator("input").count()
        print(f"input 요소 개수: {inp_count}")
        for i in range(inp_count):
            el = page.locator("input").nth(i)
            typ = await el.evaluate("el => el.type")
            cls = await el.evaluate("el => el.className")
            placeholder = await el.evaluate("el => el.getAttribute('placeholder')")
            print(f"[{i}] Type: {typ}, Class: {cls}, Placeholder: {placeholder}")

        # 'Enter your prompt' 텍스트를 담고 있는 모든 요소 분석
        prompt_txt_count = await page.locator("text='Enter your prompt'").count()
        print(f"'Enter your prompt' 텍스트 포함 요소 개수 (일부 일치): {prompt_txt_count}")
        # 좀 더 넓은 조건 검색
        prompt_elements = page.locator("div, span, p, label").filter(has_text="Enter your prompt")
        pe_count = await prompt_elements.count()
        print(f"'Enter your prompt' 필터링 요소 개수: {pe_count}")
        for i in range(min(pe_count, 5)):
            el = prompt_elements.nth(i)
            tag = await el.evaluate("el => el.tagName")
            cls = await el.evaluate("el => el.className")
            text = await el.inner_text()
            print(f"[{i}] Tag: {tag}, Class: {cls}, Text: {text[:50]}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
