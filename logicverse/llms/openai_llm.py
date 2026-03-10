from .base import BaseLLM

class OpenAILLM(BaseLLM):
    """适配 OpenAI 接口格式的大模型 (兼容 DeepSeek, Qwen 等)"""
    def __init__(self, api_key: str, model: str, base_url: str = None):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            self.model = model
        except ImportError:
            raise ImportError("请先安装 openai 库: pip install openai")

    def chat(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1 # 保持低温度以输出稳定的 JSON
            )
            return response.choices[0].message.content
        except Exception as e:
            return f'{{"thought": "API异常", "action": "finish", "action_input": {{"answer": "大模型接口报错: {str(e)}"}} }}'