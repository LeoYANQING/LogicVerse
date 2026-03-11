from .core.agent import LogicVerseAgent
from .tools.registry import registry
from .llms.base import BaseLLM, MockLLM
from .llms.openai_llm import OpenAILLM
from .utils.config import LLMConfig  # 👈 核心修改：改为导入你写的强大配置类

__version__ = "0.0.1"
# 👈 核心修改：把 load_env 从暴露名单里踢出去，换成 LLMConfig
__all__ = ["LogicVerseAgent", "registry", "BaseLLM", "MockLLM", "OpenAILLM", "LLMConfig"]