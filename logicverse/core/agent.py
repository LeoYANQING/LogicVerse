from logicverse.memory.buffer import MemoryBuffer
from logicverse.tools.registry import registry
from logicverse.utils.parser import JsonParser
# 假设你在 planners/react.py 中实现了 build_react_prompt
from logicverse.planners.react import build_react_prompt

class LogicVerseAgent:
    """高度可拓展的智能体核心类 (支持 Multi-Agent)"""
    
    def __init__(self, name: str, role: str, llm, tools: list = None, memory=None, max_steps: int = 10):
        self.name = name        # Agent 的名字 (如: "文献检索员")
        self.role = role        # Agent 的系统人设 (System Prompt)
        self.llm = llm          # Agent 的大脑 (注入的 OpenAILLM 实例)
        self.tools = tools or [] # Agent 的专属工具权限列表 (如: ["search_papers"])
        self.memory = memory or MemoryBuffer()
        self.max_steps = max_steps

    def _get_allowed_tools(self) -> dict:
        """只暴露该 Agent 被授权的工具，防止越权调用"""
        if not self.tools:
            return {} # 没有分配工具
        return {name: registry.tools[name] for name in self.tools if name in registry.tools}

    def run(self, query: str, context: str = "") -> str:
        """
        执行循环。
        参数 context 非常重要，它是 Multi-Agent 之间传递上下文的桥梁！
        """
        print(f"\n[{self.name}] 🎬 开始执行任务...")
        self.memory.add_user_message(f"{context}\n用户指令: {query}" if context else query)

        allowed_tools = self._get_allowed_tools()
        
        # --- 这里简化了 ReAct 循环以展示架构逻辑 ---
        for step in range(self.max_steps):
            history_str = self.memory.get_formatted_history()
            
            # 组装超级 Prompt: 包含人设、工具描述、历史记录、当前任务
            prompt = build_react_prompt(self.role, allowed_tools, history_str)
            raw_res = self.llm.chat(prompt)

            try:
                res = JsonParser.parse(raw_res)
                action = res.get("action")
                action_input = res.get("action_input", {})
                thought = res.get("thought", "思考中...")

                print(f"[{self.name} | Step {step+1}] 🧠 {thought}")

                if action == "finish":
                    answer = action_input.get("answer", "")
                    print(f"[{self.name}] ✅ 任务完成。")
                    self.memory.add_ai_message(answer)
                    return answer

                # 工具权限校验与调用
                if action in allowed_tools:
                    print(f"[{self.name}] 🛠️ 调用工具: {action}({action_input})")
                    obs = allowed_tools[action]["func"](**action_input)
                    print(f"[{self.name}] 👀 观察结果: {str(obs)[:100]}...")
                    self.memory.add_tool_observation(action, str(obs))
                else:
                    self.memory.add_tool_observation(action, f"错误：未授权或不存在的工具 '{action}'")

            except Exception as e:
                self.memory.add_tool_observation("system", f"格式化错误，必须返回严谨的 JSON。错误: {e}")

        return "❌ 达到最大思考步数，未能完成任务。"