"""AAAAAAAAAAA"""
import mysql.connector
from mysql.connector import Error

from settings import mysql_server, mysql_user, mysql_password

def connect_scrape_database():
    """AAAAAAAAAAA"""
    try:
        connection = mysql.connector.connect(
            host= mysql_server,
            user= mysql_user,
            password= mysql_password
        )

        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("CREATE DATABASE IF NOT EXISTS scrape_database")
            connection.database = 'scrape_database'

            table_create = '''
            CREATE TABLE IF NOT EXISTS bus_routes (
                id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Primary Key (Auto-increment)',
                route_name TEXT COMMENT 'Bus Route information for each state transport',
                route_link TEXT COMMENT 'Link to the route details',
                busname TEXT COMMENT 'Name of the bus',
                bustype TEXT COMMENT 'Type of the bus',
                departing_time TIME COMMENT 'Departure time',
                duration TEXT COMMENT 'Duration of the journey',
                reaching_time TIME COMMENT 'Arrival time',
                star_rating FLOAT COMMENT 'Rating of the bus',
                price DECIMAL(10, 2) COMMENT 'Price of the ticket',
                seats_available INT COMMENT 'Number of seats available'
            )'''
            cursor.execute(table_create)
            return connection
        # return None

    except Error as e:
        print(f"Error: \n{e}")
        return None
