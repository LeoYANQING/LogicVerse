from logicverse.llms.openai_llm import OpenAILLM
from logicverse.utils.config import LLMConfig

class LLMFactory:
    """LLM 动态装配器：根据 Provider 自动组装对应的模型接口"""
    
    # 核心注册表：出厂默认自带 openai 模式
    _creators = {
        "openai": OpenAILLM,
    }

    @classmethod
    def register(cls, provider_name: str, llm_class):
        """
        开放的装配接口：允许外部开发者动态添加新的 LLM 驱动。
        只要继承了 BaseLLM，就能插进 LogicVerse。
        """
        if not hasattr(llm_class, "chat"):
            raise TypeError(f"装配失败: {llm_class.__name__} 必须实现 chat 方法 (继承 BaseLLM)。")
        
        cls._creators[provider_name.lower()] = llm_class
        print(f"🔌 [装配器] 成功挂载新模型驱动: {provider_name}")

    @classmethod
    def create(cls, provider: str = None, **kwargs):
        """
        制造流水线：根据配置实例化对应的 LLM。
        可以手动指定 provider，否则自动从 .env 读取。
        """
        provider = provider or LLMConfig.get_provider()
        
        if provider not in cls._creators:
            supported = ", ".join(cls._creators.keys())
            raise ValueError(f"装配失败: 不支持的接口类型 '{provider}'。目前支持的列表: [{supported}]")
            
        llm_class = cls._creators[provider]
        return llm_class(**kwargs)