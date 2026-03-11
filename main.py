from logicverse.llms.factory import LLMFactory

def main():
    # 1. 工厂模式：根据 .env 自动生产大脑
    # 不管你是用 DeepSeek 还是本地 Ollama，只要 LLM_PROVIDER=openai，这一行代码全搞定
    try:
        llm = LLMFactory.create()
    except Exception as e:
        print(e)
        return

    # 2. 交付给 Agent 使用
    # agent = LogicVerseAgent(llm=llm)
    # agent.run("你的任务...")
    
    # 测试一下
    print(f"✅ 引擎装配成功！当前模型: {llm.model}")
    print(llm.chat("你好，请确认你的身份。"))

if __name__ == "__main__":
    main()