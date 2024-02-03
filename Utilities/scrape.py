import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.tradingview.com/markets/stocks-egypt/market-movers-all-stocks/"

# Set up a Selenium WebDriver (make sure to have the appropriate driver installed)
driver = webdriver.Chrome()

driver.get(url)
try:
    load_more_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "content-D4RPB3ZC"))
    )
except Exception as e:
    print(f"Error waiting for 'Load More' button: {e}")
    driver.quit()
    exit()
    
while True:
    try:
        if load_more_button.is_displayed():
            load_more_button.click()
            time.sleep(2)  # Adjust sleep time if necessary
        else:
            break
    except Exception as e:
        print(f"Error clicking 'Load More' button: {e}")
        break

time.sleep(5)

page_source = driver.page_source

driver.quit()

# Parse the HTML content of the page
soup = BeautifulSoup(page_source, 'html.parser')
table = soup.find('table', class_='table-Ngq2xrcG')
print("Table", table)

# Extract data from the table
data = []
for row in soup.select('tbody[tabindex="100"] tr'):
    columns = row.find_all('td')
    company_name = columns[0].text.strip()
    price = columns[1].text.strip()
    percent_change = columns[2].text.strip()

    ticker_tag = columns[0].find('a')
    if ticker_tag:
        ticker_symbol = ticker_tag.text.strip()
    else:
        ticker_symbol = None

    data.append({
        'Ticker Symbol': ticker_symbol,
        'Company Name': company_name,
    })

# Save data to a JSON file
json_filename = 'egx_stock_data.json'
with open(json_filename, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f'Data has been saved to {json_filename}')