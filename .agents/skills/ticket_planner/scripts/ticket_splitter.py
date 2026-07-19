import argparse
import json
import os
from google import genai
from google.genai import types

def generate_tickets(prompt, answers):
    # Gemini SDK 클라이언트 초기화 (환경 변수 GEMINI_API_KEY 사용 권장, 없을 경우 하드코딩된 키 사용)
    api_key = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6LufZgpf1zlTE4sZV6ASoj50ir0nRhl4z7nm4bmM-3bjA")
    client = genai.Client(api_key=api_key)
    
    sys_prompt = """당신은 3AI 시스템의 수석 기획자(만복)를 돕는 티켓 분할 자동화 스크립트입니다.
사용자의 초기 요구사항과, 그에 대해 역면접(Grill)한 답변 내역을 바탕으로 완벽한 스펙(Spec)을 정의하고, 이를 개발자(안티)가 즉시 코딩할 수 있는 가장 작은 단위의 개발 티켓(Tickets)들로 분할하세요.

결과는 반드시 JSON 배열 포맷으로만 출력하세요. 
각 티켓은 우리의 규정인 GPS(Goal, Proof, Steps) 구조를 준수해야 합니다.
형식 예시: 
[
  {
    "ticket_id": 1,
    "title": "티켓 제목",
    "goal": "목표 (무엇을 달성하는가?)", 
    "proof": "완료 판단 기준 (어떻게 성공을 확인하는가?)", 
    "steps": ["절차1", "절차2"]
  }
]"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"초기 요구사항:\n{prompt}\n\n역면접 답변:\n{answers}\n\n티켓 분할을 시작하세요.",
            config=types.GenerateContentConfig(
                system_instruction=sys_prompt,
                response_mime_type="application/json"
            )
        )
        return response.text
    except Exception as e:
        return json.dumps([{"error": str(e)}])

def validate_gps_completeness(tickets):
    for ticket in tickets:
        tid = ticket.get('ticket_id', 'unknown')
        assert ticket.get('goal'), f"Ticket {tid}: Goal missing"
        assert ticket.get('proof'), f"Ticket {tid}: Proof missing"
        assert len(ticket.get('steps', [])) >= 3, f"Ticket {tid}: Steps < 3"
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="역면접 기반 티켓 분할 자동화 스크립트")
    parser.add_argument("--prompt", type=str, required=True, help="사용자 초기 요구사항 요약")
    parser.add_argument("--answers", type=str, required=True, help="역면접 답변 내역 요약")
    
    args = parser.parse_args()
    
    tickets_json = generate_tickets(args.prompt, args.answers)
    try:
        tickets = json.loads(tickets_json)
        validate_gps_completeness(tickets)
        print(json.dumps(tickets, indent=2, ensure_ascii=False))
    except AssertionError as ae:
        print(f"GPS 검증 실패: {ae}")
        print("Raw Output:", tickets_json)
    except Exception as e:
        print(f"JSON 파싱 에러: {e}")
        print("Raw Output:", tickets_json)
