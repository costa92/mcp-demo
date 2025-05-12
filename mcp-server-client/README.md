# MCP Server-Client 项目说明

## 项目简介

本项目基于 MCP 协议，结合 LangChain、OpenAI、SSE 等技术，提供了一个支持文档智能检索和工具调用的 Agent 服务（agentd）与客户端，适用于 AI 助手、智能问答、文档搜索等场景。

- 服务端支持通过 HTTP/SSE 协议接收消息，异步处理并返回结果。
- 客户端支持与服务端交互，自动调用工具，支持多种 LLM。
- 内置文档检索工具，支持 langchain、llama-index、autogen 等主流 AI 框架文档的智能搜索。

---

## 目录结构

```
├── main.py           # Stdio 协议服务端入口
├── service.py        # SSE/HTTP 服务端入口
├── client.py         # 客户端示例
├── requirements.txt  # 依赖包
├── pyproject.toml    # 项目元信息
├── .env copy         # 环境变量示例
├── Makefile          # 常用命令
```

---

## 快速开始

### 1. 安装依赖

建议使用 Python 3.10+，推荐使用虚拟环境：

```bash
# 安装 uv（如未安装）
make install-uv
# 创建虚拟环境
make create-venv
# 安装依赖
make install-deps
```

### 2. 配置环境变量

复制 `.env copy` 为 `.env` 并根据实际情况填写：

```
SERPER_API_KEY=你的Serper API Key
MCP_PORT=8000
MCP_SERVER_URL=http://localhost:8000
OPENAI_API_KEY=你的OpenAI Key
OPENAI_BASE_URL=你的OpenAI Base URL
OPENAI_MODEL=你的模型名（如 Qwen/Qwen3-235B-A22B）
```

---

### 3. 启动服务端

#### 方式一：Stdio 协议

```bash
python main.py
```

配置

```json
{
  "mcpServers": {
    "web-search": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "/home/hellotalk/code/ai/mcp-demo/mcp-server-client",
        "run",
        "main.py"
      ]
    }
  }
}
```

#### 方式二：SSE/HTTP 协议

```bash
uvicorn service:app --host 0.0.0.0 --port 8000
# 或
python service.py --host 0.0.0.0 --port 8000
```

---

### 4. 启动客户端

```bash
uv run client.py http://localhost:8000/sse
```


配置

```json
{
  "mcpServers": {
    "web-search": {
      "type": "http",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

---

## 主要功能

### 1. 智能文档检索工具
- 支持 langchain、llama-index、autogen、agno、openai-agents-sdk、mcp-doc、camel-ai、crew-ai 等主流 AI 框架文档的智能搜索。
- 自动调用 Serper API 进行网页检索，抓取并提取网页内容。

### 2. Agent 工具调用
- 支持通过 LLM 自动调用自定义工具（如文档检索、计算等）。
- 工具注册示例见 `main.py`、`service.py`。

### 3. SSE/HTTP 协议支持
- 服务端支持标准 HTTP POST 消息和 SSE 实时推送。
- 客户端支持与服务端的 SSE 长连接。

---

## 依赖说明

详见 `requirements.txt`，主要依赖：
- beautifulsoup4
- httpx
- mcp
- openai
- python-dotenv
- starlette
- uvicorn

---

## 常用命令

```bash
make install-uv        # 安装 uv
make create-venv       # 创建虚拟环境
make install-deps      # 安装依赖
```

---

## 参考文档
- [LangChain 官方文档](https://python.langchain.com/docs/)
- [MCP 协议](https://modelcontextprotocol.io/)
- [Serper API](https://serper.dev/)
- [OpenAI 官方文档](https://platform.openai.com/docs/)

---

## 常见问题

1. **服务端 202 Accepted**
   - 说明消息已被服务端接收，处理为异步。请通过轮询、SSE 或 WebSocket 获取最终结果。
2. **环境变量未配置**
   - 请确保 `.env` 文件已正确填写并加载。
3. **依赖安装失败**
   - 请确认 Python 版本 >= 3.10，且已正确创建虚拟环境。

---

## License
MIT
