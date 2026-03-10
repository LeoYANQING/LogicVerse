
---

# LogicVerse

**LogicVerse** 是一个轻量级、模块化的大语言模型（LLM）智能体框架，专注于通过逻辑推理（Reasoning）与动作（Acting）的循环来解决复杂问题。

## ✨ 核心特性

* **ReAct 规划引擎**：内置标准的 Reason + Act 思考循环，让智能体具备逐步拆解任务的能力。
* **轻量化设计**：核心逻辑简洁，易于二次开发与定制化。
* **自动化工具管理**：提供 `@registry.tool` 装饰器，支持自动从函数文档字符串中提取信息并生成工具描述。
* **多模型支持**：支持 OpenAI 接口及 Mock 模式，并设计了统一的 BaseLLM 基类方便扩展。
* **记忆管理**：具备内置的 `MemoryBuffer` 模块，自动维护多轮对话的上下文。

## 📂 项目结构

```text
LogicVerse/
├── logicverse/               # 核心框架包
│   ├── core/                 # 调度中心 (Agent Orchestrator)
│   ├── planners/             # 规划算法 (如 ReAct)
│   ├── tools/                # 工具注册与管理系统
│   ├── llms/                 # 模型适配器 (OpenAI, Mock 等)
│   ├── memory/               # 记忆缓冲区
│   └── utils/                # 配置文件加载与输出解析器
├── main.py                   # 示例运行入口
└── pyproject.toml            # 项目元数据与依赖管理

```

## 🚀 快速上手

### 1. 安装环境

确保已安装 Python 3.10+，并安装相关依赖：

```bash
pip install -e .

```

### 2. 配置密钥

在项目根目录创建 `.env` 文件，并填写你的 OpenAI API Key：

```text
OPENAI_API_KEY=your_sk_key_here

```

### 3. 运行示例

直接执行 `main.py` 启动智能体对话：

```python
from logicverse import LogicVerseAgent, registry
from logicverse import OpenAILLM

# 定义一个简单的工具
@registry.tool
def get_weather(city: str) -> str:
    """获取指定城市的实时天气"""
    return f"{city} 的天气晴，25摄氏度。"

# 启动智能体
agent = LogicVerseAgent(llm=OpenAILLM())
agent.run("帮我查一下北京的天气并给点穿衣建议。")

```

## 🗺️ 进化路线图 (Roadmap)

* **第一阶段：标准化 (Standardization)**
* [ ] 实现统一的 BaseLLM 接口。
* [ ] 完善 Tool 注册机制，支持自动提取函数注释。
* [ ] 强化 JSON Parser 的自动纠错逻辑。


* **第二阶段：增强能力 (Enhancement)**
* [ ] 引入更复杂的规划算法（如 Plan-and-Execute）。
* [ ] 支持外部向量数据库作为长期记忆。



## 📄 开源协议

[MIT License]

---
