import os
import json
import asyncio
from playwright.async_api import async_playwright

COOKIE_PATH = r"D:\AI\.secrets\byteplus_cookies.json"

async def main():
    os.makedirs(os.path.dirname(COOKIE_PATH), exist_ok=True)
    
    print("BytePlus 수동 로그인 및 쿠키 저장 스크립트 시작")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # BytePlus 로그인 페이지 이동
        await page.goto("https://console.byteplus.com/login")
        
        print("\n[안내] 브라우저 창에서 BytePlus 로그인을 완료해 주세요.")
        print("로그인이 성공적으로 완료되면 콘솔 창으로 돌아와 [Enter] 키를 눌러주세요.")
        
        # 사용자 대기
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, input, "로그인을 마치셨다면 Enter를 누르세요...")
        
        # 쿠키 획득 및 저장
        cookies = await context.cookies()
        with open(COOKIE_PATH, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
            
        print(f"\n[성공] 쿠키 파일이 안전하게 저장되었습니다: {COOKIE_PATH}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
