from logicverse.llms.factory import LLMFactory
# 如果你想测试完整的 Agent，可以把下面的注释打开
# from logicverse import LogicVerseAgent, registry

def main():
    print("🚀 === LogicVerse 引擎双模式装配测试 ===\n")

    # ==========================================
    # 模式一：全自动装配 (推荐日常开发使用)
    # 核心优势：代码里没有任何敏感信息，完全通过 .env 驱动
    # ==========================================
    print("👉 [测试一] 读取 .env 自动装配")
    try:
        # 零参数，全靠工厂和配置中心的默契配合
        llm_auto = LLMFactory.create()
        print(f"✅ 自动装配成功！当前模型: {llm_auto.model}")
        
        # 真正的网络请求测试
        print(f"🤖 模型回复:\n{llm_auto.chat('你好，请用一句话介绍你的身份。')}\n")
    except Exception as e:
        print(f"❌ 自动装配失败: {e}\n")


    # ==========================================
    # 模式二：代码传参强制装配 (适合多模型对比 / 动态租户切换)
    # 核心优势：无视 .env 的默认值，利用高优先级参数强行覆盖
    # ==========================================
    print("👉 [测试二] 代码手动传参装配 (覆盖 .env)")
    try:
        # 假设你在做“模型竞技场”，临时拉起一个 Qwen 阿里云百炼接口
        llm_manual = LLMFactory.create(
            provider="openai",  # 依然走 OpenAI 兼容协议
            model="qwen-turbo", # 强行指定模型名
            api_key="sk-dummy-key-for-test-123", # 强行传入别的 Key
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1" # 强行覆盖 URL
        )
        print(f"✅ 参数装配成功！当前模型: {llm_manual.model}")
        
        # 验证容错能力：因为我们故意填了假 Key，这里必定会触发我们在 openai_llm.py 里写的 except 兜底机制！
        print(f"🤖 容错机制测试 (预期返回 JSON 报错格式):\n{llm_manual.chat('你好')}\n")
    except Exception as e:
        print(f"❌ 参数装配失败: {e}\n")


    # ==========================================
    # 进阶玩法：交付给真正的 Agent 大脑
    # ==========================================
    # agent = LogicVerseAgent(llm=llm_auto)
    # agent.run("请告诉我你是谁，并且证明你能思考。")

if __name__ == "__main__":
    main()