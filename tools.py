from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import GoogleSerperAPIWrapper
import random
import yfinance as yf
import os


@tool("google_search", return_direct=True)
def searchGoogle(input:str) -> str:
    """Useful when you need to search the web for EGX stocks fundamentals"""
    search = GoogleSerperAPIWrapper(serper_api_key=os.environ["SERPAPI_API_KEY"])
    return search.run(input)

@tool("stock_price", return_direct=False)
def getStockPrice(symbol:str) -> str:
    """Useful for when you need to find out the price of stock that is not in EGX. You should input the stock ticker used on the yfinance API"""
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return round(todays_data['Close'].iloc[0], 2)

@tool("lower_case", return_direct=True)
def toLowerCase(input:str) -> str:
    """Returns the input as lower case"""
    return input.lower()

tools = [toLowerCase, getStockPrice, searchGoogle]