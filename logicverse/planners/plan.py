def build_plan_prompt(query: str) -> str:
    """Plan 范式：适用于宏大工程，强制模型先输出拆解步骤"""
    return f"""你是一个顶级的架构师和项目经理。用户提出了一个复杂的宏大任务。
请不要直接执行，而是将其拆解为逻辑清晰、可执行的子任务列表（Step 1, Step 2...）。

复杂任务：{query}"""