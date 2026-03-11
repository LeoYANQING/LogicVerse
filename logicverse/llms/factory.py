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
            raise TypeError(f"❌ 装配失败: {llm_class.__name__} 必须实现 chat 方法 (继承 BaseLLM)。")
        
        cls._creators[provider_name.lower()] = llm_class
        print(f"🔌 [装配器] 成功挂载新模型驱动: {provider_name}")

    @classmethod
    def create(cls, provider: str = None, **kwargs):
        """
        制造流水线：根据配置实例化对应的 LLM。
        支持双模式：
        1. 自动装配：无参数调用，全自动读取 .env
        2. 参数装配：传入 api_key, model 等覆盖 .env 配置
        """
        # 1. 确定协议 (传参优先，否则读 .env)
        provider = provider or LLMConfig.get_provider()
        if not provider:
            provider = "openai" # 终极兜底
        provider = provider.lower().strip()
        
        # 2. 校验协议
        if provider not in cls._creators:
            supported = ", ".join(cls._creators.keys())
            raise ValueError(f"❌ 装配失败: 不支持的接口类型 '{provider}'。目前支持: [{supported}]")
            
        llm_class = cls._creators[provider]

        # 3. 装配日志展示 (提升框架可观测性)
        if kwargs:
            keys = ", ".join(kwargs.keys())
            print(f"⚙️ [Factory] 侦测到手动传参 ({keys})，正在按 [{provider}] 协议混合装配引擎...")
        else:
            print(f"⚙️ [Factory] 正在按 [{provider}] 协议标准装配引擎 (全自动读取 .env)...")

        # 4. 实例化引擎
        return llm_class(**kwargs)