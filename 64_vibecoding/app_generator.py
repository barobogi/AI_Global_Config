import os
import re
import glob
import subprocess
import json

# Claude CLI 실행 파일 탐색 로직 (VSCode 확장 경로 탐색)
_claude_paths = glob.glob(r"C:\Users\82102\.vscode\extensions\anthropic.claude-code-*-win32-x64\resources\native-binary\claude.exe")
CLAUDE_EXE = sorted(_claude_paths)[-1] if _claude_paths else "claude.exe"

def apply_feedback_whitelist(app_dir: str, prompt: str) -> bool:
    """
    Apply whitelisted feedback commands using regex.
    Returns True if a whitelist command was matched and applied, False otherwise.
    """
    style_path = os.path.join(app_dir, "style.css")
    if not os.path.exists(style_path):
        return False

    with open(style_path, "r", encoding="utf-8") as f:
        css = f.read()

    applied = False

    # 1. 색상 [컬러]
    color_match = re.match(r'^색상\s+(.+)$', prompt.strip(), re.IGNORECASE)
    if color_match:
        color = color_match.group(1).strip()
        # Replace --main-color or any primary color variable
        css, n = re.subn(r'--main-color:\s*[^;]+;', f'--main-color: {color};', css)
        if n == 0:
            css = f":root {{\n  --main-color: {color};\n}}\n" + css
        applied = True

    # 2. 레이아웃 [유형]
    layout_match = re.match(r'^레이아웃\s+(.+)$', prompt.strip(), re.IGNORECASE)
    if layout_match:
        layout = layout_match.group(1).strip()
        if "2단" in layout:
            css, n = re.subn(r'--layout-grid:\s*[^;]+;', '--layout-grid: repeat(2, 1fr);', css)
        elif "3단" in layout:
            css, n = re.subn(r'--layout-grid:\s*[^;]+;', '--layout-grid: repeat(3, 1fr);', css)
        elif "1단" in layout:
            css, n = re.subn(r'--layout-grid:\s*[^;]+;', '--layout-grid: 1fr;', css)
        if layout_match:
            applied = True

    # 3. 폰트 [크기]
    font_match = re.match(r'^폰트\s+(.+)$', prompt.strip(), re.IGNORECASE)
    if font_match:
        size = font_match.group(1).strip()
        css, n = re.subn(r'--base-font-size:\s*[^;]+;', f'--base-font-size: {size};', css)
        applied = True

    if applied:
        with open(style_path, "w", encoding="utf-8") as f:
            f.write(css)
            
    return applied


def generate_with_llm(app_dir: str, prompt: str):
    """
    Generate or update app using Claude CLI via subprocess.
    """
    # Read existing files to give context if they exist
    existing_code = ""
    for file_name in ["index.html", "style.css", "script.js"]:
        path = os.path.join(app_dir, file_name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                existing_code += f"\n\n--- {file_name} ---\n"
                existing_code += f.read()
                
    system_prompt = f"""
You are an expert Web Application Generator.
Create a complete web application based on the user's prompt.
You MUST output EXACTLY three files: index.html, style.css, and script.js.
Use this specific format with markdown code blocks:

```html
<!-- HTML content here -->
```

```css
/* CSS content here */
:root {{
  --main-color: #5B8DEE;
  --layout-grid: 1fr;
  --base-font-size: 16px;
}}
```

```javascript
// JS content here
```

Ensure standard CSS variables like --main-color, --layout-grid, and --base-font-size are defined in :root.
"""
    if existing_code:
        system_prompt += f"\nHere is the existing code (modify it according to the prompt):\n{existing_code}"

    full_prompt = f"{system_prompt}\n\nUser Request: {prompt}"

    # Call Claude CLI via subprocess
    try:
        result = subprocess.run(
            [CLAUDE_EXE, "--print", full_prompt],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=120
        )
        response_text = result.stdout
    except Exception as e:
        response_text = f"Subprocess Error: {e}"
        with open(os.path.join(app_dir, "error.log"), "a", encoding="utf-8") as f:
            f.write(f"Failed to run Claude CLI:\n{response_text}\n")
        return

    # Parse the response and write files
    html_match = re.search(r'```html\n(.*?)\n```', response_text, re.DOTALL)
    css_match = re.search(r'```css\n(.*?)\n```', response_text, re.DOTALL)
    js_match = re.search(r'```(?:javascript|js)\n(.*?)\n```', response_text, re.DOTALL)
    
    os.makedirs(app_dir, exist_ok=True)
    
    if html_match:
        with open(os.path.join(app_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_match.group(1))
    if css_match:
        with open(os.path.join(app_dir, "style.css"), "w", encoding="utf-8") as f:
            f.write(css_match.group(1))
    if js_match:
        with open(os.path.join(app_dir, "script.js"), "w", encoding="utf-8") as f:
            f.write(js_match.group(1))
            
    # If no blocks matched, it might have failed to format. We just log it.
    if not html_match and not css_match:
        with open(os.path.join(app_dir, "error.log"), "a", encoding="utf-8") as f:
            f.write(f"Failed to parse LLM response:\n{result.stdout}\n")


def process_prompt(app_name: str, prompt: str):
    app_dir = os.path.join(os.path.dirname(__file__), "apps", app_name)
    os.makedirs(app_dir, exist_ok=True)
    
    # Try whitelist first
    if apply_feedback_whitelist(app_dir, prompt):
        return "whitelist"
        
    # Otherwise, LLM
    generate_with_llm(app_dir, prompt)
    return "llm"
