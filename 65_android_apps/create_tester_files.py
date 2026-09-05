# -*- coding: utf-8 -*-
"""
create_tester_files.py — 테스터 22명 이메일 목록을 CSV, TXT(쉼표 구분/줄바꿈 구분) 및 README 형태로 영구 보관하는 파이프라인
"""
from pathlib import Path

TESTERS = [
    "barabogi@gmail.com",
    "barobogi79@gmail.com",
    "bhang9394@gmail.com",
    "bluesky07yj@gmail.com",
    "c87277@gmail.com",
    "comchyta@gmail.com",
    "e54ast@gmail.com",
    "echo3192@gmail.com",
    "echo3196@gmail.com",
    "hahahoho@gmail.com",
    "hanbogi7979@gmail.com",
    "hanbogi79@gmail.com",
    "hanbogi79@naver.com",
    "hyunchul.lee79@gmail.com",
    "leemichaela55@gmail.com",
    "leesuchoul5312@gmail.com",
    "leeujin1001@gmail.com",
    "lhb7942@gmail.com",
    "lovelyqny@gmail.com",
    "namexxok@gmail.com",
    "woongja.han@gmail.com",
    "yunha1004@gmail.com"
]

BASE_DIR = Path(r"D:\AI\65_android_apps")

def generate_files():
    # 1. Standard CSV file (Google Play Console 'CSV 파일 업로드' 전용)
    csv_file = BASE_DIR / "PLAY_CONSOLE_20_TESTERS.csv"
    csv_content = "\n".join(TESTERS) + "\n"
    csv_file.write_text(csv_content, encoding="utf-8")

    # 2. Comma-separated TXT file (구글 콘솔 텍스트 박스 복사-붙여넣기 전용)
    comma_file = BASE_DIR / "PLAY_CONSOLE_20_TESTERS_COMMA.txt"
    comma_content = ", ".join(TESTERS)
    comma_file.write_text(comma_content, encoding="utf-8")

    # 3. Documentation README
    readme_file = BASE_DIR / "PLAY_CONSOLE_TESTERS_GUIDE.md"
    readme_content = f"""# Google Play Console 20인 비공개 테스터 표준 목록

본 폴더에는 65번 뿌리 안드로이드 앱 시리즈(1탄 오늘뭐하지, 2탄 도서관/열람실 등) 공통으로 활용하는 **22인 테스터 이메일 명단 파일**이 보관되어 있습니다.

## 📁 보관 파일 목록
1. **[PLAY_CONSOLE_20_TESTERS.csv](file:///d:/AI/65_android_apps/PLAY_CONSOLE_20_TESTERS.csv)**
   - 구글 플레이 콘솔 테스터 등록 화면에서 **`[CSV 파일 업로드]`** 클릭 시 바로 선택해서 업로드하는 표준 CSV 파일
2. **[PLAY_CONSOLE_20_TESTERS_COMMA.txt](file:///d:/AI/65_android_apps/PLAY_CONSOLE_20_TESTERS_COMMA.txt)**
   - 쉼표(`,`)로 구분된 22명 이메일 텍스트 파일 (텍스트 상자 복사-붙여넣기용)

## 📋 등록된 테스터 이메일 (총 {len(TESTERS)}명)
""" + "\n".join([f"{idx}. {email}" for idx, email in enumerate(TESTERS, 1)]) + "\n"
    readme_file.write_text(readme_content, encoding="utf-8")

    print("테스터 명단 파일 생성 완료:")
    print(f"- CSV: {csv_file}")
    print(f"- COMMA TXT: {comma_file}")
    print(f"- GUIDE MD: {readme_file}")

if __name__ == "__main__":
    generate_files()
