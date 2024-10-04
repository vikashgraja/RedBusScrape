import pandas as pd

from sql_connector import connect_scrape_database
from web_scraper import ScrapeRedbus

states = [
    'apsrtc',
    'ksrtc-kerala',
    'tsrtc',
    'ktcl',
    'rsrtc',
    'south-bengal-state-transport-corporation-sbstc',
    'hrtc',
    'astc',
    'uttar-pradesh-state-road-transport-corporation-upsrtc',
    'west-bengal-transport-corporation',
]

data_all_state = []
for stc in states:
    url = f'https://www.redbus.in/online-booking/{stc}'

    scraper = ScrapeRedbus(url)
    data_all_state += [scraper.start_scrape()]

df = pd.DataFrame(data_all_state)
df.to_csv('test.csv', index=False)
print("Ok")

# connection = connect_scrape_database()
# cursor = connection.cursor()

