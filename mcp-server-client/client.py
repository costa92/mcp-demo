#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any
from mcp import ClientSession
from contextlib import AsyncExitStack
from openai import AsyncOpenAI
import os
from mcp.client.sse import sse_client
import json
import logging
import asyncio
import sys
from mcp.types import Tool, CallToolResult

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPClient:
    def __init__(self, url: str = ""):
        """初始化MCP客户端
        
        Args:
            url: SSE服务器URL
        """
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self._streams_context = None
        self._session_context = None
        self.openai = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )

    async def connect_to_sse_server(self, server_url: str) -> None:
        """连接到SSE服务器
        
        Args:
            server_url: SSE服务器URL
        """
        logger.info(f"正在连接SSE服务器: {server_url}")
        self._streams_context = sse_client(url=server_url)
        streams = await self._streams_context.__aenter__()

        self._session_context = ClientSession(*streams)
        self.session = await self._session_context.__aenter__()
        await self.session.initialize()

        logger.info("已成功连接到SSE服务器")

    async def cleanup(self) -> None:
        """清理会话和流资源"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)
        logger.info("会话已关闭")
    
    def _prepare_tools(self, tools: List[Tool]) -> List[Dict[str, Any]]:
        """准备工具列表
        
        Args:
            tools: 工具列表
            
        Returns:
            格式化后的工具列表
        """
        return [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            }
        } for tool in tools]

    async def _handle_tool_call(self, tool_call, messages: List[Dict]) -> tuple[List[str], List[Dict]]:
        """处理工具调用
        
        Args:
            tool_call: 工具调用对象
            messages: 消息历史
            
        Returns:
            final_text: 最终文本列表
            tool_result: 工具调用结果列表
        """
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        final_text = []
        tool_result = []

        # 执行工具调用
        result = await self.session.call_tool(tool_name, tool_args)
        tool_result.append({"call": tool_name, "result": result})
        final_text.append(f"[调用工具 {tool_name}, 参数: {tool_args}]")

        # 继续对话
        messages.extend([
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [tool_call]
            },
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result.content[0].text
            }
        ])

        logger.info(f"工具 {tool_name} 调用完成, 参数: {tool_args}, 返回: {result.content[0].text}")

        return final_text, tool_result

    async def process_query(self, query: str) -> str:
        """处理查询并返回结果
        
        Args:
            query: 用户查询
            
        Returns:
            处理结果
        """
        logger.info(f"正在处理查询: {query}")

        messages = [{"role": "user", "content": query}]
        
        # 获取可用工具
        response = await self.session.list_tools()
        available_tools = self._prepare_tools(response.tools)

        # 调用OpenAI API
        completion = await self.openai.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )

        final_text = []
        tool_result = []
        assistant_message = completion.choices[0].message

        # 处理工具调用
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_texts, tool_results = await self._handle_tool_call(tool_call, messages)
                final_text.extend(tool_texts)
                tool_result.extend(tool_results)

                # 获取最终回复
                completion = await self.openai.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL"),
                    max_tokens=1000,
                    messages=messages
                )
                
                content = completion.choices[0].message.content
                final_text.append(str(content) if isinstance(content, (dict, list)) else content)
        else:
            content = assistant_message.content
            final_text.append(str(content) if isinstance(content, (dict, list)) else content)

        return "\n".join(final_text)

    async def chat_loop(self) -> None:
        """运行交互式聊天循环"""
        print("\nMCP 客户端已启动!")
        print("输入查询内容,输入'quit'退出")
        
        while True:
            try:
                query = input("\n查询: ").strip()
                
                if query.lower() == 'quit':
                    break
                    
                response = await self.process_query(query)
                print("\n" + response)
                    
            except Exception as e:
                logger.error(f"处理查询时发生错误: {str(e)}")
                print(f"\n错误: {str(e)}")


async def main() -> None:
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: uv run client.py <SSE MCP 服务器URL (例如: http://localhost:8080/sse)>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_sse_server(server_url=sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
