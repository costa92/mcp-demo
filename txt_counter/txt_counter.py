import os
import logging
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True  # 强制重新配置日志
)
logger = logging.getLogger(__name__)

# 添加控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 创建 MCP Server
mcp = FastMCP("桌面 TXT 文件统计器")

@mcp.tool()
def count_desktop_txt_files() -> int:
    """Count the number of .txt files on the desktop."""
    # Get the desktop path
    username = os.getenv("USER") or os.getenv("USERNAME")
    desktop_path = Path(f"/Users/{username}/Desktop")
    logger.info(f"Scanning desktop path: {desktop_path}")
    
    # Count .txt files
    txt_files = list(desktop_path.glob("*.txt"))
    count = len(txt_files)
    logger.info(f"Found {count} .txt files on desktop")
    return count

@mcp.tool()
def list_desktop_txt_files() -> str:
    """Get a list of all .txt filenames on the desktop."""
    # Get the desktop path
    username = os.getenv("USER") or os.getenv("USERNAME")
    desktop_path = Path(f"/Users/{username}/Desktop")
    logger.info(f"Scanning desktop path: {desktop_path}")
    
    # Get all .txt files
    txt_files = list(desktop_path.glob("*.txt"))
    
    # Return the filenames
    if not txt_files:
        logger.info("No .txt files found on desktop")
        return "No .txt files found on desktop."
    
    # Format the list of filenames
    file_list = "\n".join([f"- {file.name}" for file in txt_files])
    logger.info(f"Found {len(txt_files)} .txt files on desktop")
    logger.debug(f"File list:\n{file_list}")
    return f"Found {len(txt_files)} .txt files on desktop:\n{file_list}"

if __name__ == "__main__":
    # Initialize and run the server
    logger.info("Starting MCP server...")
    mcp.run()