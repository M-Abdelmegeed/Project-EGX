from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import GoogleSerperAPIWrapper
from tradingview_ta import TA_Handler, Exchange, Interval
import random
import yfinance as yf
import os

@tool("google_search", return_direct=True)
def searchGoogle(input:str) -> str:
    """Useful when you need to search the web to find fundamentals about stocks"""
    search = GoogleSerperAPIWrapper(serper_api_key=os.environ["SERPAPI_API_KEY"])
    return search.run(input)

# @tool("stock_price", return_direct=False)
# def getStockPrice(symbol:str) -> str:
#     """Useful for when you need to find out the price of a stock in NYSE. You should input the stock ticker used on the yfinance API"""
#     ticker = yf.Ticker(symbol)
#     todays_data = ticker.history(period='1d')
#     return round(todays_data['Close'].iloc[0], 2)

@tool("stock_price_egx", return_direct=False)
def getStockPriceEGX(symbol:str) -> str:
    """Useful for when you need to find out the current price of a stock in EGX. You should input the stock ticker used on the tradingView API"""
    stock = TA_Handler(
        symbol=symbol,
        screener='egypt',
        exchange='EGX',
        interval=Interval.INTERVAL_1_DAY
    )
    return stock.get_analysis().indicators['close']

@tool("stock_data_egx", return_direct=False)
def getStockDataEGX(symbol:str) -> str:
    """Useful for when you need to find out stock technicals and statistics. You should input the stock ticker used on the tradingView API. Input only 4 letters"""
    stock = TA_Handler(
        symbol=symbol,
        screener='egypt',
        exchange='EGX',
        interval=Interval.INTERVAL_1_DAY
    )
    return stock.get_analysis().indicators

tools = [getStockDataEGX, getStockPriceEGX, searchGoogle]

print(getStockDataEGX('FWRY'))