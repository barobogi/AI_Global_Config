import asyncio
import os
import logging
from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.types import Resource

# Stdio 통신을 방해하지 않도록 로그는 파일에만 남김
logging.basicConfig(
    filename=r"d:\AI\AI_hub\mcp_server_push.log", 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

server = Server("kony_inbox_monitor")
INBOX_PATH = r"d:\AI\AI_hub\status\inbox.md"
active_session = None

@server.list_resources()
async def list_resources() -> list[Resource]:
    global active_session
    # Claude Desktop이 초기화 후 리소스를 요청할 때 세션을 탈취하여 백그라운드 태스크에서 사용
    active_session = server.request_context.session
    logging.info("Active session captured from list_resources.")
    return [Resource(uri="file:///inbox.md", name="Kony Inbox", mimeType="text/markdown")]

@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "file:///inbox.md":
        logging.info("Claude Desktop is reading the inbox resource.")
        if os.path.exists(INBOX_PATH):
            with open(INBOX_PATH, "r", encoding="utf-8") as f:
                return f.read()
        return ""
    raise ValueError(f"Unknown resource: {uri}")

async def monitor_file():
    global active_session
    last_mtime = 0
    if os.path.exists(INBOX_PATH):
        last_mtime = os.path.getmtime(INBOX_PATH)
    
    logging.info("Background monitor started.")
    while True:
        await asyncio.sleep(1)
        if active_session and os.path.exists(INBOX_PATH):
            current = os.path.getmtime(INBOX_PATH)
            if current > last_mtime:
                last_mtime = current
                logging.info("Detected inbox change. Sending resource updated notification.")
                try:
                    await active_session.send_resource_updated("file:///inbox.md")
                    logging.info("Notification sent successfully to Claude Desktop.")
                except Exception as e:
                    logging.error(f"Error sending notification: {e}")

async def main():
    logging.info("Starting Kony MCP Stdio Server...")
    # 파일 감시 백그라운드 태스크 실행
    asyncio.create_task(monitor_file())
    
    # Stdio 서버 실행
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, 
            write_stream, 
            server.create_initialization_options()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Server stopped.")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
