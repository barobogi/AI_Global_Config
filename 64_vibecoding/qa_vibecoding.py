import os
import re
from html.parser import HTMLParser

class SimpleHTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.errors = []
        self.void_elements = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def handle_starttag(self, tag, attrs):
        if tag not in self.void_elements:
            self.tags.append(tag)
        # 접근성(A11y) 체크: img 태그에 alt 속성 필수
        if tag == 'img':
            has_alt = any(attr[0] == 'alt' for attr in attrs)
            if not has_alt:
                self.errors.append("[접근성] <img> 태그에 alt 속성이 누락되었습니다.")

    def handle_endtag(self, tag):
        if tag not in self.void_elements:
            if not self.tags:
                self.errors.append(f"닫는 태그 </{tag}>가 있지만 열린 태그가 없습니다.")
            elif self.tags[-1] == tag:
                self.tags.pop()
            else:
                self.errors.append(f"태그 불일치: <{self.tags[-1]}>가 열려있는데 </{tag}>로 닫혔습니다.")

def validate_html(html_path):
    if not os.path.exists(html_path):
        return ["HTML 파일이 없습니다."]
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    validator = SimpleHTMLValidator()
    try:
        validator.feed(html_content)
    except Exception as e:
        return [f"HTML 파싱 중 치명적 에러: {str(e)}"]
    
    if validator.tags:
        validator.errors.append(f"닫히지 않은 태그가 있습니다: {', '.join(validator.tags)}")
        
    # 시맨틱 헤딩(접근성) 체크
    if '<h1' not in html_content:
        validator.errors.append("[접근성] 문서에 <h1> 태그가 없습니다. (시맨틱 웹 위반)")
        
    return validator.errors

def validate_js(js_path):
    if not os.path.exists(js_path):
        return []
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    if content.count('{') != content.count('}'):
        errors.append("JavaScript 중괄호 '{', '}' 짝이 맞지 않습니다.")
    if content.count('(') != content.count(')'):
        errors.append("JavaScript 소괄호 '(', ')' 짝이 맞지 않습니다.")
        
    # 보안(Security) 스캔
    if 'eval(' in content:
        errors.append("[보안] 위험한 eval() 함수 사용이 감지되었습니다.")
    if 'innerHTML' in content:
        errors.append("[보안] XSS 공격 위험이 있는 innerHTML 사용이 감지되었습니다.")
    if re.search(r'(AIza[0-9A-Za-z-_]{35}|sk-[a-zA-Z0-9]{48})', content):
        errors.append("[보안] 하드코딩된 API 키(Google 또는 OpenAI 패턴)가 감지되었습니다.")
        
    return errors

def validate_css(css_path):
    if not os.path.exists(css_path):
        return []
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    if content.count('{') != content.count('}'):
        errors.append("CSS 중괄호 '{', '}' 짝이 맞지 않습니다.")
    return errors

def run_qa(app_dir):
    errors = []
    html_path = os.path.join(app_dir, "index.html")
    js_path = os.path.join(app_dir, "script.js")
    css_path = os.path.join(app_dir, "style.css")
    
    html_errs = validate_html(html_path)
    if html_errs:
        errors.extend([f"[HTML] {err}" for err in html_errs])
        
    js_errs = validate_js(js_path)
    if js_errs:
        errors.extend([f"[JS] {err}" for err in js_errs])
        
    css_errs = validate_css(css_path)
    if css_errs:
        errors.extend([f"[CSS] {err}" for err in css_errs])
        
    return errors
