
---

```markdown
# 🌌 LogicVerse (v0.1.0)

**LogicVerse** 是一个极其纯粹、高度解耦的大模型（LLM）智能体驱动框架。

它采用严格的**面向对象设计**与**依赖注入（DI）**机制，旨在为学术研究和工业级开发提供一个零副作用、可热插拔的 Agent 底座。无论是接入闭源大模型 API，还是本地部署的开源模型，LogicVerse 都能实现一行代码无缝切换。更重要的是，它原生支持**标准化技能包 (Skill Package)** 的全自动动态装配。

## ✨ 核心特性

* **🧰 多源配置中心 (Multi-Source Config):** 支持 `.env`、`YAML` 以及 Python `Dict` 动态链式注入，彻底告别全局环境变量污染。
* **🏭 动态装配车间 (Factory Pattern):** 底层引擎与配置严格隔离。通过 `LLMFactory` 动态产出兼容 OpenAI 标准格式的模型驱动（完美兼容 DeepSeek, Qwen, Ollama, vLLM 等）。
* **🧠 Meta-Agent 混合路由:** 内置微型路由分类器，根据任务复杂度自动分发至 `Direct` (极简对话)、`Plan` (宏大系统拆解) 或 `ReAct` (深度工具调用) 范式，极大地节省 Token。
* **🧩 DLC 式技能生态 (Skill Ecosystem):** 告别硬编码！支持标准化的外挂技能包。只需提供 `SKILL.md` 和独立脚本，框架即可实现全自动的人设解析与工具热挂载。

---

## 📁 核心架构

```text
LogicVerse/
├── .env                  # [私密] 默认环境变量配置
├── main.py               # [入口] 业务逻辑与 Agent 唤醒
├── logicverse/           # 📦 核心框架包 (底层黑盒)
│   ├── core/             # 🧠 中枢神经 (Meta-Agent 动态路由与执行循环)
│   ├── llms/             # 🔌 驱动引擎 (OpenAILLM 纯净接口, LLMFactory 动态装配)
│   ├── memory/           # 💾 记忆模块 (Multi-Agent 独立上下文缓冲区)
│   ├── planners/         # 🗺️ 思维策略 (Direct / Plan / ReAct 提示词构建器)
│   ├── skills/           # ✨ 技能引擎 (SkillLoader 自动化装配车间)
│   ├── tools/            # 🛠️ 工具中心 (魔法装饰器 @registry.tool)
│   └── utils/            # ⚙️ 基础设施 (链式 BaseConfig 与 JsonParser)
└── skills/               # 🧩 业务外挂技能包集市 (用户自定义)
    └── academic_researcher/  # 示例：学术研究员技能包
        ├── SKILL.md      # 声明式大脑：技能说明与 System Prompt
        └── scripts/      # 肌肉与神经：专属的 Python 工具脚本

```

---

## 🚀 快速开始

### 1. 环境准备与配置

确保你安装了框架的基础依赖：

```bash
pip install openai python-dotenv pyyaml

