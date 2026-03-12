import os
from pathlib import Path
from dotenv import dotenv_values

class BaseConfig:
    """
    ⚙️ 实例化的多源配置基类
    支持链式调用，例如：Config().load_env().set("MODEL", "gpt-4")
    """
    def __init__(self):
        # 每一个 Config 实例都有自己独立的内存字典，绝对隔离！
        self._settings = {}

    @property
    def prefix(self) -> str:
        return ""

    def _normalize_key(self, key: str) -> str:
        key = key.upper()
        return key if key.startswith(self.prefix) else f"{self.prefix}{key}"

    def load_dict(self, config_dict: dict):
        for k, v in config_dict.items():
            self._settings[self._normalize_key(k)] = str(v) if v is not None else ""
        print(f"🧰 [{self.__class__.__name__}] 注入字典配置成功")
        return self  # 返回 self 以支持链式调用

    def load_yaml(self, yaml_path: str, node_name: str = None):
        try:
            import yaml
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
                target_data = data.get(node_name, data) if node_name else data
                for k, v in target_data.items():
                    self._settings[self._normalize_key(k)] = str(v) if v is not None else ""
            print(f"📜 [{self.__class__.__name__}] 加载 YAML 成功: {yaml_path}")
        except ImportError:
            print(f"⚠️ [{self.__class__.__name__}] 缺少 pyyaml 库")
        except FileNotFoundError:
            print(f"⚠️ [{self.__class__.__name__}] 未找到 YAML: {yaml_path}")
        return self

    def load_env(self, env_path: str = None):
        try:

            path_to_load = env_path or (Path.cwd() / '.env')
            if Path(path_to_load).exists():
                # 🌟 核心突破：使用 dotenv_values 而不是 load_dotenv
                # 它只解析文件返回字典，绝对不污染 os.environ 全局变量！
                env_dict = dotenv_values(dotenv_path=path_to_load)
                for k, v in env_dict.items():
                    if v is not None:
                        self._settings[k] = v
                print(f"📦 [{self.__class__.__name__}] 成功读取 .env: {path_to_load.name}")
            else:
                print(f"⚠️ [{self.__class__.__name__}] 未找到 .env: {path_to_load}")
        except ImportError:
            print(f"⚠️ [{self.__class__.__name__}] 缺少 python-dotenv 库")
        return self

    def set(self, key: str, value: str):
        """支持单条设置"""
        self._settings[self._normalize_key(key)] = value
        return self

    def get_value(self, key: str, default=None):
        full_key = self._normalize_key(key)
        # 优先级：当前实例的字典 > 电脑原生环境变量 > 默认值
        return self._settings.get(full_key) or os.getenv(full_key, default)


# ==========================================
# 🚀 具体的业务配置类
# ==========================================

class LLMConfig(BaseConfig):
    @property
    def prefix(self) -> str:
        return "LLM_"

    # 使用 @property 让外部调用更像属性访问
    @property
    def provider(self): return self.get_value("PROVIDER", "openai").lower()
    @property
    def base_url(self): return self.get_value("BASE_URL")
    @property
    def api_key(self): return self.get_value("API_KEY", "dummy-key")
    @property
    def model(self): return self.get_value("MODEL")
    @property
    def proxy(self): return self.get_value("PROXY")