import arxiv
import requests
from typing import Optional
from logicverse.tools.registry import registry

@registry.tool
def auto_search_arxiv(query: str, max_results: int = 3) -> str:
    """
    [学术实测] 调用 arXiv 官方接口检索最新论文。支持复杂布尔逻辑。
    
    Args:
        query (str): 英文学术关键词或查询语句，例如 'abs:\"3D Vision\" AND ti:\"Transformer\"'。
        max_results (int): 检索结果数量上限，默认 3。
    """
    print(f"🌐 正在向 arXiv 请求: {query}...")
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results_list = []
        for result in search.results():
            info = (
                f"【标题】: {result.title}\n"
                f"【作者】: {[a.name for a in result.authors]}\n"
                f"【发布日期】: {result.published.strftime('%Y-%m-%d')}\n"
                f"【摘要】: {result.summary[:300]}...\n"
                f"【PDF链接】: {result.pdf_url}\n"
            )
            results_list.append(info)
        
        if not results_list:
            return "未找到相关文献，请尝试更换关键词。"
            
        return "\n---\n".join(results_list)
    except Exception as e:
        return f"检索过程中出错: {str(e)}"

@registry.tool
def get_paper_impact(paper_title: str) -> str:
    """
    [学术实测] 通过 Semantic Scholar API 获取论文的引用量和影响力。
    
    Args:
        paper_title (str): 论文的完整标题。
    """
    print(f"🔍 正在检索论文影响力: {paper_title}...")
    try:
        # 使用 Semantic Scholar 公开搜索 API
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": paper_title,
            "limit": 1,
            "fields": "title,citationCount,influentialCitationCount,externalIds,url"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "data" in data and len(data["data"]) > 0:
            paper = data["data"][0]
            impact_info = (
                f"【语义学者链接】: {paper.get('url')}\n"
                f"【总引用量】: {paper.get('citationCount', '未知')}\n"
                f"【高影响力引用】: {paper.get('influentialCitationCount', '未知')}\n"
                f"【说明】: 该数据由 Semantic Scholar 实时提供。"
            )
            return impact_info
        else:
            return "未在 Semantic Scholar 数据库中找到该论文的影响力信息。"
    except Exception as e:
        return f"影响力查询失败: {str(e)}"