```

在项目根目录创建一个 `.env` 文件：

```env
LLM_PROVIDER=openai
LLM_BASE_URL=[https://api.deepseek.com/v1](https://api.deepseek.com/v1)
LLM_API_KEY=sk-your-api-key-here
LLM_MODEL=deepseek-chat

```

### 2. 唤醒基础 Agent

如果你只想快速跑一个单体任务，可以在 `main.py` 中直接定义工具并运行：

```python
from logicverse.utils.config import LLMConfig
from logicverse.llms.factory import LLMFactory
from logicverse import LogicVerseAgent, registry

@registry.tool
def calculate_math(expression: str) -> str:
    """强大的数学计算器。参数 expression 必须是合法的 Python 表达式。"""
    return str(eval(expression))

def main():
    config = LLMConfig().load_env()
    llm = LLMFactory.create(config)
    agent = LogicVerseAgent(llm=llm)
    agent.run("你好，请帮我算一下 1024 乘以 3.14 的结果。")

if __name__ == "__main__":
    main()

```

---

## 🧩 进阶指南：如何编写与装配“技能包” (Skills)

LogicVerse 最强大的特性在于**技能与框架的彻底解耦**。你可以像制作游戏 DLC 一样制作技能包，并在运行时全自动挂载。

### Step 1: 建立技能包目录

在根目录下的 `skills/` 文件夹中，新建你的技能目录，例如 `my_first_skill/`。结构必须如下：

```text
skills/my_first_skill/
├── SKILL.md          # 必须：技能说明与指令
└── scripts/          # 可选：存放工具函数的 Python 脚本
    └── tools.py

```

### Step 2: 编写 SKILL.md (注入灵魂)

框架会自动解析 `SKILL.md`，并**精准提取 `## Instructions` 节点下的内容**作为 Agent 的系统指令（System Prompt）。

```markdown
# 我的专属技能包
这是一个测试用的技能包。

## Instructions
你是一个精通数据分析的 AI 助手。
你的工作原则：
1. 必须使用提供的工具获取数据。
2. 分析完毕后，立刻给出结论并调用 finish 结束任务。

```

### Step 3: 编写专属脚本 (赋予肌肉)

在 `scripts/` 目录下创建任意 `.py` 文件，使用 `@registry.tool` 注册工具。框架会在加载时**动态编译并捕获**这些新武器。

```python
# skills/my_first_skill/scripts/tools.py
from logicverse.tools.registry import registry

@registry.tool
def fetch_database_data(query: str) -> str:
    """[专属工具] 模拟从数据库获取数据"""
    return f"执行查询 [{query}] 成功，返回数据：[10, 20, 30]"

```

### Step 4: 一键自动化装配

在你的主程序中，使用 `SkillLoader` 加载文件夹，瞬间造出一个全副武装的专家 Agent！

```python
from logicverse.skills.loader import SkillLoader
from logicverse import LogicVerseAgent
from logicverse.llms.factory import LLMFactory
from logicverse.utils.config import LLMConfig

# 1. 初始化底座
llm = LLMFactory.create(LLMConfig().load_env())

# 2. 🪄 魔法时刻：一键加载外部技能包
skill_package = SkillLoader.load("./skills/my_first_skill")

# 3. 实例化专家 Agent
expert_agent = LogicVerseAgent(
    name="Data_Analyst",
    role=skill_package["role"],   # 自动提取的 Instructions
    tools=skill_package["tools"], # 自动扫描并挂载的专属工具
    llm=llm
)

expert_agent.run("帮我查一下数据库里最新的销售数据。")

```

---

## 🔬 终极玩法：Multi-Agent 与多模型隔离

得益于极端的依赖隔离设计，你可以在同一个脚本中实例化多个不同配置的大模型（跨模型协作），并给它们分配不同的技能包，它们之间绝对不会串台：

```python
# 实例 A：使用本地模型 + 学术研究技能包
llm_local = LLMFactory.create(LLMConfig().load_env(".env.local"))
skill_academic = SkillLoader.load("./skills/academic")
researcher = LogicVerseAgent("Researcher", skill_academic["role"], llm_local, skill_academic["tools"])

# 实例 B：使用云端模型 + 代码开发技能包
llm_cloud = LLMFactory.create(LLMConfig().load_dict({"provider": "openai", "model": "qwen-max"}))
skill_coder = SkillLoader.load("./skills/coder")
coder = LogicVerseAgent("Coder", skill_coder["role"], llm_cloud, skill_coder["tools"])

# 让他们通过上下文传递完成协同工作...

```

---

## 👨‍💻 作者与支持

* **核心开发者**: Wenbin Zuo (CDI Lab)
* **版本**: v0.1.0 (Beta)

*LogicVerse 致力于在复杂逻辑与系统解耦中寻找最优雅的平衡点，探索 Agent 架构的未来范式。*

```
