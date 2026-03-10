from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def chat(self, prompt: str) -> str:
        pass

class MockLLM(BaseLLM):
    """本地断网测试用的模拟大脑"""
    def __init__(self): 
        self.step = 0
        
    def chat(self, prompt: str) -> str:
        self.step += 1
        if self.step == 1:
            return '{"thought": "我要先查一下资料", "action": "demo_tool", "action_input": {"query": "Hello"}}'
        return '{"thought": "资料查完了", "action": "finish", "action_input": {"answer": "测试任务已通过 MockLLM 跑通。"}}'