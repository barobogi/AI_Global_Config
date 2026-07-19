import os
import json
import re
import glob

QUEUE_FILE = r"D:\AI\25_auto_pobbagi\youtube_queue.json"
TRANSCRIPTS_DIR = r"D:\AI\25_auto_pobbagi\transcripts"

def clean_vtt(vtt_content):
    """VTT 파일에서 시간 태그와 불필요한 메타데이터를 제거하고 순수 텍스트만 추출"""
    lines = vtt_content.splitlines()
    text_lines = []
    
    for line in lines:
        # 시간 정보 (00:00:00.000 --> 00:00:00.000) 건너뛰기
        if "-->" in line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
            
        # VTT 태그 (<c>, </c>, <00:00:00.000>) 제거
        clean_line = re.sub(r'<[^>]+>', '', line)
        clean_line = clean_line.strip()
        
        if clean_line and clean_line not in text_lines:
            # 중복 라인 방지 (유튜브 자동 자막은 종종 중복 출력됨)
            if not text_lines or text_lines[-1] != clean_line:
                text_lines.append(clean_line)
                
    return " ".join(text_lines)

def run_auto_pobbagi():
    if not os.path.exists(QUEUE_FILE):
        print("대기열 파일이 없습니다.")
        return
        
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)
        
    processed = queue.get("processed", [])
    if not processed:
        print("자막이 추출된 영상이 없습니다.")
        return
        
    print(f"총 {len(processed)}개의 영상 자막을 정제합니다.")
    
    for vid in processed:
        if vid.get("status") == "extracted" and "transcript_path" in vid:
            vtt_path = vid["transcript_path"]
            
            if os.path.exists(vtt_path):
                with open(vtt_path, "r", encoding="utf-8") as f:
                    vtt_content = f.read()
                    
                clean_text = clean_vtt(vtt_content)
                
                # 정제된 텍스트 저장
                txt_path = vtt_path.replace(".vtt", ".txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(f"제목: {vid['title']}\n")
                    f.write(f"채널: {vid['channel_name']}\n")
                    f.write(f"링크: {vid['link']}\n")
                    f.write("-" * 50 + "\n\n")
                    f.write(clean_text)
                    
                print(f"[{vid['video_id']}] 자막 정제 완료 -> {txt_path}")
                vid["status"] = "cleaned"
                vid["clean_text_path"] = txt_path
                
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=4)
        
    print("=== 자동 뽀개기(정제 단계) 완료! 이제 만복이 요약 프롬프트를 넘겨받을 차례입니다. ===")

if __name__ == "__main__":
    run_auto_pobbagi()
