class MemoryBuffer:
    """
    Agent 的独立记忆中枢 (支持 Multi-Agent)
    每个 Agent 实例都拥有自己独立的海马体，互不干扰。
    """
    def __init__(self, max_turns: int = 10):
        self.history = []
        self.max_turns = max_turns

    def add_user_message(self, content: str):
        """记录用户的指令或上游 Agent 传来的上下文"""
        self.history.append({"role": "user", "content": content})

    def add_ai_message(self, content: str):
        """记录 Agent 自己最终得出的结论"""
        self.history.append({"role": "assistant", "content": content})

    def add_tool_observation(self, tool_name: str, result: str):
        """记录工具调用的中间结果 (系统级观察)"""
        self.history.append({"role": "system", "content": f"[Tool: {tool_name}] 观察结果: {result}"})

    def get_formatted_history(self) -> str:
        """
        将历史记录格式化为纯文本，喂给大模型的上下文。
        为了防止爆 Token，默认只保留最近的 max_turns * 2 条记录。
        """
        recent_history = self.history[-self.max_turns * 2:] 
        if not recent_history:
            return "当前暂无历史记忆。"
        
        # 将列表拼接成大模型容易理解的对话流
        formatted_lines = []
        for msg in recent_history:
            role_tag = msg['role'].upper()
            formatted_lines.append(f"{role_tag}: {msg['content']}")
            
        return "\n".join(formatted_lines)

    def clear(self):
        """清空记忆，方便 Agent 重置状态"""
        self.history.clear()