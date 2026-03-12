from .base import BaseLLM

class OpenAILLM(BaseLLM):
    """适配 OpenAI 接口格式的大模型 (纯净接口版：完全由外部注入参数)"""
    
    def __init__(self, api_key: str, model: str, base_url: str = None, proxy: str = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("请先安装 openai 库: pip install openai")

        # 1. 极致纯净：只接收外部传进来的参数，绝不去读任何配置
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.proxy = proxy

        # 强校验：既然是你外面传进来的，那就必须传完整
        if not self.api_key or not self.model:
            raise ValueError("引擎启动失败：必须明确提供 api_key 和 model 参数。")

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