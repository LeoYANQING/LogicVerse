class MemoryBuffer:
    """管理 Agent 的运行上下文和历史记录"""
    def __init__(self):
        self.history = []

    def add_user_query(self, query: str):
        self.history.append(f"User Query: {query}")

    def add_ai_thought_and_action(self, thought: str, action: str, action_input: dict):
        self.history.append(f"AI Thought: {thought}\nAI Action: {action}({action_input})")

    def add_observation(self, observation: str):
        self.history.append(f"Observation: {observation}")

    def add_system_error(self, error_msg: str):
        self.history.append(f"System Error: {error_msg}")

    def get_formatted_history(self) -> str:
        return "\n".join(self.history)