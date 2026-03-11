import os
from dotenv import load_dotenv

# load_dotenv() 会自动向上级目录寻找 .env 文件并加载
# override=True 确保 .env 里的变量能覆盖掉系统已有的同名环境变量
load_dotenv(override=True)

class LLMConfig:
    """LogicVerse 统一大模型配置管理类"""
    
    @classmethod
    def get_base_url(cls):
        return os.getenv("LLM_BASE_URL")

    @classmethod
    def get_api_key(cls):
        # 如果没有配置 Key (比如本地 Ollama)，默认返回占位符防止 OpenAI SDK 报错
        return os.getenv("LLM_API_KEY", "dummy-key")

    @classmethod
    def get_model(cls):
        return os.getenv("LLM_MODEL")

    @classmethod
    def get_proxy(cls):
        return os.getenv("LLM_PROXY")
    
    @classmethod
    def get_provider(cls):
        # 默认使用 openai 模式，自动转小写防呆
        return os.getenv("LLM_PROVIDER", "openai").lower()


# ==========================================
# 独立测试模块
# ==========================================
if __name__ == "__main__":
    print("🚀 === LogicVerse 统一环境加载测试 ===")
    
    base_url = LLMConfig.get_base_url()
    model = LLMConfig.get_model()
    api_key = LLMConfig.get_api_key()
    proxy = LLMConfig.get_proxy()
    
    # 状态展示
    print(f"🔗 Base URL: {base_url if base_url else '❌ 未配置'}")
    print(f"🤖 模型名称: {model if model else '❌ 未配置'}")
    print(f"🌐 全局代理: {proxy if proxy else '未配置 (直连模式)'}")
    
    # Key 的脱敏打印逻辑
    if api_key == "dummy-key" or api_key.lower() == "ollama":
        print(f"🔑 API Key : 占位符模式 ({api_key}) - 适用于本地部署")
    elif api_key:
        # 只显示前 4 位和后 4 位，保护你的真实资产
        masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"
        print(f"🔑 API Key : 已安全加载 ({masked_key})")
    else:
        print("🔑 API Key : ❌ 未找到")