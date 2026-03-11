from .base import BaseLLM
from logicverse.utils.config import LLMConfig  # 引入你写的强大配置类

class OpenAILLM(BaseLLM):
    """适配 OpenAI 接口格式的大模型 (兼容 DeepSeek, Qwen, 本地 Ollama 等)"""
    
    def __init__(self, api_key: str = None, model: str = None, base_url: str = None, proxy: str = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("请先安装 openai 库: pip install openai")

        # 1. 动态优先级：手动传入参数 > 你的 LLMConfig 统一提取
        self.api_key = api_key or LLMConfig.get_api_key()
        self.model = model or LLMConfig.get_model()
        self.base_url = base_url or LLMConfig.get_base_url()
        self.proxy = proxy or LLMConfig.get_proxy()

        # 安全阻断：有了 dummy-key 保护，这里只需要校验 model 即可
        if not self.model:
            raise ValueError("引擎启动失败：未检测到 LLM_MODEL，请检查 .env 配置。")

        # 2. 智能网络代理路由
        http_client = None
        if self.proxy:
            try:
                import httpx
                # 防御逻辑：本地服务 (Ollama/vLLM) 坚决不走代理
                if self.base_url and ("localhost" in self.base_url or "127.0.0.1" in self.base_url):
                    pass
                else:
                    http_client = httpx.Client(proxies=self.proxy)
            except ImportError:
                print("⚠️ 警告：检测到代理配置，但缺少 httpx 库。如需代理请 pip install httpx")

        # 3. 初始化底层客户端
        self.client = OpenAI(
            api_key=self.api_key, 
            base_url=self.base_url,
            http_client=http_client
        )

    def chat(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            return f'{{"thought": "API调用崩溃", "action": "finish", "action_input": {{"answer": "接口报错: {str(e)}"}} }}'
