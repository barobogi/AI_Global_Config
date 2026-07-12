# security_scan.py — ZAP 자동 보안 스캔 + 취약점 보고
import subprocess, json, datetime, logging, sys
from pathlib import Path

BASE_DIR   = Path(__file__).parent
CONFIG     = json.loads((BASE_DIR / "scan_targets.json").read_text(encoding="utf-8"))
REPORT_DIR = BASE_DIR / "scan_reports"
REPORT_DIR.mkdir(exist_ok=True)

JAVA    = CONFIG["zap"]["java"]
ZAP_JAR = CONFIG["zap"]["jar"]
TIMEOUT = CONFIG["zap"]["timeout_sec"]
THRESHOLD = set(CONFIG["alert_threshold"])

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(BASE_DIR / "scan_reports" / "scan.log", encoding="utf-8"),
    ]
)
log = logging.getLogger(__name__)


def run_zap(url: str, name: str) -> Path:
    slug = name.replace(" ", "_")
    out  = REPORT_DIR / f"zap_{datetime.date.today()}_{slug}.json"
    log.info(f"ZAP 스캔 시작: {name} ({url})")
    result = subprocess.run(
        [JAVA, "-jar", ZAP_JAR, "-cmd",
         "-quickurl", url,
         "-quickout", str(out),
         "-quickprogress"],
        capture_output=True, text=True, timeout=TIMEOUT
    )
    if result.returncode != 0:
        log.error(f"ZAP 오류 ({name}): {result.stderr[:200]}")
    return out


def parse_alerts(report_path: Path) -> list:
    if not report_path.exists():
        return []
    try:
        data = json.loads(report_path.read_text(encoding="utf-8"))
        alerts = data.get("site", [{}])[0].get("alerts", [])
        return [a for a in alerts if any(a.get("riskdesc", "").startswith(t) for t in THRESHOLD)]
    except Exception as e:
        log.error(f"결과 파싱 실패: {e}")
        return []


def scan_all() -> list[dict]:
    """전체 대상 스캔 후 취약점 목록 반환"""
    findings = []
    for target in CONFIG["targets"]:
        if not Path(ZAP_JAR).exists():
            log.error(f"ZAP jar 없음: {ZAP_JAR} — 안티에게 설치 요청 필요")
            break
        report_path = run_zap(target["url"], target["name"])
        alerts = parse_alerts(report_path)
        if alerts:
            log.warning(f"[{target['name']}] 취약점 {len(alerts)}개 발견")
            findings.append({
                "target": target,
                "alerts": alerts,
                "report": str(report_path),
            })
        else:
            log.info(f"[{target['name']}] ✅ 취약점 없음")
    return findings


def save_summary(findings: list) -> Path:
    summary_path = REPORT_DIR / f"summary_{datetime.date.today()}.json"
    summary_path.write_text(
        json.dumps(findings, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return summary_path


if __name__ == "__main__":
    log.info("=== T022 보안 스캔 시작 ===")
    findings = scan_all()
    if findings:
        summary = save_summary(findings)
        log.warning(f"총 {len(findings)}개 대상에서 취약점 발견 → {summary}")
        log.info("patch_generator.py 호출 (T020 연동 완료 후 활성화)")
        # TODO: T020 완료 후 아래 활성화
        # from patch_generator import run_patch_pipeline
        # run_patch_pipeline(findings)
    else:
        log.info("=== 전체 스캔 완료 — 취약점 없음 ✅ ===")
