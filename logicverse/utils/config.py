# config.py created automatically
import os

def load_env(file_path=".env"):
    """极简的 .env 加载器，无需依赖第三方库"""
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()



# 测试
if __name__ == "__main__":
    load_env()
    print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
    print("DEEPSEEK_API_KEY:", os.getenv("DEEPSEEK_API_KEY"))