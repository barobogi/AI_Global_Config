# approve_and_upload.py — 만복 3차 승인 후 자동 업로드 실행
# 사용: python approve_and_upload.py --video crisp_dm_shorts.mp4 --title "..." --type shorts
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))
from youtube_uploader import upload_video

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
        shorts_suffix = " #Shorts" if args.type == "shorts" else ""

        # 기존 업로드된 영상 링크 수집 (cross-link용)
        approvals_now = load_approvals()
        uploaded_links = [
            v["uploaded"]["url"]
            for v in approvals_now.values()
            if "uploaded" in v and v["uploaded"].get("url")
        ]
        cross_link_block = ""
        if uploaded_links and args.type == "shorts":
            cross_link_block = "\n\n" + "\n".join(
                f"▶️ {u}" for u in uploaded_links[-3:]  # 최근 3개까지
            )
        elif uploaded_links and args.type == "main":
            cross_link_block = "\n\n" + "\n".join(
                f"📱 관련 쇼츠 → {u}" for u in uploaded_links[-3:]
            )

        desc = (
            "바로보기의 3AI 연구소\n\n"
            "만복(Claude Code CLI) + 코니(Cowork) + 안티(Antigravity) 3AI가 함께 만든 콘텐츠입니다."
            + cross_link_block
        )
        video_url = upload_video(
            video_path=str(video_path),
            title=args.title + shorts_suffix,
            description=desc,
            tags=tags or ["3AI", "AI자동화", "만복", "코니", "안티"],
            privacy_status=args.privacy,  # 2026-08-29 Hookify: --privacy 인자가 정의만 되고
            # upload_video()로 안 넘어가서 항상 unlisted로만 올라가던 버그(EP.03 "공개" 요청이
            # unlisted로 올라간 사고) 수정.
        )
        # 업로드 결과 저장
        approvals = load_approvals()
        approvals[video_key]["uploaded"] = {
            "url": video_url,
            "ts": datetime.now().isoformat(),
        }
        APPROVAL_LOG.write_text(json.dumps(approvals, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[ApproveUpload] 업로드 완료: {video_url}")

        # 고정 댓글로 관련 영상 링크 추가
        if cross_link_block:
            try:
                import pickle
                from googleapiclient.discovery import build
                from google.auth.transport.requests import Request as GRequest
                token_path = Path(__file__).parent / "token.pickle"
                with open(token_path, "rb") as f:
                    creds = pickle.load(f)
                if creds.expired and creds.refresh_token:
                    creds.refresh(GRequest())
                yt = build("youtube", "v3", credentials=creds)
                video_id = video_url.split("v=")[-1].split("&")[0].split("/")[-1]
                comment_text = cross_link_block.strip()
                yt.commentThreads().insert(
                    part="snippet",
                    body={"snippet": {"videoId": video_id, "topLevelComment": {"snippet": {"textOriginal": comment_text}}}}
                ).execute()
                print(f"[ApproveUpload] 고정 댓글 추가 완료")
            except Exception as e:
                print(f"[ApproveUpload] 고정 댓글 실패 (수동 추가 필요): {e}")
    else:
        print(f"\n[ApproveUpload] 다음 단계 승인 대기 중...")


if __name__ == "__main__":
    main()
