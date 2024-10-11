"""This is a test file to test the SQL connection functions."""

from sql_connector import connect_scrape_database

connection = connect_scrape_database()
cursor = connection.cursor()
cursor.execute("DESC bus_routes")

result = cursor.fetchall()
for i in result:
    print(i)
