# patch_generator.py — 취약점 → Claude CLI 패치 생성 → T020 승인 연동
import subprocess, json, logging, sys
from pathlib import Path

log = logging.getLogger(__name__)


def generate_patch(alert: dict, local_path: str) -> str | None:
    """Claude CLI로 취약점 패치 코드 생성"""
    path = Path(local_path)
    if not path.exists() or path.is_dir():
        log.warning(f"패치 대상 파일 없음: {local_path}")
        return None

    source = path.read_text(encoding="utf-8", errors="replace")
    prompt = f"""보안 취약점을 수정해주세요.

취약점 정보:
- 이름: {alert['name']}
- 위험도: {alert['riskdesc']}
- 설명: {alert['desc']}
- 해결책: {alert['solution']}

대상 파일 ({local_path}):
```
{source[:8000]}
```

취약점을 수정한 전체 파일 내용만 출력하세요 (설명 없이 코드만)."""

    result = subprocess.run(
        ["claude", "--output-format", "json", "--print"],
        input=prompt.encode("utf-8"),
        capture_output=True, timeout=120
    )
    if result.returncode != 0:
        log.error(f"Claude CLI 오류: {result.stderr.decode('utf-8', errors='replace')[:200]}")
        return None

    outer = json.loads(result.stdout.decode("utf-8"))
    return outer.get("result", "")


def apply_patch(local_path: str, patched_code: str) -> bool:
    """패치 코드를 파일에 적용"""
    try:
        Path(local_path).write_text(patched_code, encoding="utf-8")
        log.info(f"패치 적용 완료: {local_path}")
        return True
    except Exception as e:
        log.error(f"패치 적용 실패: {e}")
        return False


def run_patch_pipeline(findings: list):
    """취약점 목록 → 패치 생성 → T020 승인 요청"""
    # TODO: T020 완료 후 승인 모듈 import 경로 확정
    # from D_AI_AI_hub_shared_T020.send_approval import request_approval

    for finding in findings:
        target = finding["target"]
        local_path = target.get("local_path", "")
        for alert in finding["alerts"]:
            log.info(f"패치 생성 중: [{target['name']}] {alert['name']}")
            patched = generate_patch(alert, local_path)
            if not patched:
                continue

            # T020 승인 요청 메시지 구성
            approval_msg = (
                f"🔐 보안 패치 승인 요청\n"
                f"대상: {target['name']}\n"
                f"취약점: {alert['name']} ({alert['riskdesc']})\n"
                f"파일: {local_path}\n\n"
                f"패치 코드가 생성되었습니다. 적용하시겠습니까?"
            )
            log.info(f"[T020 연동 대기] 승인 메시지:\n{approval_msg}")

            # TODO: T020 완료 후 아래 활성화
            # approved = request_approval(approval_msg, context={"path": local_path, "code": patched})
            # if approved:
            #     apply_patch(local_path, patched)
            #     subprocess.run(["git", "add", local_path], cwd=Path(local_path).parent)
            #     subprocess.run(["git", "commit", "-m", f"fix: 보안 패치 — {alert['name']}"])
            #     subprocess.run(["git", "push"])
