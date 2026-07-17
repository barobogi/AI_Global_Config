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

    print("BytePlus 모든 모델 일괄 강제 활성화 시나리오 시작")
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
        
        # 1. 모델 활성화 관리 페이지(ComputerVision & LLM 전체)로 이동
        activation_url = "https://console.byteplus.com/ark/region:ap-southeast-1/openManagement?tab=ComputerVision"
        print(f"모델 관리 페이지로 이동 중: {activation_url}")
        await page.goto(activation_url, wait_until="load")
        await page.wait_for_timeout(5000) # 리스트 로딩 충분히 대기
        
        # Overview 단계 및 모달 팝업 가로막기 제거
        try:
            await page.evaluate("""() => {
                // 1) 체크박스 클릭
                const cb = document.querySelector('.aml-arco-checkbox');
                if (cb) cb.click();
                // 2) confirm 버튼 클릭
                setTimeout(() => {
                    const confirmBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.toLowerCase().includes('confirm'));
                    if (confirmBtn) confirmBtn.click();
                }, 500);
            }""")
            await page.wait_for_timeout(2000)
        except Exception:
            pass

        # 2. 'Enable all models' (모든 모델 일괄 활성화) 버튼 강제 클릭 및 무료 승인
        try:
            print("일괄 활성화(Enable all models) 버튼 감지 및 클릭...")
            enable_all_btn = page.locator("text=Enable all models").first
            if await enable_all_btn.count() > 0:
                await enable_all_btn.evaluate("el => el.click()")
                await page.wait_for_timeout(3000)
                
                # 무료 모드 및 동의 체크박스 강제 체크 (DOM 주입)
                print("무료 모드 및 이용약관 강제 동의 주입...")
                await page.evaluate("""() => {
                    // 모든 팝업 내 체크박스(라벨)를 찾아서 클릭
                    const labels = document.querySelectorAll('.aml-arco-modal-wrapper label, .aml-arco-modal-wrapper .aml-arco-checkbox');
                    labels.forEach(l => {
                        l.click();
                    });
                    
                    // 최종 승인 버튼 클릭
                    setTimeout(() => {
                        const submitBtn = Array.from(document.querySelectorAll('.aml-arco-modal-wrapper button')).find(b => b.innerText.toLowerCase().includes('confirm') || b.innerText.toLowerCase().includes('authorization'));
                        if (submitBtn) {
                            submitBtn.click();
                            console.log("최종 승인 격발 완료");
                        }
                    }, 1000);
                }""")
                await page.wait_for_timeout(5000)
                
            # 결과 저장
            activated_screenshot = r"D:\AI\63_youtube_creator\pipeline\output\byteplus_all_activated.png"
            await page.screenshot(path=activated_screenshot)
            print(f"모든 모델 일괄 활성화 처리 화면 스크린샷 저장: {activated_screenshot}")
            
        except Exception as e:
            print(f"일괄 활성화 중 오류 발생: {e}")
            
        # 3. LLM 탭으로 넘어가서 동일한 일괄 활성화 반복 시도
        try:
            print("LLM 탭으로 전환 및 활성화 시도...")
            await page.goto("https://console.byteplus.com/ark/region:ap-southeast-1/openManagement?tab=LLM", wait_until="load")
            await page.wait_for_timeout(5000)
            
            enable_all_btn = page.locator("text=Enable all models").first
            if await enable_all_btn.count() > 0:
                await enable_all_btn.evaluate("el => el.click()")
                await page.wait_for_timeout(3000)
                await page.evaluate("""() => {
                    const labels = document.querySelectorAll('.aml-arco-modal-wrapper label, .aml-arco-modal-wrapper .aml-arco-checkbox');
                    labels.forEach(l => l.click());
                    setTimeout(() => {
                        const submitBtn = Array.from(document.querySelectorAll('.aml-arco-modal-wrapper button')).find(b => b.innerText.toLowerCase().includes('confirm') || b.innerText.toLowerCase().includes('authorization'));
                        if (submitBtn) submitBtn.click();
                    }, 1000);
                }""")
                await page.wait_for_timeout(5000)
                
            await page.screenshot(path=r"D:\AI\63_youtube_creator\pipeline\output\byteplus_llm_activated.png")
            print("LLM 모델 전체 활성화 완료.")
            
        except Exception as e:
            print(f"LLM 탭 활성화 오류: {e}")

        # 쿠키 업데이트
        cookies = await context.cookies()
        with open(COOKIE_PATH, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
        print("최종 동기화 쿠키 갱신 완료.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
