import os
import json
import asyncio
from pathlib import Path
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

        async def handle_modal():
            """Agreements 모달이 있으면 체크 + confirm"""
            try:
                cb = page.locator("input[type='checkbox']").first
                await cb.wait_for(state="visible", timeout=5000)
                await cb.check()
                await asyncio.sleep(0.5)
                await page.locator("button:has-text('confirm')").click()
                print("  - [모달 통과] 약관 동의 완료!")
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(2)
            except Exception:
                pass  # 모달 없으면 그냥 통과

        try:
            # 1. Overview 접속 → 모달 처리
            print("  - Overview 접속...")
            await page.goto("https://console.byteplus.com/ark/region:ap-southeast-1/overview",
                            wait_until="networkidle", timeout=40000)
            await asyncio.sleep(2)
            await handle_modal()

            # 2. Playground Image 접속 → 또 모달 처리
            print("  - [1/4] Playground Image 접속...")
            await page.goto("https://console.byteplus.com/ark/region:ap-southeast-1/playground/image",
                            wait_until="networkidle", timeout=40000)
            await asyncio.sleep(2)
            await handle_modal()
            await asyncio.sleep(2)

            # 3. 프롬프트 입력
            print("  - [2/4] 프롬프트 입력...")
            # 다양한 selector 시도
            textarea = None
            for sel in ["textarea[placeholder*='prompt' i]", "textarea[placeholder*='Enter']", "textarea", ".arco-textarea"]:
                try:
                    el = page.locator(sel).first
                    await el.wait_for(state="visible", timeout=5000)
                    textarea = el
                    print(f"    textarea 찾음: {sel}")
                    break
                except Exception:
                    continue

            if not textarea:
                await page.screenshot(path=str(Path(output_path).parent / "debug_no_textarea.png"))
                print("  - [오류] textarea 못 찾음 — 스크린샷 저장")
                await browser.close()
                return False

            await textarea.fill(prompt_text)
            await asyncio.sleep(1)

            # Generate 버튼
            print("  - [3/4] Generate 버튼 클릭...")
            for sel in ["button:has-text('Generate')", "button:has-text('generate')", "[class*='generate']"]:
                try:
                    btn = page.locator(sel).first
                    await btn.wait_for(state="visible", timeout=5000)
                    await btn.click()
                    break
                except Exception:
                    continue

            # 4. 결과 이미지 대기
            print("  - [4/4] AI 렌더링 대기 중 (최대 60초)...")
            # 생성이 완료되면 화면 우측 결과 영역에 이미지가 뜸
            # 기존 이미지와 구분하기 위해 생성 전/후 요소 갯수 비교도 가능하나, 일단 넉넉히 대기
            img_locator = page.locator(".arco-image-img").last
            await img_locator.wait_for(state="visible", timeout=60000)
            
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
