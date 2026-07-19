import os

AGENTS_FILE = r"D:\AI\.agents\AGENTS.md"

def scan_rules():
    if not os.path.exists(AGENTS_FILE):
        print("AGENTS.md 파일이 존재하지 않습니다.")
        return
        
    with open(AGENTS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    rule_headers = [l for l in lines if l.startswith('## ')]
    
    score = 100
    if len(rule_headers) > 20:
        score -= 10
    if len(lines) > 500:
        score -= 20
        
    print("=== AGENTS.md 자동 채점 (MD Management) ===")
    print(f"총 라인 수: {len(lines)}")
    print(f"등록된 규칙 수: {len(rule_headers)}")
    print(f"최적화 점수: {score}/100")
    print("---------------------------------------------")
    if score < 80:
        print("경고: 규칙이 너무 비대합니다. 압축 정리가 필요합니다.")
    else:
        print("상태: 매우 깔끔하게 유지되고 있습니다.")

if __name__ == "__main__":
    scan_rules()
