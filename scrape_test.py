"""This is a test file to test the Scrape functions."""

from web_scraper import ScrapeRedbus
import pandas as pd

url = "https://www.redbus.in/online-booking/west-bengal-transport-corporation"

scraper = ScrapeRedbus(url)
data = scraper.start_scrape()

df = pd.DataFrame(data)
df.to_csv('test.csv', index=False)
print("Ok")