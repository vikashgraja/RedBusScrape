"""AAAAAAAAAAA"""

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
    URL = f'https://www.redbus.in/online-booking/{stc}'

    scraper = ScrapeRedbus(URL)
    data_all_state.extend(scraper.start_scrape())

print("Done Scraping")

data = pd.DataFrame(data_all_state)

print('Cleaning Data',end=' ')
try:
    df = data.dropna().copy()
    df.price = df.price.str.replace(r'\D', '', regex=True)
    df.seats_available = df.seats_available.str.replace(r'\D', '', regex=True)
    df = df[(df['price'] != '') & (df['seats_available'] != '')]
    df = df.astype({'seats_available': 'int', 'price': 'float64'})

except Exception as e:
    data.to_csv('test2.csv', index=False)
    print("Error in cleaning Data")
    print(e)
    quit()

df.to_csv('test2.csv', index=False)
print("Done Saving Data")

connection = connect_scrape_database()
cursor = connection.cursor()

print('Saving Data in DB',end=' ')
for i, row in df.iterrows():
    INSERT_QUERY = """
    INSERT INTO bus_routes (route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(INSERT_QUERY, tuple(row))

connection.commit()
cursor.close()
connection.close()
print('Done')
