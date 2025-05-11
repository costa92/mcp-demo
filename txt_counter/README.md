# txt_counter

> 基于 Python 3.12 和 MCP 框架的桌面 TXT 文件统计工具

---

## 项目简介

**txt_counter** 是一个用于统计和列举当前用户桌面上 `.txt` 文件数量和文件名的命令行工具。项目采用现代 Python 3.12 语法，结合 [MCP 框架](https://github.com/microsoft/mcp) 实现 API 工具注册，支持类型注解和自动化工具发现，便于扩展和集成。

---

## 功能特性

- 统计当前用户桌面上的 `.txt` 文件数量
- 列出所有 `.txt` 文件的文件名
- 采用 MCP 框架注册工具，便于集成到更大的自动化或智能平台
- 代码结构清晰，易于扩展

---

## 目录结构

```bash
.
├── main.py            # 入口脚本，演示调用
├── txt_counter.py     # 核心功能与 MCP 工具注册
├── pyproject.toml     # Python 项目配置与依赖
├── uv.lock            # 依赖锁定文件（uv/PEP 582）
├── .venv/             # 推荐的虚拟环境目录
├── .gitignore         # Git 忽略配置
├── .python-version    # Python 版本锁定（3.12）
├── .nvmrc             # Node.js 版本（如需前端集成）
└── README.md          # 项目说明文档
```

---

## 安装与运行

### 1. 环境准备

- 推荐使用 Python 3.12 及以上版本
- 建议使用虚拟环境（如 `.venv`）隔离依赖

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 2. 安装依赖

本项目采用 [uv](https://github.com/astral-sh/uv) 或 `pip` 管理依赖：

```bash
uv pip install -r pyproject.toml
# 或
pip install -r pyproject.toml
```

### 3. 运行

- 直接运行主程序：

```bash
python main.py
```

- 或运行 MCP 工具服务（推荐）：

```bash
python txt_counter.py
```

使用 mcp 运行

```bash
mcp dev txt_counter.py
```

配置 Cursor mcp

```json
{
  "mcpServers": {
    "txt-mcp": {
      "command": "python3",
      "args": [
        "/Users/你的用户名/txt_counter/txt_counter.py"
      ],
    }
  }
}
```
---

## 主要依赖

- [Python 3.12+](https://docs.python.org/3/)
- [mcp](https://github.com/microsoft/mcp) >= 1.6.0
- httpx >= 0.28.1

详见 `pyproject.toml`。

---

## 最佳实践与开发建议

- 使用类型注解（PEP 484），提升代码可读性和可维护性
- 遵循现代 Python 项目结构，配置 `pyproject.toml` 管理依赖
- 推荐使用虚拟环境和 `.python-version` 保证开发一致性
- 代码风格建议遵循 [PEP 8](https://peps.python.org/pep-0008/)
- 工具注册与 API 集成建议参考 MCP 官方文档

---

## 参考文档

- [Python 官方文档](https://docs.python.org/3/)
- [MCP 框架文档](https://github.com/microsoft/mcp)
- [uv (PEP 582) 依赖管理](https://github.com/astral-sh/uv)

---

## License

MIT
