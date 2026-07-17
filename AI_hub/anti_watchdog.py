import os
import sys
import time

TRIGGER_FILE = r"d:\AI\AI_hub\status\trigger_anti.txt"

def main():
    print("[Anti Watchdog] 안티 전용 워치독(백그라운드 태스크) 시작됨...", flush=True)
    
    # 트리거 파일이 없으면 생성
    if not os.path.exists(TRIGGER_FILE):
        with open(TRIGGER_FILE, "w") as f:
            f.write("init")
            
    last_mtime = os.path.getmtime(TRIGGER_FILE)
    
    while True:
        time.sleep(1.0)
        try:
            current_mtime = os.path.getmtime(TRIGGER_FILE)
            if current_mtime > last_mtime:
                last_mtime = current_mtime
                print("\n[Anti Trigger] 🚨 새 메시지가 발송되었습니다! inbox.md를 확인하고 즉각 대응하세요!", flush=True)
        except Exception as e:
            # 파일이 지워졌거나 접근 불가능할 경우 무시
            pass

if __name__ == "__main__":
    main()
