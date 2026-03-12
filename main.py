from logicverse.utils.config import LLMConfig
from logicverse.llms.factory import LLMFactory
from logicverse import LogicVerseAgent, registry

# 1. 注册工具池 (所有工具都在这，但我们会按需分配给不同的 Agent)
@registry.tool
def search_arxiv(query: str) -> str:
    """搜索最新的学术论文"""
    return f"检索到关于 '{query}' 的论文：基于多目标跟踪 (MOT) 与 LogicVerse 框架的新范式。"

@registry.tool
def write_python_code(requirements: str) -> str:
    """根据需求编写 Python 框架代码"""
    return f"def mot_tracker():\n    # 实现 {requirements}\n    pass"

def main():
    print("🚀 === LogicVerse Multi-Agent 协同网络 ===\n")
    
    # 共用同一个配置，或者你可以给 Coder 分配一个更强的模型配置
    config = LLMConfig().load_env()
    base_llm = LLMFactory.create(config)

    # ==========================================
    # 🕵️‍♂️ 智能体 A：首席学术研究员
    # 它的权限：只能使用搜索工具，不能写代码
    # ==========================================
    researcher = LogicVerseAgent(
        name="Researcher_Z",
        role="你是一位顶尖的 AI 学术研究员，擅长检索文献并提炼核心算法思想。你需要给出清晰的方法论摘要。",
        llm=base_llm,
        tools=["search_arxiv"] # 专属工具
    )

    # ==========================================
    # 👨‍💻 智能体 B：高级算法工程师
    # 它的权限：只能写代码，不需要去搜索
    # ==========================================
    coder = LogicVerseAgent(
        name="Coder_W",
        role="你是一位资深的算法工程师。你的任务是接收研究员的理论方案，并将其转化为结构清晰的 Python 代码框架。",
        llm=base_llm,
        tools=["write_python_code"] # 专属工具
    )

    # ==========================================
    # 🤝 工作流串联 (The Multi-Agent Workflow)
    # ==========================================
    user_goal = "去调查一下最新的 MOT (多目标跟踪) 算法，然后给我写一个基础的代码实现框架。"
    print(f"🎯 最终用户目标: {user_goal}\n")
    print("-" * 50)

    # 阶段一：研究员工作
    research_report = researcher.run("调查最新的 MOT 算法核心思想。")
    print(f"\n📄 研究报告产出:\n{research_report}\n")
    print("-" * 50)

    # 阶段二：工程师接手 (将前一个 Agent 的输出作为 Context 传给下一个)
    code_result = coder.run(
        query="根据研究员的报告，写出基础的代码框架。",
        context=f"【前置研究报告】:\n{research_report}"
    )
    
    print("\n🎉 Multi-Agent 协作完成！最终代码产出:\n" + code_result)

if __name__ == "__main__":
    main()