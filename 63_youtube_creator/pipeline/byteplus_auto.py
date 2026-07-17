import os
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

COOKIE_PATH = r"D:\AI\.secrets\byteplus_cookies.json"

async def main():
    if not os.path.exists(COOKIE_PATH):
        print(f"오류: 쿠키 파일을 찾을 수 없습니다. 경로: {COOKIE_PATH}")
        return

    print("BytePlus Playground 모달 조상 Label 매핑 및 최종 생성 시나리오 가동")
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
        
        # 1차 동의 팝업 처리 (Overview 단계)
        try:
            agree_cb_overview = page.locator("xpath=//span[contains(text(), 'using BytePlus')]/ancestor::label").first
            if await agree_cb_overview.count() > 0:
                print("Overview 동의 체크박스 조상 Label 클릭...")
                await agree_cb_overview.evaluate("el => el.click()")
                await page.wait_for_timeout(1000)
                await page.locator("button:has-text('confirm'), button:has-text('Confirm')").first.evaluate("el => el.click()")
                await page.wait_for_timeout(2000)
        except Exception:
            pass

        # 왼쪽 메뉴에서 Playground 클릭
        print("Playground 메뉴 클릭...")
        await page.locator("text=Playground").first.click(force=True)
        await page.wait_for_timeout(4000)
        
        # 2차 동의 팝업 처리 (Playground 모달 정밀 해제 - 조상 Label 클릭)
        try:
            # 텍스트 'using BytePlus'를 감싸는 조상 label을 직접 타겟팅
            modal_checkbox = page.locator("xpath=//span[contains(text(), 'using BytePlus')]/ancestor::label").first
            if await modal_checkbox.count() > 0:
                print("Playground 모달 동의 체크박스 조상 Label 발견! 강제 토글...")
                await modal_checkbox.evaluate("el => el.click()")
                await page.wait_for_timeout(1500)
                
                # confirm 버튼 클릭
                confirm_btn = page.locator(".aml-arco-modal-wrapper button:has-text('confirm'), .aml-arco-modal-wrapper button:has-text('Confirm')").first
                if await confirm_btn.count() > 0:
                    print("confirm 버튼 클릭...")
                    await confirm_btn.evaluate("el => el.click()")
                    print("모달 승인 완료.")
                    await page.wait_for_timeout(3000)
        except Exception as ex:
            print(f"Playground 모달 동의 처리 예외 (생략 가능): {ex}")
            
        # 비기너 가이드 팝업 닫기 (Escape)
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1000)

        # 상단 "Image" 탭 클릭
        print("상단 Image 탭 클릭...")
        image_tab = page.locator("div, span, button").filter(has_text="Image").first
        await image_tab.click(force=True)
        await page.wait_for_timeout(5000)
        
        # 모델 변경 시도
        try:
            print("모델 선택 드롭다운 클릭 시도...")
            dropdown_selectors = [
                ".aml-arco-select-view",
                "text=Dola-Seedream-5.0-pro",
                "xpath=//div[contains(@class, 'select-view')]",
                "xpath=//span[contains(text(), 'Seedream')]/ancestor::div[contains(@class, 'select')]"
            ]
            
            for selector in dropdown_selectors:
                target = page.locator(selector).first
                if await target.count() > 0:
                    print(f"드롭다운 클릭 격발: '{selector}'")
                    await target.evaluate("el => el.click()")
                    await page.wait_for_timeout(2000)
                    break
            
            # 리스트에서 Dola-Seed-2.1-turbo 선택
            print("모델 옵션 클릭 시도...")
            option_selectors = [
                "text=Dola-Seed-2.1-turbo",
                ".aml-arco-select-option >> text=Dola-Seed-2.1-turbo",
                "xpath=//li[contains(., 'Dola-Seed-2.1-turbo') or contains(@class, 'option')]",
                "xpath=//*[contains(text(), '2.1-turbo')]"
            ]
            
            option_clicked = False
            for opt_sel in option_selectors:
                opt = page.locator(opt_sel).first
                if await opt.count() > 0:
                    print(f"모델 옵션 클릭 격발: '{opt_sel}'")
                    await opt.evaluate("el => el.click()")
                    await page.wait_for_timeout(3000)
                    option_clicked = True
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
            
            # 생성 중 스크린샷
            generating_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generating.png"
            await page.screenshot(path=generating_screenshot)
            print(f"생성 격발 직후 화면 스크린샷 저장: {generating_screenshot}")
            
            # 생성 완료 대기 (25초)
            print("생성 완료 대기 중 (25초)...")
            await page.wait_for_timeout(25000)
            
            # 완료 스크린샷
            done_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_done.png"
            await page.screenshot(path=done_screenshot)
            print(f"완성 화면 스크린샷 저장: {done_screenshot}")
                
        except Exception as e:
            print(f"이미지 생성 프로세스 오류: {e}")
            await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_seedream_generate_error.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
