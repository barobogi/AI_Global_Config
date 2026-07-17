import os
import json
import asyncio
from playwright.async_api import async_playwright

COOKIE_PATH = r"D:\AI\.secrets\byteplus_cookies.json"

async def main():
    if not os.path.exists(COOKIE_PATH):
        print(f"오류: 쿠키 파일을 찾을 수 없습니다. 경로: {COOKIE_PATH}")
        return

    print("BytePlus 수동 모델 활성화 보조 도구 시작")
    async with async_playwright() as p:
        # 일반 창(headless=False)으로 띄움
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # 쿠키 적용
        with open(COOKIE_PATH, "r", encoding="utf-8") as f:
            cookies = json.load(f)
            await context.add_cookies(cookies)

        page = await context.new_page()
        
        # 모델 활성화(ComputerVision) 페이지로 곧장 이동
        activation_url = "https://console.byteplus.com/ark/region:ap-southeast-1/openManagement?tab=ComputerVision"
        print(f"모델 활성화 관리 페이지로 이동 중: {activation_url}")
        await page.goto(activation_url, wait_until="networkidle")
        
        print("\n[안내] 띄워진 브라우저 창에서 다음 작업을 수행해 주세요:")
        print("1. 'Dola-Seedream-5.0-pro' 모델 행의 우측에 있는 [Activate] 버튼을 클릭해 주세요.")
        print("2. 팝업창이 나타나면 다음 두 체크박스를 클릭(체크)해 주세요:")
        print("   - 'Enable Free Credits Only Mode'")
        print("   - 'I have read and agree to BytePlus Customer Agreement...' (약관 동의)")
        print("3. 파란색 [Confirm activation and authorization] 버튼을 클릭해 주세요.")
        print("\n모든 승인이 완료되어 활성화 상태로 변경되면, 콘솔 창으로 돌아와 [Enter] 키를 눌러주세요.")
        print("쿠키를 새로고침하여 최종 저장하겠습니다.")

        # 사용자 엔터 입력 대기
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, input, "활성화를 모두 완료하셨다면 Enter를 누르세요...")

        # 최신 로그인/활성화 쿠키 수집 및 업데이트
        cookies = await context.cookies()
        with open(COOKIE_PATH, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
            
        print(f"\n[성공] 활성화 세션 쿠키가 최신 상태로 갱신되었습니다: {COOKIE_PATH}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
