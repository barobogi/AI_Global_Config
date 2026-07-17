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
            """Agreements 모달이 있으면 JS 강제 클릭으로 체크 + confirm"""
            try:
                cb = page.locator("input[type='checkbox']").first
                await cb.wait_for(state="attached", timeout=5000)
                # JS 강제 클릭 (SPA 방어막 우회)
                await page.evaluate("document.querySelector('input[type=checkbox]').click()")
                await asyncio.sleep(0.8)
                await page.evaluate("""
                    var btns = document.querySelectorAll('button');
                    for(var b of btns){ if(b.textContent.trim().toLowerCase()==='confirm'){b.click();break;} }
                """)
                print("  - [모달 통과] JS 강제 클릭 완료!")
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(2)
            except Exception:
                pass

        try:
            # 1. Overview 접속 → 모달 처리
            print("  - Overview 접속...")
            await page.goto("https://console.byteplus.com/ark/region:ap-southeast-1/overview",
                            wait_until="networkidle", timeout=40000)
            await asyncio.sleep(2)
            await handle_modal()

            # 2. Playground Image 접속
            print("  - [1/4] Playground Image 접속...")
            await page.goto("https://console.byteplus.com/ark/region:ap-southeast-1/playground/image",
                            wait_until="networkidle", timeout=40000)
            await asyncio.sleep(2)

            # 약관 모달 또 뜨면 처리
            await handle_modal()

            # 투어 안내 모달 닫기 (Next → Get started 반복 클릭)
            try:
                for _ in range(5):
                    # "Get started" 버튼이 있으면 클릭 후 종료
                    gs = page.locator("button:has-text('Get started')")
                    if await gs.is_visible(timeout=1000):
                        await gs.click()
                        print("  - [투어 모달] Get started 클릭 완료")
                        await asyncio.sleep(1)
                        break
                    # "Next" 버튼 클릭
                    nb = page.locator("button:has-text('Next')")
                    if await nb.is_visible(timeout=1000):
                        await nb.click()
                        await asyncio.sleep(0.5)
            except Exception:
                pass

            await asyncio.sleep(1)

            # 투어 모달 통과 후 — Overview 하단 Image generation 카드 클릭
            if "playground/image" not in page.url:
                print("  - Image generation 카드 클릭...")
                try:
                    # Overview 하단 카드 클릭
                    await page.locator("text='Image generation'").first.click(timeout=5000)
                    await page.wait_for_load_state("networkidle")
                    await asyncio.sleep(3)
                    print(f"  - 이동 후 URL: {page.url}")
                except Exception:
                    # 메뉴 Playground 클릭
                    try:
                        await page.locator("text='Playground'").first.click(timeout=3000)
                        await asyncio.sleep(2)
                        await page.locator("text='Image'").first.click(timeout=3000)
                        await page.wait_for_load_state("networkidle")
                        await asyncio.sleep(3)
                    except Exception as e:
                        print(f"  - 이동 실패: {e}")
            await asyncio.sleep(2)

            # 3. Image 탭 → 모델 선택 → 프롬프트 입력
            print("  - [2/4] Image 탭 선택...")
            try:
                await page.locator("button:has-text('Image'), [role='tab']:has-text('Image')").first.click(timeout=5000)
                await asyncio.sleep(1.5)
                # 모델 선택 목록이 나오면 Seedream 클릭
                mdl = page.locator("text='Dola-Seedream-5.0-pro'").first
                if await mdl.is_visible(timeout=3000):
                    await mdl.click()
                    print("  - 모델 Seedream-5.0-pro 선택")
                    await asyncio.sleep(2)
            except Exception:
                pass

            print("  - [3/4] 프롬프트 입력...")
            input_el = None
            for sel in ["textarea", "[contenteditable='true']", "[role='textbox']"]:
                try:
                    el = page.locator(sel).first
                    await el.wait_for(state="visible", timeout=4000)
                    input_el = el
                    print(f"    입력창: {sel}")
                    break
                except Exception:
                    continue

            if not input_el:
                await page.screenshot(path=str(Path(output_path).parent / "debug_no_textarea.png"))
                await browser.close()
                return False

            await input_el.click()
            await input_el.fill(prompt_text)
            await asyncio.sleep(1)

            # 전송 버튼 클릭
            print("  - [3/4] 전송 버튼 클릭...")
            sent = False
            for sel in ["button[class*='send']", "[class*='send-btn']", "button[type='submit']",
                        "button:has-text('Generate')", "[class*='submit']"]:
                try:
                    btn = page.locator(sel).first
                    if await btn.is_visible(timeout=2000):
                        await btn.click()
                        sent = True
                        print(f"    전송: {sel}")
                        break
                except Exception:
                    continue
            if not sent:
                await input_el.press("Enter")
                print("    Enter 키로 전송")

            # 4. 결과 이미지 대기 (채팅 응답에 생성된 이미지)
            print("  - [4/4] AI 렌더링 대기 중 (최대 90초)...")
            await asyncio.sleep(3)
            img_locator = None
            for img_sel in [
                ".arco-image-img",
                "img[src*='tos-s']",
                "img[src*='byteplus']",
                "[class*='message'] img",
                "[class*='result'] img",
                "img[class*='image']",
            ]:
                try:
                    loc = page.locator(img_sel).last
                    await loc.wait_for(state="visible", timeout=90000)
                    img_locator = loc
                    print(f"    결과 이미지: {img_sel}")
                    break
                except Exception:
                    continue

            if not img_locator:
                await page.screenshot(path=os.path.join(output_dir, "debug_error.png"))
                print("  - [오류] 결과 이미지 못 찾음")
                await browser.close()
                return False

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
