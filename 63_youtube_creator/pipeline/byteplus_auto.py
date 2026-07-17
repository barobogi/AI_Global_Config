import os
import json
import asyncio
from playwright.async_api import async_playwright

COOKIE_PATH = r"D:\AI\.secrets\byteplus_cookies.json"

async def generate_scene_image(prompt_text, output_path):
    """
    만복의 지시(비용 0원 달성)에 따라 Playwright를 이용한 웹 매크로 스크래핑 방식으로 원상 복구 및 디버깅 롤백.
    """
    print(f"\n========== 웹 매크로 스크래핑 렌더링 (Playwright) ==========")
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(COOKIE_PATH):
        print(f"  - [오류] 인증 쿠키가 없습니다: {COOKIE_PATH}")
        return False

    async with async_playwright() as p:
        # Headless=True로 백그라운드 구동 (디버깅 시 False)
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--window-size=1920,1080"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        with open(COOKIE_PATH, "r", encoding="utf-8") as f:
            cookies = json.load(f)
            await context.add_cookies(cookies)

        page = await context.new_page()
        
        try:
            # 1. Overview 페이지로 최초 접속
            print("  - Overview 페이지 접속 (인증 초기화)...")
            await page.goto("https://console.byteplus.com/ark/region:ap-southeast-1/overview", wait_until="networkidle", timeout=30000)
            
            # 방해꾼 모달 통과 (Agreements 체크 및 confirm 클릭)
            try:
                print("  - [모달 체크] 약관 동의 모달 확인 중...")
                checkbox = page.locator("input[type='checkbox']").first
                if await checkbox.is_visible(timeout=5000):
                    await checkbox.check()
                    await asyncio.sleep(0.5)
                    await page.locator("button:has-text('confirm')").click()
                    print("  - [모달 통과] 약관 동의 완료!")
                    await asyncio.sleep(2)
            except Exception as e:
                print("  - [모달 체크] 모달 없음, 패스.")
            
            # 2. Playground 진입 (메뉴 클릭)
            print("  - [1/4] Playground 메뉴 클릭...")
            await page.locator("text='Playground'").click()
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)
            
            # 3. Image 탭 강제 전환
            print("  - [2/4] Image 탭 전환...")
            try:
                # 'Image' 텍스트를 가진 탭 버튼 클릭
                await page.locator("div.arco-tabs-header-title:has-text('Image')").click(timeout=5000)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"    - 탭 클릭 실패, JS 라우팅 우회 시도: {e}")
                # 강제로 URL 해시/경로를 변경할 수 있으면 시도 (단순 클릭 우회)
                await page.evaluate("document.querySelectorAll('.arco-tabs-header-title').forEach(el => { if(el.innerText.includes('Image')) el.click(); })")
                await asyncio.sleep(2)

            # 3. 프롬프트 입력 및 전송
            print("  - [3/4] 프롬프트 입력 및 렌더링 요청...")
            # textarea를 찾아서 입력
            textarea = page.locator("textarea[placeholder*='Enter prompt']").first
            await textarea.fill(prompt_text)
            await asyncio.sleep(1)
            
            # Generate 버튼 클릭 (보통 'Generate' 텍스트가 있는 버튼)
            gen_btn = page.locator("button:has-text('Generate')").first
            await gen_btn.click()
            
            # 4. 결과 이미지 대기 및 스크래핑
            print("  - [4/4] AI 렌더링 대기 중 (최대 40초)...")
            # 생성이 완료되면 화면 우측 결과 영역에 이미지가 뜸
            # 기존 이미지와 구분하기 위해 생성 전/후 요소 갯수 비교도 가능하나, 일단 넉넉히 대기
            img_locator = page.locator(".arco-image-img").last
            await img_locator.wait_for(state="visible", timeout=40000)
            
            # 이미지 URL (src) 추출
            img_src = await img_locator.get_attribute("src")
            if img_src:
                import urllib.request
                urllib.request.urlretrieve(img_src, output_path)
                print(f"  - [성공] 실사 이미지 스크래핑 및 저장 완료: {output_path}")
                await browser.close()
                return True
            else:
                print("  - [오류] 이미지 src를 찾을 수 없습니다.")
                await page.screenshot(path=os.path.join(output_dir, "debug_error.png"))
                await browser.close()
                return False

        except Exception as e:
            print(f"  - [오류] Playwright 자동화 예외 발생: {e}")
            await page.screenshot(path=os.path.join(output_dir, "debug_error.png"))
            await browser.close()
            return False

if __name__ == "__main__":
    print("웹 매크로 스크래핑 단독 테스트 실행")
    asyncio.run(generate_scene_image("A cute little robot waving hand, 3d render, masterpiece", r"D:\AI\63_youtube_creator\pipeline\output\test_playwright.jpg"))
