def build_direct_prompt(query: str) -> str:
    """Direct 范式：适用于简单寒暄和常识问答，无需 JSON 格式，不调用工具"""
    return f"""你是一个聪明、简洁的 AI 助手。请直接、自然地回答用户的以下问题，不需要调用任何工具：

用户问题：{query}"""