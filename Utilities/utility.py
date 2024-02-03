from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

# Load your JSON data
with open('egx_stock_data.json', 'r') as json_file:
    company_data = json.load(json_file)

# Set up the Selenium WebDriver
driver = webdriver.Chrome()


url = 'https://www.african-markets.com/en/stock-markets/egx/listed-companies'
driver.get(url)


time.sleep(5)

table = driver.find_element(By.CLASS_NAME, 'tabtable-rs_01k0jris')
rows = table.find_elements(By.TAG_NAME, 'tr')[1:] 

# Loop through each row in the table
for row in rows:
    columns = row.find_elements(By.TAG_NAME, 'td')
    
    # Extract relevant information
    company_name = columns[0].text.strip()
    sector = columns[1].text.strip()

    # Check if the company name is in your JSON data
    for company in company_data:
        print( str(company_name).upper() + "====" +  company['Company Name'])
        if str(company_name).upper() == str(company['Company Name']):
            company['Sector'] = sector
            break

# Save the modified JSON data
with open('egx_stock_data.json', 'w') as json_file:
    json.dump(company_data, json_file, indent=2)

# Close the browser
driver.quit()

print("Comparison and modification complete")