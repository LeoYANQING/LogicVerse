import os
from pathlib import Path

def create_logicverse_architecture():
    # 1. 定义项目根目录（这里设为当前目录）
    base_dir = Path.cwd()
    print(f"🚀 开始在 {base_dir} 构建 LogicVerse 目录架构...\n")

    # 2. 定义所有需要创建的文件路径
    files_to_create = [
        # 根目录文件
        ".env",
        ".gitignore",
        "pyproject.toml",
        "README.md",
        "main.py",
        
        # logicverse 核心包
        "logicverse/__init__.py",
        
        # core 调度层
        "logicverse/core/__init__.py",
        "logicverse/core/agent.py",
        
        # llms 模型层
        "logicverse/llms/__init__.py",
        "logicverse/llms/base.py",
        "logicverse/llms/openai_llm.py",
        
        # memory 记忆层
        "logicverse/memory/__init__.py",
        "logicverse/memory/buffer.py",
        
        # planners 策略层
        "logicverse/planners/__init__.py",
        "logicverse/planners/react.py",
        
        # tools 工具层
        "logicverse/tools/__init__.py",
        "logicverse/tools/registry.py",
        
        # utils 基础设施层
        "logicverse/utils/__init__.py",
        "logicverse/utils/parser.py",
        "logicverse/utils/config.py",
    ]

    # 3. 核心生成逻辑
    for file_path in files_to_create:
        full_path = base_dir / file_path
        
        # 创建父级目录 (如果不存在的话)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建空文件 (如果不存在的话)
        if not full_path.exists():
            with open(full_path, "w", encoding="utf-8") as f:
                # 顺手给几个特殊文件写点默认内容
                if file_path == ".gitignore":
                    f.write(".env\n__pycache__/\n*.pyc\n*.pyo\nbuild/\ndist/\n*.egg-info/\n")
                elif file_path == ".env":
                    f.write("# 在这里填写你的 API 密钥，千万不要提交到 Git！\nOPENAI_API_KEY=sk-...\nDEEPSEEK_API_KEY=sk-...\n")
                else:
                    f.write(f"# {full_path.name} created automatically\n")
            print(f"✅ 创建文件: {file_path}")
        else:
            print(f"⏭️  文件已存在, 跳过: {file_path}")

    print("\n🎉 架构生成完毕！你可以开始往里面填肉了。")

if __name__ == "__main__":
    create_logicverse_architecture()