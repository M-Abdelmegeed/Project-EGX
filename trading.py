from tradingview_ta import TA_Handler, Exchange, Interval
import json

json_filename = 'EGX Stock data/egx_stock_data.json'
with open(json_filename, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    
    
for entry in data:
    stock = TA_Handler(
        symbol=entry['Ticker Symbol'],
        screener='egypt',
        exchange='EGX',
        interval=Interval.INTERVAL_1_DAY
    )

    print(entry['Ticker Symbol'],stock.get_indicators(["open", "close"]))
    print(stock.get_analysis().indicators)
    print('-----------------------')