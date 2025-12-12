import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class TavilySearchTool:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str) -> str:
        res = self.client.search(query=query, max_results=5)
        return str(res)
