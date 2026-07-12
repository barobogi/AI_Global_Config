# patch_generator.py — 취약점 → Claude CLI 패치 생성 → T020 승인 연동
import subprocess, json, logging, sys, uuid, tempfile, os
from pathlib import Path

PYTHON = sys.executable
SEND_APPROVAL = str(Path(__file__).parent.parent / "T020_human_in_the_loop" / "send_approval.py")

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
    for finding in findings:
        target = finding["target"]
        local_path = target.get("local_path", "")
        # 폴더 경로인 경우 index.html로 보정
        if local_path and Path(local_path).is_dir():
            candidate = Path(local_path) / "index.html"
            local_path = str(candidate) if candidate.exists() else local_path

        for alert in finding["alerts"]:
            log.info(f"패치 생성 중: [{target['name']}] {alert['name']}")
            patched = generate_patch(alert, local_path)
            if not patched:
                continue

            # 패치 정보를 임시 JSON으로 저장 → send_approval.py에 전달
            cwd = str(Path(local_path).parent)
            patch_info = {
                "local_path": local_path,
                "code": patched,
                "cwd": cwd,
                "alert_name": alert["name"],
                "target_name": target["name"],
            }
            tmp_path = Path(tempfile.mktemp(suffix=".json", dir=Path(__file__).parent / "scan_reports"))
            tmp_path.write_text(json.dumps(patch_info, ensure_ascii=False), encoding="utf-8")

            approval_text = (
                f"대상: {target['name']}\n"
                f"취약점: {alert['name']} ({alert['riskdesc']})\n"
                f"파일: {local_path}"
            )
            result = subprocess.run(
                [PYTHON, SEND_APPROVAL,
                 "--text", approval_text,
                 "--patch-json", str(tmp_path)],
                capture_output=True, text=True, timeout=30,
                env={**os.environ, "APPROVAL_BOT_TOKEN": os.environ.get("APPROVAL_BOT_TOKEN", "")}
            )
            if result.returncode == 0:
                log.info(f"T020 승인 요청 전송 완료: {result.stdout.strip()}")
            else:
                log.error(f"T020 승인 요청 실패: {result.stderr.strip()}")
