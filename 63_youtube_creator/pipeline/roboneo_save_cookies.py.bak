import os
import json
import asyncio
from playwright.async_api import async_playwright

STATE_PATH = r"D:\AI\.secrets\roboneo_state.json"


async def main():
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)

    print("RoboNeo 수동 로그인 및 쿠키 저장 스크립트 시작")
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
        # 로보네오 메인 페이지 또는 작업실로 이동
        await page.goto("https://roboneo.com", wait_until="domcontentloaded", timeout=60000)

        print("\n[안내] 브라우저가 열렸습니다. 구글/이메일 로그인을 완료해주세요.")
        
        # Tkinter 팝업으로 로그인 완료 대기
        import tkinter as tk
        from tkinter import messagebox
        
        def show_popup():
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            return messagebox.askyesno("RoboNeo 로그인 확인", "로그인을 모두 완료하셨나요?\n로그인 후 작업 화면이 보이면 '예(Yes)'를 클릭해주세요.")
            
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, show_popup)
        
        if result:
            print("\n[감지] 사용자가 완료를 눌렀습니다. 스토리지 저장 중...")
        else:
            print("\n[취소] 사용자가 취소를 눌렀습니다.")
            await browser.close()
            return

        await context.storage_state(path=STATE_PATH)

        print(f"\n[성공] 브라우저 상태(쿠키+로컬스토리지) 저장 완료: {STATE_PATH}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
