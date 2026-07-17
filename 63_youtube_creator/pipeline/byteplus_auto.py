import os
import requests
import asyncio
from dotenv import load_dotenv

load_dotenv()

BYTEPLUS_API_KEY = os.getenv("BYTEPLUS_API_KEY")

async def generate_scene_image(prompt_text, output_path):
    """
    BytePlus API (Dola-Seedream) 연동을 통한 실사 이미지 렌더링.
    """
    print(f"\n========== 실사 이미지 렌더링 (BytePlus API) ==========")
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    if not BYTEPLUS_API_KEY:
        print("[오류] BYTEPLUS_API_KEY가 설정되지 않았습니다.")
        return False

    url = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
    headers = {
        "Authorization": f"Bearer {BYTEPLUS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "ep-20240717203157-image", # 테스트용 엔드포인트명 가정 (또는 모델명)
        "prompt": prompt_text,
        "n": 1
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        image_url = data.get("data", [{}])[0].get("url")
        
        if image_url:
            img_data = requests.get(image_url).content
            with open(output_path, 'wb') as f:
                f.write(img_data)
            print(f"  - [성공] 실사 이미지 저장 완료: {output_path}")
            return True
        else:
            print("  - [오류] 응답에 이미지 URL이 없습니다.")
            return False
            
    except Exception as e:
        print(f"  - [오류] API 호출 실패: {e}")
        return False

if __name__ == "__main__":
    print("API 연동 단독 테스트 실행")
    asyncio.run(generate_scene_image("A futuristic robot typing on a computer, highly detailed", r"D:\AI\63_youtube_creator\pipeline\output\test_api.jpg"))
