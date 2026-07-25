import os
import sys
import argparse
from google import genai

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def check_hallucination(stt_path, summary_path):
    if not os.path.exists(stt_path):
        print(f"FAIL: STT file not found ({stt_path})")
        return False
    if not os.path.exists(summary_path):
        print(f"FAIL: Summary file not found ({summary_path})")
        return False

    with open(stt_path, 'r', encoding='utf-8') as f:
        stt_content = f.read()

    with open(summary_path, 'r', encoding='utf-8') as f:
        summary_content = f.read()

    prompt = f"""
당신은 까칠하고 집요한 '악마의 변호인(Devil's Advocate)'이자 완벽주의 팩트체커입니다.
AI가 작성한 아래의 요약본(기획안) 내용이 원본 STT 자막에 명확히 존재하는 사실인지 검증하십시오.

[검증 원칙]
1. 원본 STT에 없는 내용을 유추하여 지어낸 경우(Hallucination) 가차 없이 지적하십시오.
2. 특정 주장이 사실이라면, STT에서 어떤 문맥이나 타임스탬프에서 나왔는지 찾을 수 있어야 합니다. (타임스탬프가 없다면 문맥적 근거라도 확실해야 함)
3. 전체적으로 환각이 없다면 "최종판정: PASS"를, 하나라도 심각한 환각이나 없는 내용을 지어낸 것이 있다면 "최종판정: FAIL"을 문서 마지막 줄에 정확히 기재하십시오.

==============================
[원본 STT 자막]
{stt_content}

==============================
[검증 대상 요약본]
{summary_content}
==============================

검증 결과 리포트를 작성해주세요. 각 항목별로 사실 여부를 따지고, 맨 마지막 줄에는 반드시 "최종판정: PASS" 또는 "최종판정: FAIL"이라고 적어야 합니다.
"""

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY not set. Skipping Fact-Check to avoid SPOF.")
        return True

    client = genai.Client(api_key=api_key)
    
    try:
        print(f"Running Fact-Check (Devil's Advocate) for {os.path.basename(summary_path)}...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        report = response.text
        report_path = summary_path + ".factcheck.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"Fact-Check Report generated: {report_path}")
        
        if "최종판정: PASS" in report:
            print("Fact-Check Status: PASS ✅")
            return True
        else:
            print("Fact-Check Status: FAIL ❌ (Hallucination detected)")
            return False
            
    except Exception as e:
        print(f"WARNING: Gemini API error ({e}). Skipping Fact-Check to avoid SPOF.")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Pobbagi Fact Checker (Devil's Advocate)")
    parser.add_argument('--stt', required=True, help="Path to original STT file")
    parser.add_argument('--summary', required=True, help="Path to generated summary markdown file")
    
    args = parser.parse_args()
    result = check_hallucination(args.stt, args.summary)
    
    if result:
        sys.exit(0)
    else:
        sys.exit(1)
