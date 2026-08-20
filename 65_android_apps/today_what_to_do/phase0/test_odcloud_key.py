"""Phase 0 스모크테스트 - odcloud 목록조회 API 키 연결 확인.
공공API 3종(관광정보/반려동물/기상청) 키 발급 전, 지금 있는 키로 연결 자체가 되는지 검증."""
import os
import requests
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        raise FileNotFoundError(f".env 없음: {path}")
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip()
    return env


def main():
    env = load_env(ENV_PATH)
    service_key = env.get("ODCLOUD_SERVICE_KEY")
    if not service_key:
        print("ODCLOUD_SERVICE_KEY가 .env에 없음")
        return

    url = "https://api.odcloud.kr/api/15077093/v1/dataset"
    headers = {"Authorization": f"Infuser {service_key}"}
    params = {"page": 1, "perPage": 5}

    resp = requests.get(url, headers=headers, params=params, timeout=10)
    print(f"status_code: {resp.status_code}")
    print(resp.text[:1000])


if __name__ == "__main__":
    main()
