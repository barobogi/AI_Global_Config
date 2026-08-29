# 공공데이터 카탈로그 검색 CLI — catalog.duckdb 대상
"""
사용법:
  python query.py search "실시간 좌석"          # 제목+설명+키워드 통합 검색
  python query.py category                      # 카테고리별 건수 랭킹
  python query.py category "보건의료"            # 특정 카테고리 내 인기순 목록
  python query.py top --limit 20                # 전체 다운로드 상위 N개
"""
import sys
from pathlib import Path

import duckdb

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = Path(__file__).parent / "catalog.duckdb"


def _connect():
    if not DB_PATH.exists():
        print(f"{DB_PATH} 없음 — 먼저 python fetch_catalog.py 실행할 것", file=sys.stderr)
        sys.exit(1)
    return duckdb.connect(str(DB_PATH), read_only=True)


def cmd_search(keyword: str, limit: int = 30):
    con = _connect()
    rows = con.execute(
        """
        SELECT title, new_category_nm, org_nm, download_cnt, updated_at, page_url
        FROM datasets
        WHERE title ILIKE ? OR description ILIKE ? OR keywords ILIKE ?
        ORDER BY download_cnt DESC
        LIMIT ?
        """,
        [f"%{keyword}%"] * 3 + [limit],
    ).fetchall()
    for r in rows:
        print(f"[{r[1]}] {r[0]} (다운로드 {r[3]}, {r[2]}, 갱신 {r[4]})\n  {r[5]}")
    print(f"\n총 {len(rows)}건 표시 (limit={limit})")


def cmd_category(name: str = None, limit: int = 30):
    con = _connect()
    if name:
        rows = con.execute(
            "SELECT title, org_nm, download_cnt, page_url FROM datasets "
            "WHERE new_category_nm = ? ORDER BY download_cnt DESC LIMIT ?",
            [name, limit],
        ).fetchall()
        for r in rows:
            print(f"{r[0]} (다운로드 {r[2]}, {r[1]})\n  {r[3]}")
    else:
        rows = con.execute(
            "SELECT new_category_nm, COUNT(*) FROM datasets GROUP BY 1 ORDER BY 2 DESC"
        ).fetchall()
        for r in rows:
            print(f"{r[0]}: {r[1]}건")


def cmd_top(limit: int = 30):
    con = _connect()
    rows = con.execute(
        "SELECT title, new_category_nm, org_nm, download_cnt FROM datasets "
        "ORDER BY download_cnt DESC LIMIT ?",
        [limit],
    ).fetchall()
    for r in rows:
        print(f"{r[3]:>8} | [{r[1]}] {r[0]} ({r[2]})")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    cmd = sys.argv[1]
    if cmd == "search" and len(sys.argv) > 2:
        cmd_search(sys.argv[2])
    elif cmd == "category":
        cmd_category(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "top":
        limit = 30
        if "--limit" in sys.argv:
            limit = int(sys.argv[sys.argv.index("--limit") + 1])
        cmd_top(limit)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
