from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch


load_dotenv()

def tavily_search(input: str):
    tool = TavilySearch(
        max_results=5,
        topic="general",
    )
    return tool.run(input)

def searchGoogle(input: str) -> dict:
    """Searches Google (via Serper API) and returns structured results."""
    search = GoogleSerperAPIWrapper(serper_api_key=os.environ["SERPAPI_API_KEY"])
    result = search.results(input)
    return result



print(tavily_search("AAPL:NYSE"))