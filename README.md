# MCP Demo 项目总览

本项目包含多个基于 MCP 协议和现代 Python 技术栈的子模块，涵盖智能 Agent 服务、TXT 文件统计工具、质数判断服务等，适用于 AI 助手、自动化工具集成、智能问答等多种场景。

---

## MCP Server

本项目支持两种主要的服务端通信协议：

1. **Stdio 传输协议（本地）**：适合本地进程间通信，低延迟，易于集成到本地开发环境。
2. **SSE 传输协议（远程）**：基于 HTTP 的 Server-Sent Events，适合远程服务和实时推送场景。

---

## 环境配置

1. **安装 UV 包管理器**

MacOS/Linux:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:

```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. **初始化项目与依赖**

```sh
# 创建项目目录
uv init mcp-server
cd mcp-server

# 创建并激活虚拟环境
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
uv add "mcp[cli]" httpx

# 创建服务器实现文件
touch main.py
```

---

## 子模块简介

### 1. mcp-server-client

- **功能**：基于 MCP 协议，结合 LangChain、OpenAI、SSE 等技术，提供智能文档检索和工具调用的 Agent 服务与客户端。
- **协议支持**：Stdio、SSE/HTTP。
- **主要用途**：AI 助手、文档搜索、智能问答等。
- **启动示例**：
  - Stdio 协议：`python main.py`
  - SSE/HTTP 协议：`uvicorn service:app --host 0.0.0.0 --port 8000`
- 详见 [mcp-server-client/README.md](./mcp-server-client/README.md)

### 2. txt_counter

- **功能**：基于 Python 3.12 和 MCP 框架的桌面 TXT 文件统计工具。
- **主要用途**：统计当前用户桌面 `.txt` 文件数量并列出文件名，支持 MCP 工具注册和自动化集成。
- **启动示例**：
  - 直接运行：`python main.py`
  - 作为 MCP 工具服务：`python txt_counter.py` 或 `mcp dev txt_counter.py`
- 详见 [txt_counter/README.md](./txt_counter/README.md)

### 3. mcp_test

- **功能**：基于 FastMCP 框架的质数判断服务，提供 `prime://{n}` 资源接口。
- **主要用途**：通过 MCP 客户端或 API 判断任意数字是否为质数。
- **启动示例**：`python main.py`
- 详见 [mcp_test/README.md](./mcp_test/README.md)

---

## 三个子模块总结

### 1. mcp-server-client
- **定位**：智能 Agent 服务与客户端
- **功能**：基于 MCP 协议，结合 LangChain、OpenAI、SSE 等技术，提供文档智能检索、工具自动调用等能力。
- **特点**：支持本地/远程协议，内置多种 AI 框架文档检索，适用多场景。

### 2. txt_counter
- **定位**：TXT 文件统计工具
- **功能**：统计桌面 .txt 文件数量并列出文件名
- **特点**：基于 MCP 框架，支持自动化集成，结构清晰易扩展。

### 3. mcp_test
- **定位**：质数判断服务
- **功能**：判断数字是否为质数，提供 prime://{n} 资源接口
- **特点**：基于 FastMCP，算法高效，适合基础数学服务集成。

---

## 快速开始

1. 进入对应子模块目录，参考各自 README 进行依赖安装和服务启动。
2. 推荐使用 Python 3.10+，并使用虚拟环境隔离依赖。
3. 各子模块均支持 MCP 协议，可集成到支持 MCP 的平台或工具中。

---

## 参考文档

- [python-mcp-server-client](https://github.com/GobinFan/python-mcp-server-client)
- [LangChain 官方文档](https://python.langchain.com/docs/)
- [MCP 协议](https://modelcontextprotocol.io/)
- [Serper API](https://serper.dev/)
- [OpenAI 官方文档](https://platform.openai.com/docs/)
- [MCP 框架文档](https://github.com/microsoft/mcp)

---

如需详细功能、用法和配置说明，请分别查阅各子模块下的 README 文件。

