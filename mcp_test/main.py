# 导入FastMCP类用于创建MCP服务器
from mcp.server.fastmcp import FastMCP

# 创建一个名为"Prime Number Checker"的FastMCP服务器实例
server = FastMCP("Prime Number Checker")

# 定义一个资源路由,用于检查数字是否为质数
@server.resource("prime://{n}")
def is_prime(n: int):
    # 如果数字小于2,则不是质数
    if n < 2:
        return False
    # 从2到sqrt(n)检查是否有因子
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    # 如果没有因子,则是质数
    return True

# 主函数,启动服务器
def main():
    # 使用stdio传输方式运行服务器
    server.run(transport="stdio")

# 程序入口点
if __name__ == "__main__":
    print("Starting server")
    main()
