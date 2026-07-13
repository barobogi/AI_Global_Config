"""
T063 유튜브 파이프라인 — AI Study 게시글 자동 수집기
ai-study.html에서 최신 게시글을 파싱하여 대본으로 변환
"""
import os
import re
from html.parser import HTMLParser

AI_STUDY_PATH = r"D:\AI\Daily_for_Barobogi\ai-study.html"

class StudyCardParser(HTMLParser):
    """ai-study.html에서 study-card 데이터를 추출하는 파서"""
    
    def __init__(self):
        super().__init__()
        self.cards = []
        self._in_card = False
        self._in_title = False
        self._in_content = False
        self._in_meta = False
        self._current_card = {}
        self._depth = 0
        self._card_depth = 0
        self._title_done = False
        self._content_done = False
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # study-card div 감지
        if tag == "div" and "study-card" in attrs_dict.get("class", ""):
            self._in_card = True
            self._card_depth = self._depth
            self._current_card = {
                "id": attrs_dict.get("data-id", ""),
                "category": attrs_dict.get("data-category", ""),
                "title": "",
                "content": "",
                "meta": ""
            }
            self._title_done = False
            self._content_done = False
        
        if self._in_card:
            self._depth += 1
            classes = attrs_dict.get("class", "")
            
            # 제목 p 태그 감지
            if tag == "p" and "font-semibold" in classes and not self._title_done:
                self._in_title = True
            
            # 내용 p 태그 감지
            if tag == "p" and "content-preview" in classes and not self._content_done:
                self._in_content = True
        else:
            self._depth += 1
    
    def handle_endtag(self, tag):
        self._depth -= 1
        
        if self._in_title and tag == "p":
            self._in_title = False
            self._title_done = True
        
        if self._in_content and tag == "p":
            self._in_content = False
            self._content_done = True
        
        # card 종료
        if self._in_card and tag == "div" and self._depth <= self._card_depth:
            if self._current_card.get("title"):
                self.cards.append(self._current_card.copy())
            self._in_card = False
            self._current_card = {}
    
    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        
        if self._in_title:
            self._current_card["title"] += data
        elif self._in_content:
            self._current_card["content"] += data + " "


def get_latest_study_posts(count=3):
    """ai-study.html에서 최신 N개의 게시글을 파싱하여 반환"""
    with open(AI_STUDY_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    
    parser = StudyCardParser()
    parser.feed(html)
    
    return parser.cards[:count]


def post_to_script(post):
    """게시글 데이터를 TTS용 대본으로 변환"""
    title = post["title"]
    content = post["content"]
    
    # 이모지/특수문자 제거 (TTS 발음 방지)
    content_clean = re.sub(r'[🗂🔑⚠💡🌱🛑🔥🛠️💡📌✅❌🎉]', '', content)
    content_clean = re.sub(r'\s+', ' ', content_clean).strip()
    
    # 앞부분 300자만 요약 대본으로 사용 (쇼츠는 60초 이내)
    summary = content_clean[:300] if len(content_clean) > 300 else content_clean
    
    script = f"오늘의 AI Study입니다. 제목은 {title} 입니다. {summary}"
    return script


if __name__ == "__main__":
    print("=== AI Study 최신 게시글 파싱 테스트 ===\n")
    posts = get_latest_study_posts(count=1)
    
    for post in posts:
        print(f"[ID] {post['id']}")
        print(f"[제목] {post['title']}")
        print(f"[내용 미리보기] {post['content'][:100]}...")
        print(f"\n[생성된 대본]")
        print(post_to_script(post))
        print("-" * 60)
