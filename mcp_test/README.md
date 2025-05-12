# Prime Number Checker

本项目是一个用于判断给定数字是否为质数的服务。

## 设计说明

- 使用 `FastMCP` 框架实现。
- 提供一个资源接口 `prime://{n}`，用于判断 n 是否为质数。
- 质数判断逻辑：
  - 小于 2 的数不是质数。
  - 从 2 到 sqrt(n) 之间，若存在能整除 n 的数，则 n 不是质数。
  - 否则 n 是质数。

## 使用方法

1. 启动服务：
   ```bash
   python main.py
   ```

2. 通过资源接口调用判断质数：
   - 例如判断 50 是否为质数：
    
     ```python
     is_prime(50)  # 返回 False
     ```

3. 你也可以通过 MCP 客户端或其他方式访问 `prime://{n}` 资源。
   
4. 在 cursor 配置
  
  ```json
  {
  "mcpServers": {
      "prime-number-checker": {
        "type": "stdio",
        "command": "uv",
        "args": [
          "--directory",
          "/home/hellotalk/code/ai/mcp-demo/mcp_test",
          "run",
          "main.py"
        ]
      }
    }
  }
  ```


## 示例

```python
from main import is_prime
print(is_prime(7))   # 输出 True
print(is_prime(50))  # 输出 False
```


在 cursor 调用

```txt
使用 prime-number-checker   50
```