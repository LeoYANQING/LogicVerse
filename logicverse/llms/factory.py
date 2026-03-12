from logicverse.llms.openai_llm import OpenAILLM
from logicverse.utils.config import LLMConfig

class LLMFactory:
    """LLM 动态装配器：只接收 Config 实例进行装配"""
    
    _creators = {
        "openai": OpenAILLM,
    }

    @classmethod
    def register(cls, provider_name: str, llm_class):
        if not hasattr(llm_class, "chat"):
            raise TypeError(f"❌ 装配失败: {llm_class.__name__} 必须实现 chat 方法。")
        cls._creators[provider_name.lower()] = llm_class
        print(f"🔌 [装配器] 挂载新驱动: {provider_name}")

    @classmethod
    def create(cls, config: LLMConfig):
        """
        全自动装配流水线：必须显式传入配置实例
        """
        # 强校验：强制规范外部调用者的行为
        if not isinstance(config, LLMConfig):
            raise TypeError("❌ 工厂报错：必须传入一个实例化的 LLMConfig 对象！")

        provider = config.provider
        if provider not in cls._creators:
            supported = ", ".join(cls._creators.keys())
            raise ValueError(f"❌ 装配失败: 不支持 '{provider}'。支持列表: [{supported}]")
            
        llm_class = cls._creators[provider]

        print(f"⚙️ [Factory] 正在按 [{provider}] 协议从 Config 实例提取参数装配引擎...")
        
        # 从你传进来的 config 实例中提取所有参数，喂给大模型
        kwargs = {
            "api_key": config.api_key,
            "model": config.model,
            "base_url": config.base_url,
            "proxy": config.proxy
        }

        return llm_class(**kwargs)