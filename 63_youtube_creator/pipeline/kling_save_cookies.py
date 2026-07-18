# Kling AI 쿠키 저장용 Playwright 스크립트
import os
import json
import asyncio
from playwright.async_api import async_playwright

STATE_PATH = r"D:\AI\.secrets\kling_state.json"


async def main():
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)

    print("Kling AI 수동 로그인 및 쿠키 저장 스크립트 시작")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--window-size=1920,1080"],
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        page = await context.new_page()
        await page.goto("https://kling.ai/create/image", wait_until="domcontentloaded", timeout=60000)

        print("\n[안내] 브라우저가 열렸습니다.")
        print("구글 로그인으로 Kling AI에 접속한 뒤, 콘솔에서 Enter를 눌러주세요.")
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, input, "로그인을 마치셨다면 Enter를 누르세요...")

        await context.storage_state(path=STATE_PATH)

        print(f"\n[성공] 브라우저 상태(쿠키+로컬스토리지) 저장 완료: {STATE_PATH}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
