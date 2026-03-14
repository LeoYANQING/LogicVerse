# 文件路径: logicverse/skills/loader.py
import os
import sys
import importlib.util
import re
from typing import Dict, Any
from logicverse.tools.registry import registry

class SkillLoader:
    """自动化技能装配车间"""

    @staticmethod
    def load(skill_dir: str) -> Dict[str, Any]:
        """
        加载标准技能包，返回：{"name": 技能名, "role": 提取的人设指令, "tools": [工具名列表]}
        """
        if not os.path.exists(skill_dir):
            raise FileNotFoundError(f"❌ 找不到技能包目录: {skill_dir}")

        skill_name = os.path.basename(os.path.normpath(skill_dir))
        print(f"🔄 [SkillLoader] 正在挂载外挂技能包: <{skill_name}> ...")

        # ==========================================
        # 1. 提取灵魂：解析 SKILL.md
        # ==========================================
        skill_md_path = os.path.join(skill_dir, "SKILL.md")
        instructions = f"你是一个具备 {skill_name} 技能的 AI 助手。"
        
        if os.path.exists(skill_md_path):
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 智能提取 ## Instructions 节点下的文本作为 Prompt
                match = re.search(r'## Instructions\n(.*?)(?=##|$)', content, re.DOTALL)
                if match:
                    instructions = match.group(1).strip()
                else:
                    instructions = content.strip() 
            print(f"  ├── 📄 成功解析 SKILL.md，已提取 Agent 核心指令")
        else:
            print(f"  ├── ⚠️ 未找到 SKILL.md，使用默认指令")

        # ==========================================
        # 2. 挂载肌肉：动态加载 scripts/ 下的工具
        # ==========================================
        scripts_dir = os.path.join(skill_dir, "scripts")
        loaded_tools = []
        
        if os.path.exists(scripts_dir):
            # 记录加载前的全局工具快照
            existing_tools = set(registry.tools.keys())
            
            for filename in os.listdir(scripts_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    filepath = os.path.join(scripts_dir, filename)
                    module_name = f"logicverse.dynamic_skills.{skill_name}.{filename[:-3]}"
                    
                    # 动态编译并导入未知的 .py 文件
                    spec = importlib.util.spec_from_file_location(module_name, filepath)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    print(f"  ├── 🔌 动态挂载脚本: {filename}")
            
            # 计算差集，精准捕获刚才被新脚本注册的 @registry.tool
            new_tools = set(registry.tools.keys()) - existing_tools
            loaded_tools = list(new_tools)
            print(f"  └── 🛠️ 自动识别并激活了 {len(loaded_tools)} 个专属工具: {loaded_tools}")

        return {
            "name": skill_name,
            "role": instructions,
            "tools": loaded_tools
        }