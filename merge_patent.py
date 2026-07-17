import pathlib

v03_path = pathlib.Path(r'D:\AI\11_특허아이디어\변호별정리\11_18_이종AI_MCP_브릿지동기화\11_18_이종AI_MCP_브릿지동기화_최종_v0.3.md')
coni_path = pathlib.Path(r'd:\AI\AI_hub\shared\messages\코니→만복_20260717_T026완성_특허보강_통합과제.md')
v05_path = pathlib.Path(r'D:\AI\11_특허아이디어\변호별정리\11_18_이종AI_MCP_브릿지동기화\11_18_이종AI_MCP_브릿지동기화_최종_v0.5.md')

v03 = v03_path.read_text(encoding='utf-8')
coni = coni_path.read_text(encoding='utf-8')

# Extract "예제 7" part from Coni
part_a_start = coni.find('## 예제 7: 실제 3AI 협업 시스템 (T026 자율감시 파이프라인)')
part_a_end = coni.find('---', part_a_start)
part_a = coni[part_a_start:part_a_end].strip()

# Extract "8-7" part from Coni
part_b_start = coni.find('### 8-7. 실제 엔터프라이즈 구현을 통한 입증')
part_b_end = coni.find('---', part_b_start)
part_b = coni[part_b_start:part_b_end].strip()

# Insert part A into v03 after "6. 발명의 효과"
# Wait, let's just insert it exactly before "## 7. 선행 기술 분석"
v03 = v03.replace('## 7. 선행 기술 분석 (진보성 입증)', part_a + '\n\n---\n\n## 7. 선행 기술 분석 (진보성 입증)')

# Insert part B into v03 at the end of section 8 (before "## 9. 청구항")
v03 = v03.replace('## 9. 청구항 (Claims)', part_b + '\n\n---\n\n## 9. 청구항 (Claims)')

# Update version header
v03 = v03.replace('**버전**: v0.4 (최종본 — 오류 수정 완료)', '**버전**: v0.5 (최종본 — T026 사례 보강 완료)')
v03 = v03.replace('**기여자**: 안티(LangGraph 분석) + 코니(명세서 보강 + 오류 정정)', '**기여자**: 안티(LangGraph 분석) + 코니(명세서 보강 + 오류 정정 + T026 파이프라인 보강)')

v05_path.write_text(v03, encoding='utf-8')
print("v0.5 created successfully!")
