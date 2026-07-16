# approve_and_upload.py — 만복 3차 승인 후 자동 업로드 실행
# 사용: python approve_and_upload.py --video crisp_dm_shorts.mp4 --title "..." --type shorts
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from youtube_upload import upload_video

APPROVAL_LOG = Path(__file__).parent.parent.parent / "AI_hub" / "shared" / "data" / "youtube_approvals.json"


def load_approvals() -> dict:
    if APPROVAL_LOG.exists():
        return json.loads(APPROVAL_LOG.read_text(encoding="utf-8"))
    return {}


def save_approval(video_id_key: str, stage: int, ai_name: str, ok: bool, note: str = ""):
    approvals = load_approvals()
    if video_id_key not in approvals:
        approvals[video_id_key] = {"stages": {}, "created_at": datetime.now().isoformat()}
    approvals[video_id_key]["stages"][str(stage)] = {
        "ai": ai_name, "ok": ok, "note": note, "ts": datetime.now().isoformat()
    }
    APPROVAL_LOG.parent.mkdir(parents=True, exist_ok=True)
    APPROVAL_LOG.write_text(json.dumps(approvals, ensure_ascii=False, indent=2), encoding="utf-8")
    return approvals[video_id_key]


def check_all_approved(video_id_key: str) -> bool:
    """1차(안티)+2차(코니)+3차(만복) 모두 OK인지 확인"""
    approvals = load_approvals()
    entry = approvals.get(video_id_key, {})
    stages = entry.get("stages", {})
    return (
        stages.get("1", {}).get("ok") and
        stages.get("2", {}).get("ok") and
        stages.get("3", {}).get("ok")
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video",   required=True)
    parser.add_argument("--title",   required=True)
    parser.add_argument("--type",    default="shorts", choices=["shorts", "main"])
    parser.add_argument("--tags",    default="")
    parser.add_argument("--privacy", default="public")
    parser.add_argument("--stage",   type=int, choices=[1, 2, 3], required=True, help="1=안티 2=코니 3=만복")
    parser.add_argument("--ai",      required=True, help="승인 AI 이름 (안티/코니/만복)")
    parser.add_argument("--ok",      action="store_true", help="승인")
    parser.add_argument("--reject",  action="store_true", help="반려")
    parser.add_argument("--note",    default="")
    args = parser.parse_args()

    video_path = Path(args.video)
    video_key  = video_path.stem   # 파일명 (확장자 제외)

    ok = args.ok and not args.reject

    # 승인 기록
    entry = save_approval(video_key, args.stage, args.ai, ok, args.note)
    stages = entry.get("stages", {})

    print(f"[ApproveUpload] {args.ai} {args.stage}차 {'✅ 승인' if ok else '❌ 반려'}: {video_key}")
    if args.note:
        print(f"  메모: {args.note}")

    if not ok:
        print(f"[ApproveUpload] 반려됨 — 보완 후 재제출 필요")
        return

    # 현재 단계 현황 출력
    for s in ["1", "2", "3"]:
        name = {"1": "안티", "2": "코니", "3": "만복"}[s]
        st = stages.get(s, {})
        status = "✅" if st.get("ok") else ("❌" if st else "⏳")
        print(f"  {status} {s}차 ({name}): {st.get('note', '-')}")

    # 3차 만복 승인 완료 → 업로드
    if check_all_approved(video_key):
        print(f"\n[ApproveUpload] 3AI 전원 승인 완료 → 유튜브 업로드 시작!")
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        result = upload_video(
            file_path=str(video_path),
            title=args.title,
            tags=tags,
            video_type=args.type,
            privacy=args.privacy,
        )
        # 업로드 결과 저장
        approvals = load_approvals()
        approvals[video_key]["uploaded"] = {
            "url": result["url"],
            "video_id": result["video_id"],
            "ts": datetime.now().isoformat(),
        }
        APPROVAL_LOG.write_text(json.dumps(approvals, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[ApproveUpload] 완료: {result['url']}")
    else:
        print(f"\n[ApproveUpload] 다음 단계 승인 대기 중...")


if __name__ == "__main__":
    main()
