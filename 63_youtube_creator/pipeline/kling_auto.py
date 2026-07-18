import os
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

COOKIE_PATH = r"D:\AI\.secrets\kling_cookies.json"
STATE_PATH = r"D:\AI\.secrets\kling_state.json"
TARGET_URL = "https://kling.ai/app/image/new"

async def generate_scene_image(prompt_text, output_path):
    """
    Kling AI 무료 플랜의 Playwright 자동화를 통해 이미지를 생성한다.
    byteplus_auto.py와 동일한 인터페이스를 유지한다.
    """
    print(f"\n========== Kling AI 이미지 생성 (Playwright) ==========")
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(COOKIE_PATH):
        print(f"  - [오류] 인증 쿠키가 없습니다: {COOKIE_PATH}")
        return False

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--window-size=1920,1080"]
        )
        context = await browser.new_context(
            storage_state=STATE_PATH if os.path.exists(STATE_PATH) else None,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        page = await context.new_page()

        try:
            print("  - Kling AI 접속 중...")
            await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(3)

            page_screenshot = str(Path(output_path).parent / "kling_debug.png")
            await page.screenshot(path=page_screenshot)
            print(f"  - 디버그 스크린샷 저장: {page_screenshot}")

            prompt_box = None
            try:
                # 1. 텍스트 에어리어 최후의 수단 (가장 마지막에 있는 textarea가 보통 프롬프트 창임)
                locator = page.locator("textarea").last
                await locator.wait_for(state="visible", timeout=15000)
                prompt_box = locator
                print("    입력창 발견: textarea.last")
            except Exception:
                try:
                    # 2. 플레이스홀더 기반 검색
                    locator = page.get_by_placeholder("describe the image").first
                    await locator.wait_for(state="visible", timeout=15000)
                    prompt_box = locator
                    print("    입력창 발견: placeholder")
                except Exception:
                    pass

            if not prompt_box:
                print("  - [오류] 입력창을 찾지 못했습니다")
                await browser.close()
                return False

            await prompt_box.click(force=True)
            await prompt_box.fill(prompt_text)
            await asyncio.sleep(1.5)

            send_button = None
            try:
                btn = page.get_by_role("button", name="Generate").first
                if await btn.is_visible(timeout=5000):
                    send_button = btn
                    print("    전송 버튼 발견: get_by_role(Generate)")
            except Exception:
                try:
                    btn = page.locator("button:has-text('Generate'), button:has-text('생성')").first
                    if await btn.is_visible(timeout=5000):
                        send_button = btn
                        print("    전송 버튼 발견: has-text")
                except Exception:
                    pass

            # 버튼 클릭 전, 기존에 존재하는 이미지 목록 수집 (오탐지 방지)
            initial_imgs = await page.evaluate("""
                () => {
                    return Array.from(document.querySelectorAll('img')).map(img => img.src);
                }
            """)

            if send_button:
                await send_button.click()
            else:
                await prompt_box.press("Enter")
                print("    Enter로 전송 시도")

            print("  - 이미지 생성 대기 중 (최대 120초)...")
            await asyncio.sleep(15)

            found_id = None
            for _ in range(30):
                found_id = await page.evaluate("""
                    (initial) => {
                        const imgs = Array.from(document.querySelectorAll('img'));
                        const new_imgs = imgs.filter(img => img.naturalWidth >= 500 && img.src && !initial.includes(img.src));
                        if (new_imgs.length > 0) {
                            const img = new_imgs[new_imgs.length - 1];
                            img.id = 'kling-generated-target';
                            return 'kling-generated-target';
                        }
                        return null;
                    }
                """, initial_imgs)
                
                if found_id:
                    break
                await asyncio.sleep(6)

            if not found_id:
                print("  - [오류] 생성된 이미지 결과를 확인하지 못했습니다 (타임아웃)")
                error_screenshot = str(Path(output_path).parent / "kling_error.png")
                await page.screenshot(path=error_screenshot)
                print(f"  - 에러 상황 스크린샷 저장: {error_screenshot}")
                await browser.close()
                return False

            # 요소 자체를 스크린샷 캡처하여 저장 (CORS 보안 에러 완벽 우회)
            img_locator = page.locator(f"#{found_id}")
            # 이미지가 화면에 보이도록 스크롤 (필요한 경우)
            await img_locator.scroll_into_view_if_needed()
            await img_locator.screenshot(path=output_path)
            
            print(f"  - [성공] 이미지 저장: {output_path}")
            await browser.close()
            return True

        except Exception as e:
            print(f"  - [오류] Playwright 자동화 예외 발생: {e}")
            await browser.close()
            return False


if __name__ == "__main__":
    print("Kling AI 이미지 생성 단독 테스트 실행")
    asyncio.run(generate_scene_image("Futuristic AI robot in a dark tech lab, blue neon glow, cinematic, 3D render, masterpiece", r"D:\AI\63_youtube_creator\pipeline\output\kling_test.jpg"))
