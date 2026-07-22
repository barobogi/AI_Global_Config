import os
import time
import asyncio
from playwright.async_api import async_playwright

STATE_PATH = r"D:\AI\.secrets\roboneo_state.json"
DEBUG_IMG = r"C:\Users\82102\.gemini\antigravity\brain\e13a19ad-5a8a-437a-ae63-e0a85249a912\roboneo_debug.png"

async def generate_scene_image(prompt: str, output_path: str):
    print("=" * 50)
    print(f"[RoboNeo Auto] 이미지 생성 시작 (v0.2 Playwright Test)")
    print(f"프롬프트: {prompt}")
    print("=" * 50)
    
    if not os.path.exists(STATE_PATH):
        print(f"[오류] 쿠키 파일({STATE_PATH})이 없습니다. 수동 로그인 스크립트를 먼저 실행해주세요.")
        return False

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(
            storage_state=STATE_PATH,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        page = await context.new_page()
        print("  - RoboNeo 접속 중...")
        try:
            await page.goto("https://roboneo.com", wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(5000)  # React 렌더링 대기
            
            # 현재 화면 캡처하여 아티팩트로 저장 (UI 구조 파악용)
            await page.screenshot(path=DEBUG_IMG)
            print(f"  - 디버그 스크린샷 저장 완료: {DEBUG_IMG}")
            
            # 모든 textarea 요소들의 정보를 출력해본다.
            textareas = await page.locator("textarea").all()
            print(f"  - 발견된 textarea 개수: {len(textareas)}")
            
            # TODO: 실제 프롬프트 입력 및 생성 로직은 UI 캡처 확인 후 구현 예정
            
        except Exception as e:
            print(f"  - [오류] {str(e)}")
            await page.screenshot(path=DEBUG_IMG)
            await browser.close()
            return False

        await browser.close()
    
    # 지금은 테스트이므로 빈 파일만 생성
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(b"mock_video_data_from_roboneo")
        
    print("[RoboNeo Auto] 디버그 실행 완료!")
    return True

def generate_video_via_roboneo(prompt: str, output_path: str):
    return asyncio.run(generate_scene_image(prompt, output_path))

if __name__ == "__main__":
    test_prompt = "A cinematic shot of a futuristic AI managing data streams, blue and orange neon lights, 16:9"
    test_output = os.path.join(os.path.dirname(__file__), "output", "roboneo_test_output.mp4")
    generate_video_via_roboneo(test_prompt, test_output)
