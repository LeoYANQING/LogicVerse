from logicverse.tools.registry import registry
from logicverse.utils.parser import JsonParser
from logicverse.memory.buffer import MemoryBuffer
from logicverse.planners.react import build_react_prompt

class LogicVerseAgent:
    def __init__(self, llm, max_steps=10):
        self.llm = llm
        self.max_steps = max_steps

    def run(self, query: str):
        print(f"🚀 LogicVerse v0.0.1 启动 | 任务: {query}\n")
        
        # 1. 初始化记忆模块
        memory = MemoryBuffer()
        memory.add_user_query(query)

        # 2. 开启思考循环
        for step in range(self.max_steps):
            # 获取当前上下文，并组装 ReAct Prompt
            history_str = memory.get_formatted_history()
            prompt = build_react_prompt(query, registry.get_tool_prompts(), history_str)
            
            # 请求大模型
            raw_res = self.llm.chat(prompt)

            try:
                # 解析输出
                res = JsonParser.parse(raw_res)
                thought = res.get("thought", "Thinking...")
                action = res.get("action")
                action_input = res.get("action_input", {})

                print(f"[{step+1}] 🧠 思考: {thought}")
                print(f"[{step+1}] 🛠️ 行动: {action} | 参数: {action_input}")

                # 记录动作到记忆
                memory.add_ai_thought_and_action(thought, action, action_input)

                # 终止条件
                if action == "finish":
                    answer = action_input.get('answer', '任务完成')
                    print(f"\n✅ 最终结果: {answer}")
                    return answer

                # 执行工具
                if action in registry.tools:
                    obs = registry.tools[action]["func"](**action_input)
                else:
                    obs = f"错误：未找到工具 '{action}'"

                print(f"[{step+1}] 👀 观察: {obs}\n")
                memory.add_observation(str(obs))

            except Exception as e:
                # 自愈闭环：解析失败，记录报错并进入下一次循环纠错
                error_msg = f"格式错误，请严格输出 JSON。详情: {e}"
                print(f"⚠️ 触发自愈机制: {error_msg}")
                memory.add_system_error(error_msg)

        print("❌ 达到最大思考步数，任务被迫终止。")
        return None