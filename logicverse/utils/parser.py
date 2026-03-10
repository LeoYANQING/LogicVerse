# parser.py created automatically
import json

class JsonParser:
    @staticmethod
    def parse(text: str) -> dict:
        """从 LLM 的杂乱输出中精准提取并解析 JSON"""
        clean_text = text.replace("```json", "").replace("```", "").strip()
        start = clean_text.find('{')
        end = clean_text.rfind('}')
        if start != -1 and end != -1:
            clean_text = clean_text[start:end+1]
        try:
            return json.loads(clean_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON解析失败: {e}")