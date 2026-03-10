import inspect
from typing import Callable, Dict

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict] = {}

    def tool(self, func: Callable):
        """装饰器：将 Python 函数转化为 Agent 工具"""
        name = func.__name__
        sig = inspect.signature(func)
        params = {k: (v.annotation.__name__ if v.annotation != inspect._empty else "Any") 
                  for k, v in sig.parameters.items()}
        
        self.tools[name] = {
            "func": func,
            "description": (func.__doc__ or "无描述").strip(),
            "parameters": params
        }
        return func

    def get_tool_prompts(self) -> str:
        """生成供大模型阅读的工具说明书"""
        return "\n".join([f"- {n}: {i['description']} | 参数: {i['parameters']}" for n, i in self.tools.items()])

# 全局单例工具箱
registry = ToolRegistry()