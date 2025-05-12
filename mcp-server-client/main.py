#! /usr/bin/env python3


import json
import os
import httpx
import logging
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
from typing import Dict, Optional, List

mcp = FastMCP("agentdocs-service")

# 确保环境变量加载
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_AGENT = "Agentdocs-app/1.0"
SERPER_URL = "https://google.serper.dev/search"

# 文档URL映射
docs_urls: Dict[str, str] = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable", 
    "autogen": "microsoft.github.io/autogen/stable",
    "agno": "docs.agno.com",
    "openai-agents-sdk": "openai.github.io/openai-agents-python",
    "mcp-doc": "modelcontextprotocol.io",
    "camel-ai": "docs.camel-ai.org",
    "crew-ai": "docs.crewai.com"
}

async def search_web(query: str) -> Optional[Dict]:
    """
    使用Google Serper API搜索网页内容
    
    Args:
        query: 搜索查询字符串
    
    Returns:
        搜索结果字典或None(如果发生错误)
    """
    if not os.getenv("SERPER_API_KEY"):
        logger.error("SERPER_API_KEY not found in environment variables")
        return None
        
    payload = json.dumps({"q": query, "num": 2})
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-Key": os.getenv("SERPER_API_KEY"),
        "User-Agent": USER_AGENT
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SERPER_URL,
                headers=headers,
                data=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.error(f"Error occurred during web search: {e}")
            return None

async def get_web_content(url: str) -> Optional[str]:
    """
    获取网页内容并提取文本
    
    Args:
        url: 网页URL
    
    Returns:
        网页文本内容或None(如果发生错误)
    """
    headers = {"User-Agent": USER_AGENT}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 移除脚本和样式元素
            for script in soup(["script", "style"]):
                script.decompose()
                
            return soup.get_text(separator="\n").strip()
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.error(f"Error occurred while fetching content: {e}")
            return None

@mcp.tool()
async def get_docs(query: str, library: str) -> str:
    """
    搜索给定查询和库的最新文档。
    支持 langchain、llama-index、autogen、agno、openai-agents-sdk、mcp-doc、camel-ai 和 crew-ai。

    Args:
        query: 要搜索的查询 (例如 "React Agent")
        library: 要搜索的库 (例如 "agno")

    Returns:
        文档中的文本内容

    Raises:
        ValueError: 当指定的库不受支持时
    """
    # 验证库是否支持
    if not query or not library:
        return "Query and library parameters cannot be empty"
        
    library = library.lower().strip()
    if library not in docs_urls:
        raise ValueError(f"Library {library} not supported. Supported libraries: {', '.join(docs_urls.keys())}")
    
    # 构建搜索查询
    search_query = f"site:{docs_urls[library]} {query}"
    
    # 执行搜索
    results = await search_web(search_query)
    if not results or not results.get("organic"):
        return "No results found"
    
    # 获取并合并所有结果文本
    texts: List[str] = []
    for result in results["organic"]:
        if "link" not in result:
            continue
            
        content = await get_web_content(result["link"])
        if content:
            texts.append(content)
    
    if not texts:
        return "No valid content found"
        
    return "\n\n---\n\n".join(texts)

# Stdio协议
if __name__ == "__main__":
    mcp.run(transport="stdio")