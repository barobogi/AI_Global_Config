import os
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

COOKIE_PATH = r"D:\AI\.secrets\kling_cookies.json"
STATE_PATH = r"D:\AI\.secrets\kling_state.json"

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
            await page.goto("https://kling.ai/app/image/new", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(3)

            page_screenshot = str(Path(output_path).parent / "kling_debug.png")
            await page.screenshot(path=page_screenshot)
            print(f"  - 디버그 스크린샷 저장: {page_screenshot}")

            prompt_box = None
            for selector in [
                "textarea",
                "[contenteditable='true']",
                "[role='textbox']",
                "input[type='text']",
            ]:
                try:
                    locator = page.locator(selector).first
                    await locator.wait_for(state="visible", timeout=30000)
                    prompt_box = locator
                    print(f"    입력창 발견: {selector}")
                    break
                except Exception:
                    continue

            if not prompt_box:
                print("  - [오류] 입력창을 찾지 못했습니다")
                await browser.close()
                return False

            await prompt_box.click(force=True)
            await prompt_box.fill(prompt_text)
            await asyncio.sleep(1.5)

            send_button = None
            for selector in [
                "text='생성'",
                "text='Generate'",
                "button:has-text('생성')",
                "button:has-text('Generate')",
                "button[type='submit']",
                "[class*='generate']",
            ]:
                try:
                    btn = page.locator(selector).first
                    if await btn.is_visible(timeout=2000):
                        send_button = btn
                        print(f"    전송 버튼 발견: {selector}")
                        break
                except Exception:
                    continue

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

            image_base64 = None
            for _ in range(30):
                base64_data = await page.evaluate("""
                    (initial) => {
                        const imgs = Array.from(document.querySelectorAll('img'));
                        const new_imgs = imgs.filter(img => img.naturalWidth >= 500 && img.src && !initial.includes(img.src));
                        if (new_imgs.length > 0) {
                            const img = new_imgs[new_imgs.length - 1];
                            const canvas = document.createElement('canvas');
                            canvas.width = img.naturalWidth;
                            canvas.height = img.naturalHeight;
                            const ctx = canvas.getContext('2d');
                            ctx.drawImage(img, 0, 0);
                            return canvas.toDataURL('image/jpeg', 0.95);
                        }
                        return null;
                    }
                """, initial_imgs)
                
                if base64_data:
                    image_base64 = base64_data
                    break
                await asyncio.sleep(6)

            if not image_base64:
                print("  - [오류] 생성된 이미지 결과를 확인하지 못했습니다 (타임아웃)")
                error_screenshot = str(Path(output_path).parent / "kling_error.png")
                await page.screenshot(path=error_screenshot)
                print(f"  - 에러 상황 스크린샷 저장: {error_screenshot}")
                await browser.close()
                return False

            import base64
            # "data:image/jpeg;base64,....." 포맷에서 헤더 제거
            header, encoded = image_base64.split(",", 1)
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(encoded))
            
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
