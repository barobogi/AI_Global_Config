# 공공데이터포털(odcloud) 전체 데이터셋 카탈로그를 DuckDB로 긁어오는 스크립트
"""
2026-08-29: 3탄 후보 발굴 때 만복이 직감으로 5개 도메인만 조사했다가
"왜 5개밖에 안 되냐, 넓고 크게 생각하자"는 지적을 받은 데서 시작.
매번 fork 돌려서 WebSearch로 조사하는 대신, 전체 카탈로그(약 96,472건)를
메타데이터만 가볍게 긁어서 로컬 DuckDB에 넣어두고 SQL로 바로 검색.

주의: 이건 "메타데이터 카탈로그"일 뿐 — 활용신청/응답필드실측/이용조건 확인 같은
깊은 검증은 각 앱 착수 시점(Phase 0)에 여전히 개별로 해야 함 (조기추상화 금지 원칙 유지).

사용법:
  python fetch_catalog.py          # 전체 재수집 (최초 실행, ~97 페이지)
  python fetch_catalog.py --update # 증분 갱신용 자리(현재는 전체 재수집과 동일, TODO)
"""
import argparse
import sys
import time
from pathlib import Path

import duckdb
import requests

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ENV_PATH = Path(r"D:\AI\65_android_apps\.env")
DB_PATH = Path(__file__).parent / "catalog.duckdb"
API_URL = "https://api.odcloud.kr/api/15077093/v1/dataset"
PER_PAGE = 1000  # 실측: 1000까지 정상, 5000은 빈 응답 (2026-08-29 확인)


def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        raise FileNotFoundError(f".env 없음: {path}")
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip()
    return env


def fetch_all_pages(service_key: str):
    headers = {"Authorization": f"Infuser {service_key}"}
    page = 1
    total = None
    all_rows = []
    while True:
        resp = requests.get(API_URL, headers=headers, params={"page": page, "perPage": PER_PAGE}, timeout=30)
        resp.raise_for_status()
        d = resp.json()
        if total is None:
            total = d.get("totalCount", 0)
            print(f"전체 {total}건, perPage={PER_PAGE} 기준 {-(-total // PER_PAGE)}페이지 예정")
        rows = d.get("data", [])
        if not rows:
            break
        all_rows.extend(rows)
        print(f"  page {page}: 누적 {len(all_rows)}/{total}")
        if len(all_rows) >= total:
            break
        page += 1
        time.sleep(0.2)  # API 예의상 짧은 딜레이
    return all_rows


def build_db(rows: list):
    # 2026-08-29: 최초 버전은 con.executemany()로 96,472건을 한 줄씩 넣다가 25분 넘게
    # 걸려서 중단함 — DataFrame 경유 벌크 적재로 바꾸니 수 초로 단축됨.
    import pandas as pd

    if DB_PATH.exists():
        DB_PATH.unlink()
    con = duckdb.connect(str(DB_PATH))
    records = [
        (
            r.get("id"), r.get("title"), r.get("desc"), r.get("keywords"),
            r.get("category_nm"), r.get("new_category_nm"), r.get("org_nm"),
            r.get("ext"), r.get("download_cnt") or 0, r.get("view_cnt") or 0,
            r.get("updated_at"), r.get("created_at"), r.get("page_url"), r.get("register_status"),
        )
        for r in rows
    ]
    cols = ["id", "title", "description", "keywords", "category_nm", "new_category_nm",
            "org_nm", "ext", "download_cnt", "view_cnt", "updated_at", "created_at",
            "page_url", "register_status"]
    df = pd.DataFrame(records, columns=cols)
    con.execute("CREATE TABLE datasets AS SELECT * FROM df")
    con.execute("CREATE INDEX idx_category ON datasets(new_category_nm)")
    con.execute("CREATE INDEX idx_org ON datasets(org_nm)")
    count = con.execute("SELECT COUNT(*) FROM datasets").fetchone()[0]
    print(f"DuckDB 적재 완료: {count}건 -> {DB_PATH}")
    con.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="증분 갱신(현재 미구현, 전체 재수집과 동일)")
    args = parser.parse_args()

    env = load_env(ENV_PATH)
    service_key = env.get("ODCLOUD_SERVICE_KEY")
    if not service_key:
        print("ODCLOUD_SERVICE_KEY가 .env에 없음", file=sys.stderr)
        sys.exit(1)

    rows = fetch_all_pages(service_key)
    build_db(rows)


if __name__ == "__main__":
    main()
