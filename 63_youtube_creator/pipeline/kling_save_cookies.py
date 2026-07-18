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

        print("\n[안내] 브라우저가 열렸습니다. 구글/이메일 로그인을 완료해주세요.")
        print("로그인이 성공하여 작업실(URL: /app/image/new)에 입장하면 5초 후 자동으로 세션이 저장됩니다!")
        
        try:
            # 작업실 URL로 이동할 때까지 최대 120초 대기
            await page.wait_for_url("**/app/image/new*", timeout=120000)
            print("\n[감지] 작업실 진입 확인! 스토리지 로딩 대기 중 (5초)...")
            await page.wait_for_timeout(5000)
        except Exception as e:
            print("\n[실패] 시간 초과(120초) 또는 URL 감지 실패:", e)
            await browser.close()
            return

        await context.storage_state(path=STATE_PATH)

        print(f"\n[성공] 브라우저 상태(쿠키+로컬스토리지) 저장 완료: {STATE_PATH}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
