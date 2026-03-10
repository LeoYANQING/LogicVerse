import os
from logicverse import LogicVerseAgent, registry
from logicverse import MockLLM, OpenAILLM, load_env

# 1. 自动读取 .env 文件中的环境变量
load_env()

# 2. 定义业务工具
@registry.tool
def calculate(expression: str) -> str:
    """计算数学表达式的结果"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {e}"

@registry.tool
def demo_tool(query: str) -> str:
    """一个模拟的外部数据查询工具"""
    return f"接收到查询: {query}。数据一切正常！"

def main():
    # --- 模式 A：断网跑通测试 (默认开启) ---
    llm = MockLLM()

    # --- 模式 B：接入真实大模型 (配置好 .env 后取消下方注释) ---
    # api_key = os.getenv("DEEPSEEK_API_KEY")
    # if api_key:
    #     llm = OpenAILLM(
    #         api_key=api_key, 
    #         base_url="https://api.deepseek.com/v1", 
    #         model="deepseek-chat"
    #     )
    
    # 3. 运行框架
    agent = LogicVerseAgent(llm=llm)
    agent.run("测试一下工具调用机制是否顺畅")

if __name__ == "__main__":
    main()