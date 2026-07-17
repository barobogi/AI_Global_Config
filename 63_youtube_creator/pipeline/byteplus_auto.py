import os
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

COOKIE_PATH = r"D:\AI\.secrets\byteplus_cookies.json"
OUTPUT_DIR = r"D:\AI\63_youtube_creator\pipeline\output"

async def main():
    if not os.path.exists(COOKIE_PATH):
        print(f"오류: 쿠키 파일을 찾을 수 없습니다. 경로: {COOKIE_PATH}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("BytePlus Seedream-4.5 이미지 생성 자동화 (마우스 Bounding Box 클릭 보강)")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        with open(COOKIE_PATH, "r", encoding="utf-8") as f:
            cookies = json.load(f)
            await context.add_cookies(cookies)

        page = await context.new_page()
        
        # Overview 페이지로 이동
        print("Overview 페이지로 이동 중...")
        await page.goto("https://console.byteplus.com/ark/region:ap-southeast-1/overview", wait_until="load")
        await page.wait_for_timeout(5000)
        
        # 1차 동의 팝업 처리
        try:
            checkboxes = page.locator(".aml-arco-checkbox, input[type='checkbox']")
            if await checkboxes.count() > 0:
                await checkboxes.first.evaluate("el => el.click()")
                await page.wait_for_timeout(1000)
                await page.locator("button:has-text('confirm'), button:has-text('Confirm')").first.evaluate("el => el.click()")
                await page.wait_for_timeout(2000)
        except Exception:
            pass

        # Playground 클릭
        print("Playground 메뉴 클릭...")
        await page.locator("text=Playground").first.click(force=True)
        await page.wait_for_timeout(4000)
        
        # 2차 동의 팝업 처리
        try:
            modal_checkboxes = page.locator(".aml-arco-modal-wrapper .aml-arco-checkbox, .aml-arco-modal-wrapper input[type='checkbox']").first
            if await modal_checkboxes.count() > 0:
                await modal_checkboxes.evaluate("el => el.click()")
                await page.wait_for_timeout(1000)
                confirm_btn = page.locator(".aml-arco-modal-wrapper button:has-text('confirm'), .aml-arco-modal-wrapper button:has-text('Confirm')").first
                await confirm_btn.evaluate("el => el.click()")
                await page.wait_for_timeout(3000)
        except Exception:
            pass
            
        # 비기너 가이드 팝업 닫기 (Escape)
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1000)

        # 상단 "Image" 탭 클릭
        print("상단 Image 탭 클릭...")
        image_tab = page.locator("div, span, button").filter(has_text="Image").first
        await image_tab.click(force=True)
        await page.wait_for_timeout(5000)
        
        # 모델 변경 시도 (Bounding Box 기반 정밀 타격)
        try:
            print("드롭다운 Bounding Box 클릭 시도...")
            dropdown_target = page.locator(".aml-arco-select-view").first
            if await dropdown_target.count() > 0:
                box = await dropdown_target.bounding_box()
                if box:
                    # 박스의 정중앙을 마우스로 클릭
                    await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                    print("드롭다운 마우스 클릭 완료.")
                    await page.wait_for_timeout(2000)
            
            # 리스트 옵션 Bounding Box 클릭 시도
            print("옵션 리스트에서 ByteDance-Seedream-4.5 Bounding Box 타격...")
            options = page.locator("xpath=//*[contains(text(), 'Seedream-4.5') or contains(text(), '4.5 251128')]")
            opt_count = await options.count()
            print(f"발견된 옵션 수: {opt_count}")
            
            option_clicked = False
            for i in range(opt_count):
                opt = options.nth(i)
                box = await opt.bounding_box()
                if box:
                    await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                    print(f"옵션 [{i}] 마우스 중앙 클릭 격발 성공")
                    option_clicked = True
                    await page.wait_for_timeout(3000)
                    break
            
            if not option_clicked:
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(1000)
                
        except Exception as e:
            print(f"모델 변경 중 예외 발생: {e}")

        # 이미지 생성 진행
        try:
            print("프롬프트 타이핑 및 주입...")
            editor = page.locator(".tiptap.ProseMirror")
            await editor.click(force=True)
            await page.wait_for_timeout(1000)
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.wait_for_timeout(1000)
            
            prompt = "A cybernetic green frog sitting on a gold coin, 3d render, high detail, masterpiece"
            await page.keyboard.type(prompt, delay=50)
            await page.wait_for_timeout(3000)
            
            # 전송 버튼 강제 격발
            print("전송 버튼 강제 격발 시도...")
            submit_btn = page.locator("[data-testid='image-sender-submit-button']").first
            if await submit_btn.count() > 0:
                await submit_btn.evaluate("el => el.click()")
            else:
                submit_btn_backup = page.locator("button").filter(has=page.locator("svg")).last
                await submit_btn_backup.evaluate("el => el.click()")
                
            await page.wait_for_timeout(5000)
            
            # 생성 완료 대기 (25초)
            print("생성 중... 완료 대기 중 (25초)...")
            await page.wait_for_timeout(25000)
            
            # 3. 생성 완료된 최종 이미지 로컬 파일 다운로드/캡처 저장
            print("최종 완성 이미지 파일 추출 중...")
            result_img = page.locator("xpath=//div[contains(@class, 'image') or contains(@class, 'canvas')]//img").first
            if await result_img.count() == 0:
                result_img = page.locator("img").last
                
            if await result_img.count() > 0:
                output_filename = os.path.join(OUTPUT_DIR, "generated_youtube_source.png")
                await result_img.screenshot(path=output_filename)
                print(f"[대성공] 유튜브 본편 소스 이미지 다운로드 완료: {output_filename}")
            else:
                print("오류: 완성 이미지 요소를 화면에서 감지하지 못했습니다.")
                
            # 전체 화면 상태 백업 저장
            done_screenshot = os.path.join(OUTPUT_DIR, "byteplus_seedream_done.png")
            await page.screenshot(path=done_screenshot)
            print(f"완성 화면 스크린샷 저장: {done_screenshot}")
                
        except Exception as e:
            print(f"이미지 생성 프로세스 오류: {e}")
            await page.screenshot(path=os.path.join(OUTPUT_DIR, "byteplus_seedream_generate_error.png"))

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
