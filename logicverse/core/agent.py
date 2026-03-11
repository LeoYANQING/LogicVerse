from logicverse.tools.registry import registry
from logicverse.utils.parser import JsonParser
from logicverse.memory.buffer import MemoryBuffer
from logicverse.planners.react import build_react_prompt
from logicverse.planners.direct import build_direct_prompt
from logicverse.planners.plan import build_plan_prompt

class LogicVerseAgent:
    def __init__(self, llm, max_steps=10):
        self.llm = llm
        self.max_steps = max_steps

    def _route_task(self, query: str) -> str:
        """元认知：让 LLM 自己决定用什么范式处理任务"""
        router_prompt = f"""你是一个底层的任务路由分类器。
请分析以下用户输入，并从 [direct, react, plan] 中选择最合适的一个：
- direct: 简单的日常对话、打招呼、常识问答，不需要使用任何工具。
- react: 需要调用外部工具（如计算器、查询数据、搜索）才能解决的具体任务。
- plan: 宏大的、模糊的复杂工程任务（如写系统、写长篇论文），需要先拆解步骤。

用户输入: {query}
请注意：只允许输出这三个英文单词中的一个，不要包含任何其他字符！"""
        
        # 使用低温度调用模型进行分类
        decision = self.llm.chat(router_prompt).strip().lower()
        
        # 鲁棒性兜底逻辑
        if "direct" in decision: return "direct"
        if "plan" in decision: return "plan"
        return "react" # 默认回退到最全能的 ReAct 范式

    def run(self, query: str):
        print(f"🚀 LogicVerse 接收任务: {query}")
        
        # 阶段一：动态路由评估
        print("🧭 [Meta-Agent] 正在评估任务复杂度...")
        paradigm = self._route_task(query)
        print(f"🎯 决断完毕：将使用 [{paradigm.upper()}] 范式执行该任务。\n")
        print("-" * 40)

        # 阶段二：范式分发
        if paradigm == "direct":
            return self._run_direct(query)
        elif paradigm == "plan":
            return self._run_plan(query)
        else:
            return self._run_react(query)

    # ================= 各范式的具体执行逻辑 =================

    def _run_direct(self, query: str):
        """处理简单任务，直接对话，极其省钱省时"""
        prompt = build_direct_prompt(query)
        response = self.llm.chat(prompt)
        print(f"🤖 [Direct]: {response}")
        print("-" * 40 + "\n✅ 任务完成")
        return response

    def _run_plan(self, query: str):
        """处理宏大任务，仅作拆解，不陷入死循环"""
        prompt = build_plan_prompt(query)
        response = self.llm.chat(prompt)
        print(f"🗺️ [Plan 任务拆解]:\n{response}")
        print("-" * 40 + "\n✅ 计划制定完成")
        return response

    def _run_react(self, query: str):
        """处理需要使用工具的复杂任务 (原有的经典逻辑)"""
        memory = MemoryBuffer()
        memory.add_user_query(query)

        for step in range(self.max_steps):
            history_str = memory.get_formatted_history()
            prompt = build_react_prompt(query, registry.get_tool_prompts(), history_str)
            raw_res = self.llm.chat(prompt)

            try:
                res = JsonParser.parse(raw_res)
                thought = res.get("thought", "Thinking...")
                action = res.get("action")
                action_input = res.get("action_input", {})

                print(f"[{step+1}] 🧠 思考: {thought}")
                print(f"[{step+1}] 🛠️ 行动: {action} | 参数: {action_input}")
                memory.add_ai_thought_and_action(thought, action, action_input)

                if action == "finish":
                    answer = action_input.get('answer', '任务完成')
                    print(f"\n✅ 最终结果: {answer}")
                    return answer

                if action in registry.tools:
                    obs = registry.tools[action]["func"](**action_input)
                else:
                    obs = f"错误：未找到工具 '{action}'"

                print(f"[{step+1}] 👀 观察: {obs}\n")
                memory.add_observation(str(obs))

            except Exception as e:
                error_msg = f"格式错误，请严格输出 JSON。详情: {e}"
                print(f"⚠️ 自愈触发: {error_msg}")
                memory.add_system_error(error_msg)

        print("❌ 达到最大思考步数。")
        return None