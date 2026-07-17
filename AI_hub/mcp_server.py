from flask import Flask, request, jsonify
import logging
import time

app = Flask(__name__)

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MCP_Bridge")

@app.route("/trigger_inbox_check", methods=["POST"])
def trigger_inbox_check():
    """
    master_watch.py로부터 inbox.md 변경 시 자동 트리거 수신
    Kony가 즉시 반응할 수 있는 엔드포인트
    """
    data = request.json or {}
    source = data.get("source", "unknown")
    logger.info(f"✅ [자동] Kony가 수신함 변경사항 감지 트리거 수신 (출처: {source})")
    
    # 여기서 코니가 inbox.md를 다시 읽고 후속 처리를 진행하게 됨
    # (실제 코니 AI의 처리는 별도로 연동됨)
    
    return jsonify({"status": "success", "message": "Trigger received successfully"}), 200

if __name__ == "__main__":
    logger.info("Starting Kony MCP Bridge Server on port 5003...")
    app.run(host="127.0.0.1", port=5003, debug=False)
