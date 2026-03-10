import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable

# ==========================================
# 模块 1: 工具基类 (Tools) - 方便无限拓展新能力
# ==========================================
class Tool:
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func

    def execute(self, **kwargs) -> str:
        try:
            # 运行真实函数，并将结果转为字符串
            result = self.func(**kwargs)
            return str(result)
        except Exception as e:
            return f"工具执行出错: {str(e)}"

# 定义几个演示工具
def weather_api(city: str) -> str:
    mock_data = {"北京": "晴天, 25°C", "上海": "下雨, 18°C", "纽约": "多云, 20°C"}
    return mock_data.get(city, f"找不到 {city} 的天气数据")

def calculator_api(expression: str) -> str:
    return str(eval(expression)) # 注意：生产环境绝对不要直接用 eval，这里仅作演示

# ==========================================
# 模块 2: 模型接口 (LLM Provider) - 方便随时切换大模型
# ==========================================
class BaseLLM(ABC):
    @abstractmethod
    def chat(self, prompt: str) -> str:
        pass

# 这里我们写一个 Dummy 模拟类，方便你现在不配 API Key 也能跑通代码
# 未来你可以照猫画虎写一个 OpenAILLM 或 DeepSeekLLM
class DummyLLM(BaseLLM):
    def chat(self, prompt: str) -> str:
        # 1. 先检查 prompt (包含了之前的历史记忆) 里有没有工具返回的结果
        if "晴天, 25°C" in prompt:
            # 如果看到了观察结果，说明天气查完了，该结束了
            return '{"thought": "我已经获取到了北京的天气结果，可以回答用户了", "action": "finish", "action_input": {"answer": "北京今天晴天，气温25°C。"}}'
        
        # 2. 如果没看到结果，说明是第一次进循环，去查天气
        elif "北京" in prompt:
            return '{"thought": "用户想查北京天气，我需要调用天气工具", "action": "weather_api", "action_input": {"city": "北京"}}'
        
        # 3. 兜底
        else:
            return '{"thought": "我不懂这个问题", "action": "finish", "action_input": {"answer": "抱歉，我无法回答。"}}'
# ==========================================
# 模块 3: 核心调度器 (Agent Engine) - 框架的大脑
# ==========================================
class BaseAgent:
    def __init__(self, llm: BaseLLM, tools: List[Tool]):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.max_steps = 5 # 防止死循环

    def _build_system_prompt(self) -> str:
        """构建系统提示词，强制要求 JSON 输出"""
        tool_descs = [f"- {t.name}: {t.description}" for t in self.tools.values()]
        tool_list_str = "\n".join(tool_descs)
        
        return f"""
你是一个智能助手，你可以使用以下工具：
{tool_list_str}
- finish: 如果你已经得出最终答案，请使用此工具。

你必须并且只能输出一个合法的 JSON 对象，格式如下：
{{
    "thought": "你当前的思考过程",
    "action": "要调用的工具名称（必须是上述工具之一，或者 finish）",
    "action_input": {{ "参数名": "参数值" }} 
}}
"""

    def run(self, user_input: str) -> str:
        print(f"🚀 开始执行任务: {user_input}\n")
        
        # 历史记录（记忆）
        memory = [f"用户输入: {user_input}"]
        
        for step in range(self.max_steps):
            print(f"--- Step {step + 1} ---")
            
            # 1. 组装当前的完整 Prompt
            current_context = "\n".join(memory)
            full_prompt = self._build_system_prompt() + "\n\n当前执行记录:\n" + current_context
            
            # 2. 调用大模型
            llm_response_text = self.llm.chat(full_prompt)
            print(f"[LLM 原始输出] {llm_response_text}")
            
            # 3. 解析 JSON (自带基础纠错防崩溃)
            try:
                # 生产环境中，这里可以用正则表达式把 ```json ``` 标签去掉再解析
                parsed_response = json.loads(llm_response_text)
                thought = parsed_response.get("thought", "")
                action = parsed_response.get("action", "")
                action_input = parsed_response.get("action_input", {})
            except json.JSONDecodeError:
                error_msg = "系统提示: 你的输出不是合法的 JSON，请修正后重新输出。"
                print(f"❌ 解析失败，尝试纠错: {error_msg}")
                memory.append(error_msg)
                continue # 进入下一轮循环，让大模型自己纠正
            
            print(f"🧠 思考: {thought}")
            print(f"🛠️  行动: {action} 参数: {action_input}")
            
            # 4. 判断是否完成
            if action == "finish":
                final_answer = action_input.get("answer", "任务完成")
                print(f"\n✅ 最终答案: {final_answer}")
                return final_answer
                
            # 5. 执行工具
            if action in self.tools:
                tool_instance = self.tools[action]
                observation = tool_instance.execute(**action_input)
                print(f"👀 观察结果: {observation}")
            else:
                observation = f"错误: 找不到名为 '{action}' 的工具。"
                print(observation)
                
            # 6. 将结果存入记忆，进入下一步
            memory.append(f"LLM 输出: {llm_response_text}")
            memory.append(f"工具返回结果 (Observation): {observation}")
            print() # 空行美化输出
            
        print("\n⚠️ 达到最大步数限制，任务终止。")
        return "未能完成任务"

# ==========================================
# 测试运行
# ==========================================
if __name__ == "__main__":
    # 1. 准备工具箱
    my_tools = [
        Tool("weather_api", "查询城市天气。参数需包含 'city'，如 {'city': '北京'}", weather_api),
        Tool("calculator_api", "计算数学公式。参数需包含 'expression'，如 {'expression': '2+2'}", calculator_api)
    ]
    
    # 2. 准备大脑 (这里用我们写的 Dummy 模拟器)
    my_llm = DummyLLM()
    
    # 3. 组装框架
    agent = BaseAgent(llm=my_llm, tools=my_tools)
    
    # 4. 运行！
    agent.run("请问北京今天天气怎么样？")