import os
import json

LOG_FILE = r"C:\Users\82102\.gemini\antigravity\brain\82673447-5345-4190-a04f-2179e9dc3de0\.system_generated\logs\transcript.jsonl"
OUT_FILE = r"C:\Users\82102\.gemini\antigravity\brain\82673447-5345-4190-a04f-2179e9dc3de0\session_report.html"

def generate_report():
    total_steps = 0
    errors = 0
    tools_used = {}
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    total_steps += 1
                    if data.get("status") == "ERROR":
                        errors += 1
                    if "tool_calls" in data:
                        for tc in data["tool_calls"]:
                            t_name = tc.get("function_name", "unknown")
                            tools_used[t_name] = tools_used.get(t_name, 0) + 1
                except:
                    pass

    html = f"""
    <html>
    <head><title>Session Report</title></head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h2>📊 Session Report (Auto-generated)</h2>
        <p><strong>Total Steps:</strong> {total_steps}</p>
        <p><strong>Total Errors:</strong> {errors}</p>
        <h3>🛠 Tools Used</h3>
        <ul>
    """
    for k, v in tools_used.items():
        html += f"<li>{k}: {v} times</li>\n"
    
    html += """
        </ul>
    </body>
    </html>
    """
    
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Report generated at: {OUT_FILE}")

if __name__ == "__main__":
    generate_report()
