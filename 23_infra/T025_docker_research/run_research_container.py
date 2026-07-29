"""
T025 Docker Research Container Runner (v0.1)
3AI 통합용 Docker 리서치 모듈 래퍼
"""
import os
import sys
import subprocess
import json
import argparse

if sys.stdout is not None and getattr(sys.stdout, "encoding", None) is not None:
    if sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAME = "3ai/research_search:latest"
SHARED_DATA_DIR = r"D:\AI\AI_hub\shared\data"

def ensure_docker_image():
    """Docker 이미지 가용성 검사 및 필요 시 빌드"""
    print("🐳 [T025] Docker 이미지 상태 점검 중...")
    result = subprocess.run(["docker", "images", "-q", IMAGE_NAME], capture_output=True, text=True)
    if not result.stdout.strip():
        print(f"🔨 [T025] Docker 이미지({IMAGE_NAME})가 없습니다. 빌드를 시작합니다...")
        build_cmd = ["docker", "build", "-t", IMAGE_NAME, MODULE_DIR]
        res = subprocess.run(build_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ [Error] Docker 빌드 실패: {res.stderr}")
            return False
        print("✅ [T025] Docker 이미지 빌드 완료!")
    else:
        print("✅ [T025] 기존 Docker 이미지를 확인했습니다.")
    return True

def run_container_search(queries, max_results=5, output_file=None):
    """Docker 컨테이너를 구동하여 격리된 병렬 리서치 수행"""
    if not ensure_docker_image():
        return {"status": "error", "message": "Docker image not ready"}

    os.makedirs(SHARED_DATA_DIR, exist_ok=True)
    
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{SHARED_DATA_DIR}:/app/shared_data",
        IMAGE_NAME,
        "--queries"
    ] + queries + ["--max", str(max_results)]

    print(f"🚀 [T025] Docker 리서치 컨테이너 격발 중... (쿼리 수: {len(queries)})")
    start_t = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    
    if start_t.returncode != 0:
        print(f"❌ [Error] 컨테이너 실행 오류: {start_t.stderr}")
        return {"status": "error", "message": start_t.stderr}
        
    try:
        data = json.loads(start_t.stdout.strip())
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"💾 [T025] 결과 저장 완료: {output_file}")
        return data
    except Exception as e:
        print(f"⚠️ [Warning] JSON 파싱 실패: {e}")
        return {"status": "raw_output", "output": start_t.stdout}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="T025 Docker Research Runner")
    parser.add_argument("--queries", nargs="+", required=True, help="Queries to search")
    parser.add_argument("--max", type=int, default=5, help="Max results per query")
    parser.add_argument("--output", type=str, help="Output JSON path")
    
    args = parser.parse_args()
    res = run_container_search(args.queries, args.max, args.output)
    print(json.dumps(res, ensure_ascii=False, indent=2))
