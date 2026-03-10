def build_react_prompt(query: str, tool_descriptions: str, history: str) -> str:
    """构建 ReAct (Reason + Act) 模式的系统提示词"""
    return f"""你是一个解决问题的智能专家。你可以使用以下工具：
{tool_descriptions}
- finish: 如果你已经得出最终答案，请调用此工具，参数为 {{"answer": "你的最终回复"}}

你必须且只能输出严格的 JSON 格式：
{{
    "thought": "你的思考过程",
    "action": "要调用的工具名称",
    "action_input": {{"参数名": "参数值"}}
}}

当前任务：{query}

【执行记录】
{history}"""