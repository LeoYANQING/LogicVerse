import os
import sys
from logicverse.utils.config import LLMConfig
from logicverse.llms.factory import LLMFactory
from logicverse.core.agent import LogicVerseAgent
from logicverse.tools.registry import registry
from logicverse.skills.loader import SkillLoader  # 🌟 引入核心的 DLC 装配引擎

# ==========================================
# 🛠️ 传统方式：定义基础的通用魔法工具
# ==========================================

@registry.tool
def get_weather(city: str) -> str:
    """获取指定城市的天气情况。参数 city 是城市中文名。"""
    weather_db = {
        "北京": "晴朗，气温 25°C，适合出行",
        "上海": "小雨，气温 18°C，建议带伞",
        "深圳": "多云，气温 28°C，有些闷热"
    }
    return weather_db.get(city, f"抱歉，暂时无法获取 {city} 的天气数据。")

@registry.tool
def calculate_math(expression: str) -> str:
    """执行复杂的数学计算。参数 expression 必须是合法的 Python 数学表达式，如 '1024 * 3.14'。"""
    try:
        result = eval(expression)
        return f"计算成功，结果为: {result}"
    except Exception as e:
        return f"数学表达式错误: {e}"


# ==========================================
# 🚀 主程序：双轨制全链路演示
# ==========================================

def main():
    print("🌟 === 启动 LogicVerse 智能生态系统 === \n")

    # 1. 挂载动力引擎 (读取 .env 配置)
    print("⚙️ 正在装配底层大模型引擎...")
    config = LLMConfig().load_env()
    
    if not config.get_value("API_KEY"):
        print("❌ 致命错误: 未在 .env 文件中检测到 LLM_API_KEY！")
        sys.exit(1)

    try:
        llm = LLMFactory.create(config)
    except Exception as e:
        print(f"❌ 引擎装配失败: {e}")
        sys.exit(1)


    # ==========================================
    # 🧪 演示 1：传统方式 (手动挂载工具)
    # ==========================================
    print("\n" + "="*50)
    print(" 🧪 演示 1：传统方式 (手动配置单体 Agent)")
    print("="*50)
    
    agent_classic = LogicVerseAgent(
        name="生活管家_Alpha",
        role="你是一位贴心且严谨的生活管家。遇到天气或计算问题，请务必使用工具。一旦拿到所有需要的数据，请立即给出友好的最终回复，并调用 finish 结束任务。",
        llm=llm,
        tools=["get_weather", "calculate_math"], 
        max_steps=5 
    )

    query_classic = "我明天要去北京出差，请帮我查一下天气。另外，帮我算一下 128 的 3 次方是多少？"
    print(f"\n🗣️ 用户指令: {query_classic}")
    try:
        final_answer = agent_classic.run(query_classic)
        print(f"\n🎉 最终回复:\n{final_answer}")
    except Exception as e:
        print(f"\n❌ 执行异常: {e}")


    # ==========================================
    # 🧩 演示 2：DLC 式装配 (全自动加载外部技能包)
    # ==========================================
    print("\n\n" + "="*50)
    print(" 🧩 演示 2：面向未来的 DLC 技能装配 (Multi-Agent 生态)")
    print("="*50)

    test_skill_dir = "./skills/academic_researcher"
    print(f"👉 尝试全自动挂载外部技能包: {test_skill_dir}")

    if not os.path.exists(test_skill_dir):
        print(f"   ⚠️ 未检测到技能包目录 {test_skill_dir}，跳过演示。")
        print("   💡 请参照 README 在根目录建立该文件夹即可体验魔法。")
    else:
        try:
            # 🌟 核心高光：只要一个文件夹路径，直接解析出 Prompt 和 专属工具！
            skill_package = SkillLoader.load(test_skill_dir)
            
            # 瞬间造出全副武装的专业研究员 Agent
            agent_expert = LogicVerseAgent(
                name="学术专家_DLC",
                role=skill_package["role"],   # 自动提取自 SKILL.md
                llm=llm,
                tools=skill_package["tools"], # 自动捕获自 scripts/
                max_steps=5
            )

            query_skill = "请帮我检索一下关于 deep learning的最新论文，并告诉我核心思想。"
            print(f"\n🗣️ 用户指令: {query_skill}")
            final_answer2 = agent_expert.run(query_skill)
            
            print(f"\n🎉 最终回复:\n{final_answer2}")
            
        except Exception as e:
            print(f"❌ 技能包装配或执行失败: {e}")

    print("\n🌟 === 所有演示流程结束 === 🌟")

if __name__ == "__main__":
    main()