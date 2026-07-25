import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\AI\Temp_Manbok\langgraph_transcript.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 전체를 1000줄 단위로 청크 분할하여 핵심 내용 추출
chunks = {}
chunk_size = 1000
for i in range(0, len(lines), chunk_size):
    chunk = lines[i:i+chunk_size]
    start_time = chunk[0].split(']')[0].strip('[') if chunk else '00:00'
    end_time = chunk[-1].split(']')[0].strip('[') if chunk else '00:00'
    chunks[f"{start_time}~{end_time}"] = ''.join(chunk)

# 특허 관련 핵심 키워드 집중 검색
patent_keywords = {
    '단일 런타임/환경 제약': ['단일', '동일한 환경', '같은 환경', '파이썬 런타임', '프로세스'],
    '멀티에이전트 구조': ['멀티에이전트', '멀티 에이전트', '슈퍼바이저', '워커', 'supervisor', 'worker'],
    '스테이트 공유': ['스테이트', 'state', '공유 메모리', '공유 스토리지'],
    '오케스트레이션': ['오케스트레이션', 'orchestration', '지휘자', '라우터'],
    '통신/동기화': ['통신', '동기화', '메시지', '이벤트'],
    '플랫폼 제약': ['플랫폼', '샌드박스', '외부', '격리'],
}

report_lines = []
report_lines.append("# 🔍 LangGraph 자막 뽀개기 - 특허 11_18 차별성 분석 리포트")
report_lines.append(f"\n분석 대상: https://youtu.be/3My9sphTxtk")
report_lines.append(f"총 자막 세그먼트: {len(lines):,}개")
report_lines.append(f"\n분석 목적: LangGraph의 기술적 한계를 명확히 파악하여 특허 Seed 11_18(MCP 브릿지 이종 동기화)의 비자명성(Non-obviousness) 및 진보성 논리 강화\n")
report_lines.append("\n---\n")

for category, keywords in patent_keywords.items():
    hits = []
    for i, line in enumerate(lines):
        for kw in keywords:
            if kw in line:
                # 앞뒤 문맥 포함
                ctx_start = max(0, i-2)
                ctx_end = min(len(lines), i+3)
                ctx = ' '.join(l.strip() for l in lines[ctx_start:ctx_end])
                hits.append(f"  - L{i+1}: {ctx[:200]}")
                break
    
    report_lines.append(f"\n## 【{category}】 ({len(hits)}건 적중)")
    if hits:
        for h in hits[:10]:  # 카테고리당 최대 10개
            report_lines.append(h)
    else:
        report_lines.append("  - (해당 내용 없음)")

# 5강 멀티에이전트 구간 전체 추출
report_lines.append("\n---\n")
report_lines.append("## 【5강 멀티에이전트 전체 구간】\n")
in_5gang = False
for i, line in enumerate(lines):
    if '5강' in line:
        in_5gang = True
    if in_5gang:
        report_lines.append(f"  {line.strip()}")
    if i > 10000 and in_5gang:
        break

with open(r'D:\AI\Temp_Manbok\langgraph_patent_analysis.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print(f"✅ 분석 완료: D:\\AI\\Temp_Manbok\\langgraph_patent_analysis.md")
print(f"총 {len(report_lines)}줄 리포트 생성")
