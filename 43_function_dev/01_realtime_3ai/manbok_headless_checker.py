"""
만복 전용 헤드리스 스케줄 폴링 스크립트 (보완책)
Project: 43_function_dev/01_realtime_3ai
Author: Anti (Operator) / Requested by: Manbok (PM)

동작:
1. realtime_3ai.db에서 recipient in ('manbok', 'all') AND status='unread' 메시지 조회
2. 미확인 메시지가 존재하면 만복이의 실제 Claude Code CLI (claude -p)를 호출하여 답변 생성
3. 생성된 답변을 realtime_3ai.db에 정식 write 후 상태를 read로 갱신
4. Windows Task Scheduler에 등록하여 10~15분 간격 자동 실행 가능
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
from realtime_engine import Realtime3AIEngine

def check_and_process_manbok_inbox():
    engine = Realtime3AIEngine()
    unread = engine.get_unread_messages("manbok")
    
    if not unread:
        print("[Manbok Headless] 처리할 미확인 메시지가 없습니다.")
        return

    print(f"[Manbok Headless] 📩 미확인 메시지 {len(unread)}건 발견. Claude CLI 처리 시작...")
    
    for msg in unread:
        msg_id = msg["msg_id"]
        sender = msg["sender"]
        content = msg["content"]
        conv_id = msg["conversation_id"]
        
        print(f"\n--- [메시지 ID: {msg_id}] 발신자: {sender} (주제: {conv_id}) ---")
        print(f"내용:\n{content}\n")
        
        # 만복 전용 Claude 프롬프트 구성
        prompt = (
            f"당신은 3AI의 맏형이자 총괄 기획자(PM) '만복'입니다. "
            f"다음은 3AI 실시간 통신망을 통해 '{sender}'가 보낸 메시지입니다.\n\n"
            f"--- 메시지 내용 ---\n{content}\n------------------\n\n"
            f"총괄 PM의 관점에서 명확하고 핵심적인 답변을 작성해 주세요."
        )
        
        try:
            # 실제 로컬 Claude CLI (Headless 모드) 실행 시도
            claude_cmd = ["claude", "-p", prompt]
            proc = subprocess.run(
                claude_cmd, 
                capture_output=True, 
                text=True, 
                encoding="utf-8", 
                timeout=90
            )
            
            if proc.returncode == 0 and proc.stdout.strip():
                reply_content = proc.stdout.strip()
                print(f"✅ Claude CLI 응답 수신 완료 ({len(reply_content)}자)")
                
                # DB에 만복의 응답 기록
                reply_id = engine.send_message(
                    sender="manbok",
                    recipient=sender,
                    content=reply_content,
                    conversation_id=conv_id,
                    tier=1,
                    metadata={"source": "manbok_headless_cli"}
                )
                print(f"💾 응답 저장 완료 (MSG ID: {reply_id})")
                engine.mark_message_status(msg_id, "processed")
            else:
                print(f"⚠️ Claude CLI 실행 반환 코드: {proc.returncode}. (Stderr: {proc.stderr[:150]})")
                
        except FileNotFoundError:
            print("ℹ️ 'claude' CLI 명령어를 찾을 수 없습니다. (대화형 VS Code 세션에서 응답 권장)")
        except Exception as e:
            print(f"❌ 헤드리스 실행 중 오류: {e}")

if __name__ == "__main__":
    check_and_process_manbok_inbox()
