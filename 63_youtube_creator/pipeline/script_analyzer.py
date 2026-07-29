"""
Script Analyzer & TTS Hardener (v0.2)
- 인트로 훅 길이/자수 검증
- 평균 문장 길이 및 낭독 속도(350자/분 기준) 계산
- 반복 단어/핵심 단어 분포 분석
- [하드닝 훅] 3AI -> 쓰리에이아이, AI -> 에이아이 자동 독음 교정 및 하드 검증
"""
import os
import sys
import re
from collections import Counter

if sys.stdout is not None and getattr(sys.stdout, 'encoding', None) is not None:
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

STOPWORDS = {
    "그리고", "그런데", "그래서", "하지만", "저희는", "우리는", "저희가", "우리가",
    "이제", "이런", "저런", "그런", "이것", "저것", "그것", "때문에", "그러면",
    "합니다", "습니다", "있습니다", "됩니다", "입니다",
}

def validate_and_fix_tts_pronunciation(script_text: str) -> tuple[str, bool]:
    """
    TTS 낭독용 텍스트에서 '3AI' -> '쓰리에이아이', 'AI' -> '에이아이' 독음 자동 교정 훅.
    반환: (교정된 tts_text, 교정 발생 여부)
    """
    fixed_text = script_text
    is_modified = False
    
    # 1. 3AI -> 쓰리에이아이 (삼 에이 아이 낭독 오류 방지)
    if re.search(r'\b3AI\b', fixed_text, re.IGNORECASE) or '3AI' in fixed_text:
        fixed_text = re.sub(r'3AI', '쓰리에이아이', fixed_text)
        fixed_text = re.sub(r'3ai', '쓰리에이아이', fixed_text)
        is_modified = True
        
    # 2. AI -> 에이아이 (단독 AI 낭독 안정화)
    if re.search(r'\bAI\b', fixed_text):
        fixed_text = re.sub(r'\bAI\b', '에이아이', fixed_text)
        is_modified = True
        
    return fixed_text, is_modified

def analyze_script(script_text):
    print("==================================================")
    print("📊 대본 정량 분석기 (Script Analyzer v0.2)")
    print("==================================================")
    
    # 0. TTS 독음 하드닝 검사
    tts_text, modified = validate_and_fix_tts_pronunciation(script_text)
    if modified:
        print("🚨 [TTS 하드닝] '3AI' -> '쓰리에이아이' / 'AI' -> '에이아이' 독음 교정이 자동 적용되었습니다.")
    else:
        print("✅ [TTS 하드닝] 독음 예외 항목 없음 (쓰리에이아이 표기 준수 확인)")
    
    # 1. 공백 제외 순수 글자수 및 예상 시간
    clean_text = re.sub(r'\s+', '', script_text)
    total_chars = len(clean_text)
    est_seconds = (total_chars / 350.0) * 60.0
    
    print(f"📏 총 글자수 (공백 제외): {total_chars}자")
    print(f"⏱️ 예상 낭독 시간: 약 {est_seconds:.1f}초 (골든렝스 35~40초 준수 여부 체크)")
    
    # 2. 문장 분할 및 평균 문장 길이
    sentences = [s.strip() for s in re.split(r'[.!?]\s*', script_text) if s.strip()]
    total_sentences = len(sentences)
    avg_sentence_len = (total_chars / total_sentences) if total_sentences > 0 else 0
    
    print(f"📝 총 문장 수: {total_sentences}개")
    print(f"📐 평균 문장 길이: 약 {avg_sentence_len:.1f}자")
    
    # 3. 인트로 훅 분석 (첫 1~2문장)
    if sentences:
        hook_text = sentences[0]
        hook_chars = len(re.sub(r'\s+', '', hook_text))
        HOOK_LIMIT_CHARS = 18
        print(f"⚓ 인트로 훅 문장: \"{hook_text}\" ({hook_chars}자)")
        if hook_chars <= HOOK_LIMIT_CHARS:
            print(f"✅ [Pass] 훅 문장이 간결하여 시청자 이탈 방지에 효과적입니다 ({HOOK_LIMIT_CHARS}자 이내, 약 3초).")
        else:
            print(f"⚠️ [Warning] 훅 문장이 깁니다. {HOOK_LIMIT_CHARS}자 이내(약 3초)로 단축을 권장합니다.")

    # 4. 키워드 빈도 분석
    words = re.findall(r'[가-힣a-zA-Z0-9]+', script_text)
    words_filtered = [w for w in words if len(w) > 1 and w not in STOPWORDS]
    counter = Counter(words_filtered)
    top_keywords = counter.most_common(5)
    
    print(f"🏷️ 상위 반복 키워드 5선: {top_keywords}")
    print("==================================================")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        text = "3AI가 유튜브 영상을 보고 스스로 똑똑해진다면, 믿으시겠어요? 저희 3AI는 매일 저녁 기술 채널을 훑어봅니다."
        
    analyze_script(text)
