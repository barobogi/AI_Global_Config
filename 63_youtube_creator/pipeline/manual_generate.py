import os
import json
import asyncio
from playwright.async_api import async_playwright

COOKIE_PATH = r"D:\AI\.secrets\byteplus_cookies.json"

async def main():
    if not os.path.exists(COOKIE_PATH):
        print(f"오류: 쿠키 파일을 찾을 수 없습니다. 경로: {COOKIE_PATH}")
        return

    print("BytePlus 수동 이미지 생성 및 최종 검증 도구 시작")
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
        
        # 이미지 플레이그라운드 페이지로 직행
        playground_url = "https://console.byteplus.com/ark/region:ap-southeast-1/playground"
        print(f"플레이그라운드 페이지로 이동 중: {playground_url}")
        await page.goto(playground_url, wait_until="load")
        
        print("\n[안내] 띄워진 브라우저 창에서 다음 최종 작업을 직접 완료해 주세요:")
        print("1. 화면에 약관 팝업이나 가이드 모달이 뜬다면 마우스로 [Confirm] 또는 닫기(X)를 눌러서 걷어내 주세요.")
        print("2. 상단 [Image] 탭으로 이동해 주세요.")
        print("3. 좌측 상단 드롭다운에서 모델을 [Dola-Seed-2.1-turbo] 로 변경해 주세요.")
        print("4. 프롬프트 창에 다음 내용을 입력하고 오른쪽 [전송 화살표(↑)]를 눌러 그림을 그려주세요:")
        print("   -> 프롬프트: A cybernetic green frog sitting on a gold coin, 3d render, high detail, masterpiece")
        print("5. 그림 생성이 완벽히 성공한 것을 확인하신 후, 이 콘솔 창으로 돌아와 [Enter] 키를 누르시면 완료됩니다!")

        # 사용자 엔터 입력 대기
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, input, "이미지 생성 완료 확인 후 Enter를 누르세요...")

        # 최종 쿠키 저장
        cookies = await context.cookies()
        with open(COOKIE_PATH, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
            
        print("\n[성공] 최종 쿠키를 저장하고 세션을 성공적으로 닫았습니다.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
