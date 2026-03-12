import json

def build_react_prompt(role: str, allowed_tools: dict, history_str: str) -> str:
    """
    LogicVerse ReAct 范式提示词构建器
    负责将人设、工具说明和历史记忆融合成严苛的系统指令。
    """
    
    # 1. 动态生成工具说明书
    tools_desc = ""
    if allowed_tools:
        tools_desc = "\n【你可以使用的工具】:\n"
        for name, tool in allowed_tools.items():
            # 这里假设你在 @registry.tool 装饰器里把函数的 __doc__ 存进了 doc 字段
            tools_desc += f"- {name}: {tool.get('doc', '无工具说明')}\n"
    else:
        tools_desc = "\n【注意】: 你当前没有任何外部工具可以使用。如果认为任务已完成，请直接输出 finish 动作。\n"

    # 2. 极其严厉的格式紧箍咒 (这是 ReAct 不崩溃的核心)
    format_instructions = """
【强制输出规范】(极其重要！！！)
你必须且只能输出一个合法的 JSON 对象，绝对不能包含任何多余的解释性文本，也不能包含 Markdown 代码块标记（如 ```json）。
你的输出必须严格符合以下 JSON 结构：
{
    "thought": "你的思考过程。请详细说明你当前的目标是什么，为什么要采取下一步行动。",
    "action": "你要调用的工具名称（必须从【你可以使用的工具】列表中选择。如果任务已经完成，或者不需要工具，请填写 'finish'）",
    "action_input": {"参数名": "参数值"} // 这是传给工具的参数字典。如果 action 是 finish，这里请放入 {"answer": "最终给用户的详细回复内容"}
}
"""

    # 3. 组装终极 Prompt
    prompt = f"""【系统人设与任务目标】:
{role}
{tools_desc}
{format_instructions}
=========================================
【当前上下文与历史记忆】:
{history_str}
=========================================

请基于上述规则和当前对话上下文，直接输出你下一步行动的纯 JSON 文本：
"""
    return prompt