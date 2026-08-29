# 고신호(high-signal) 검증 프레임워크 — 3AI 파이프라인 공용 검증기 모음
"""
verify_video.py/goal_runner.py에 각각 따로 박혀있던 held-out 검증 로직을
재사용 가능한 형태로 추출. Langfuse "Stop Burning Tokens" 뽀개기(2026-08-29)에서
확인한 원칙 2가지를 코드로 강제한다:
  1. 애매한 스칼라 판단("괜찮아 보임") 대신 명확한 예/아니오 검증을 쓴다.
  2. 반복 루프가 매 턴 봐온 기준과 별개로, 최종 확인은 held-out 기준으로 한다.

CLI 사용법 (goal_runner.py --final-check-command 등에서 재사용 가능):
  python verifiers.py video <mp4_path>
  python verifiers.py json <path>
  python verifiers.py pytest <test_path_or_dir>
  python verifiers.py dup <youtube_video_id>

exit 0 = PASS, exit 1 = FAIL, exit 2 = 사용법 오류
"""
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def check_video_integrity(mp4_path) -> tuple[bool, str]:
    """실제 프레임 디코딩 검증 — 메타데이터(해상도/길이)만으론 못 잡는 스트림
    손상 탐지. EP.03 손상 영상이 verify_video.py의 메타데이터 체크만으론
    걸러지지 않고 통과했던 사고(2026-08-29)에서 도출."""
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ffmpeg_exe = "ffmpeg"  # PATH에 있으면 폴백

    try:
        result = subprocess.run(
            [ffmpeg_exe, "-v", "error", "-i", str(mp4_path), "-f", "null", "-"],
            capture_output=True, text=True, timeout=120
        )
    except Exception as e:
        return False, f"ffmpeg 실행 실패: {e}"

    stderr = result.stderr
    if "Invalid NAL unit" in stderr or "Error splitting the input" in stderr:
        return False, "H.264 스트림 손상 감지 (Invalid NAL unit)"
    if result.returncode != 0:
        return False, f"ffmpeg 디코딩 실패(exit {result.returncode}): {stderr[:300]}"
    return True, "프레임 디코딩 정상"


def check_json_valid(path) -> tuple[bool, str]:
    """JSON 파일 문법 검증."""
    try:
        with open(path, encoding="utf-8") as f:
            json.load(f)
        return True, "JSON 파싱 정상"
    except Exception as e:
        return False, f"JSON 파싱 실패: {e}"


def check_pytest(test_path) -> tuple[bool, str]:
    """pytest 실행 후 전체 통과 여부. 요약 라인만 반환(전체 로그는 호출자가 캡처)."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_path), "-q"],
            capture_output=True, text=True, timeout=300
        )
    except Exception as e:
        return False, f"pytest 실행 실패: {e}"
    ok = result.returncode == 0
    tail = (result.stdout + result.stderr).strip().splitlines()
    summary = tail[-1] if tail else "(출력 없음)"
    return ok, summary


def check_not_duplicate(video_id) -> tuple[bool, str]:
    """뽀개기 선택 전 중복 확인 — pobbagi_history.db + 과거 메시지 파일 이중 대조.
    2026-08-29: 만복이 7/19에 이미 배정됐던 jdbOVepEtUE를 다시 뽀개기로 선택한 실수에서
    도출. DB만 보면 못 잡는다는 게 실제로 확인됨(그 배정은 메시지 파일에만 남아있고
    DB엔 기록된 적이 없었음) — 그래서 메시지 폴더 텍스트 검색까지 같이 한다."""
    hits = []
    db_path = Path(r"D:\AI\25_auto_pobbagi\pobbagi_history.db")
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            c = conn.cursor()
            c.execute("SELECT title, pobbagi_date, assignee FROM pobbagi_history WHERE video_id=?", (video_id,))
            row = c.fetchone()
            conn.close()
            if row:
                hits.append(f"DB: {row[1]} {row[2]} 담당 [{row[0]}]")
        except Exception:
            pass

    messages_dir = Path(r"D:\AI\AI_hub\shared\messages")
    if messages_dir.exists():
        for f in messages_dir.glob("*.md"):
            if "뽀개기후보목록" in f.name:
                continue  # 후보 풀 나열일 뿐 실제 배정/완료 근거 아님 — 매일 재노출되는 미처리 항목까지 오탐 방지
            try:
                if video_id in f.read_text(encoding="utf-8", errors="ignore"):
                    hits.append(f"메시지: {f.name}")
            except Exception:
                continue

    if hits:
        return False, "이미 처리/배정된 이력 있음 — " + " | ".join(hits[:5])
    return True, "신규 (중복 이력 없음)"


CHECKS = {
    "video": check_video_integrity,
    "json": check_json_valid,
    "pytest": check_pytest,
    "dup": check_not_duplicate,
}


def main():
    if len(sys.argv) < 3:
        print("사용법: python verifiers.py <video|json|pytest> <경로>", file=sys.stderr)
        sys.exit(2)
    check_type, target = sys.argv[1], sys.argv[2]
    check_fn = CHECKS.get(check_type)
    if not check_fn:
        print(f"알 수 없는 검증 타입: {check_type} (사용 가능: {', '.join(CHECKS)})", file=sys.stderr)
        sys.exit(2)
    ok, msg = check_fn(target)
    print(f"[{'PASS' if ok else 'FAIL'}] {check_type}: {msg}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
