import os
import sys
import glob
import datetime
from google import genai

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SKILLS_DIR = r"D:\AI\.agents\skills"
EVAL_LOGS_DIR = r"D:\AI\AI_hub\shared\eval_logs"
INBOX_PATH = r"D:\AI\AI_hub\status\inbox.md"

def evaluate_skill(skill_path, client):
    skill_name = os.path.basename(os.path.dirname(skill_path))
    print(f"Evaluating skill: {skill_name}...")
    
    with open(skill_path, 'r', encoding='utf-8') as f:
        skill_content = f.read()
        
    prompt = f"""
당신은 완벽주의 성향을 가진 AI 스킬 검증 에이전트(Auditor)입니다.
아래 제공되는 파일은 특정 AI 에이전트 스킬의 행동 강령 및 테스트 케이스가 담긴 SKILL.md 파일입니다.

[요구사항]
이 스킬의 문서 내에는 반드시 'Eval 테스트 케이스(5개 이상)'와 '성공/실패 채점 기준(정량적 숫자)'이 명시되어 있어야 합니다. (만약 둘 중 하나라도 없으면 'FAIL: 자동 반려 (테스트 케이스 또는 채점 기준 누락)'으로 처리하십시오.)
문서에 테스트 케이스가 존재한다면, 당신이 직접 해당 에이전트라고 가정하고 각 테스트 케이스를 머릿속으로 시뮬레이션(실행)해 보십시오.
그리고 각 테스트 케이스가 '성공/실패 채점 기준'을 통과할 수 있는지 정량적으로 판단하여 결과를 도출하십시오.

[출력 형식]
반드시 다음 구조를 지켜서 답변하십시오.

### {skill_name} 검증 결과
- **테스트 케이스 존재 여부**: (있음/없음)
- **채점 기준 정량화 여부**: (정량적/비정량적)
- **시뮬레이션 통과 횟수**: (예: 4/5 통과)
- **최종판정**: (PASS 또는 FAIL) - 3개 이상 통과 및 정량적 채점 기준 충족 시 PASS

[SKILL.md 내용]
{skill_content}
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Error evaluating {skill_name}: {e}")
        return f"### {skill_name} 검증 결과\n- **최종판정**: ERROR (API 호출 실패 - {str(e)})"

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("FAIL: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    skill_files = glob.glob(os.path.join(SKILLS_DIR, "*", "SKILL.md"))
    if not skill_files:
        print("No SKILL.md files found.")
        sys.exit(0)
        
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    report_path = os.path.join(EVAL_LOGS_DIR, f"{today_str}_eval_report.md")
    
    report_lines = [
        f"# 📊 3AI 스킬 Eval 자동화 리포트 ({today_str})",
        "> **실행 시간**: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "> **목적**: 등록된 모든 스킬의 테스트 케이스 자동 시뮬레이션 및 정량 평가",
        "---",
        ""
    ]
    
    pass_count = 0
    fail_count = 0
    
    for sf in skill_files:
        result_text = evaluate_skill(sf, client)
        report_lines.append(result_text)
        report_lines.append("\n---\n")
        
        if "최종판정: PASS" in result_text.upper():
            pass_count += 1
        else:
            fail_count += 1
            
    report_lines.insert(4, f"### 📈 종합 요약\n- **총 스킬 수**: {len(skill_files)}\n- **PASS**: {pass_count}\n- **FAIL/ERROR**: {fail_count}\n---\n")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))
        
    print(f"Eval Report generated: {report_path}")
    
    # 코니에게 inbox.md 메시지 전송
    msg_id = datetime.datetime.now().strftime("%H:%M")
    coney_msg = f"  - [{msg_id}] `AI_hub/shared/eval_logs/{today_str}_eval_report.md` (Eval 자동 보고서 검토 요청)\n"
    
    if os.path.exists(INBOX_PATH):
        with open(INBOX_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        insert_idx = -1
        for i, line in enumerate(lines):
            if line.startswith("### 코니 수신"):
                insert_idx = i + 1
                break
                
        if insert_idx != -1:
            lines.insert(insert_idx, coney_msg)
            with open(INBOX_PATH, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print("Successfully sent message to Kony via inbox.md")
        else:
            print("Failed to find '### 코니 수신' in inbox.md")

if __name__ == "__main__":
    main()
