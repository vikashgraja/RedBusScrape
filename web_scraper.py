"""This module provides functions to scrape RedBus web page."""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class ScrapeRedbus:
    """This class provides functions to scrape RedBus web page."""
    def __init__(self, url, timeout=5):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.timeout = timeout

    def load_url(self, url):
        """Load url"""
        self.driver.get(url)
        time.sleep(self.timeout)

    def ispagenated(self):
        """Finds weather the web page is paginated"""
        self.driver.get(self.url)
        try:
            pagination_container = self.driver.find_element(By.CLASS_NAME, "DC_117_paginationTable")
            page_tabs = pagination_container.find_elements(By.CLASS_NAME, "DC_117_pageTabs")
            num_pages = len(page_tabs)
            return num_pages
        except NoSuchElementException:
            return False

    def scrape_bus_routes(self):
        """Function to scrape bus routes in the page"""
        route_elements = self.driver.find_elements(By.CLASS_NAME, 'route')
        bus_routes_link = [route.get_attribute('href') for route in route_elements]
        bus_routes_name = [route.text.strip() for route in route_elements]
        return bus_routes_link, bus_routes_name

    def scrape_bus_details(self, url, route_name):
        """Function to scrape bus details in the page"""
        try:
            self.load_url(url)

            view_buses_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "button"))
            )
            self.driver.execute_script("arguments[0].click();", view_buses_button)
            time.sleep(self.timeout)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.timeout)

            bus_name_elements = self.driver.find_elements(By.CLASS_NAME,
                "travels.lh-24.f-bold.d-color")
            bus_type_elements = self.driver.find_elements(By.CLASS_NAME,
                "bus-type.f-12.m-top-16.l-color.evBus")
            departing_time_elements = self.driver.find_elements(By.CLASS_NAME,
                 "dp-time.f-19.d-color.f-bold")
            duration_elements = self.driver.find_elements(By.CLASS_NAME,
                "dur.l-color.lh-24")
            reaching_time_elements = self.driver.find_elements(By.CLASS_NAME,
                "bp-time.f-19.d-color.disp-Inline")
            star_rating_elements = self.driver.find_elements(By.XPATH,
                "//div[@class='rating-sec lh-24']")
            price_elements = self.driver.find_elements(By.CLASS_NAME,
                                                       "fare.d-block")

            seat_availability_elements = self.driver.find_elements(By.XPATH,
        "//div[contains(@class, 'seat-left m-top-30') or contains(@class, 'seat-left m-top-16')]")

            bus_details = []
            bus_len = len(bus_name_elements)
            for i in range(bus_len):
                bus_detail = {
                    "route_name": route_name,
                    "route_link": url,
                    "busname": bus_name_elements[i].text,
                    "bustype": bus_type_elements[i].text,
                    "departing_time": departing_time_elements[i].text,
                    "duration": duration_elements[i].text,
                    "reaching_time": reaching_time_elements[i].text,
                    "star_rating": star_rating_elements[i].text if i < len(
                        star_rating_elements) else '0',
                    "price": price_elements[i].text,
                    "seats_available": seat_availability_elements[i].text if i < len(
                        seat_availability_elements) else '0'
                }
                bus_details.append(bus_detail)
            return bus_details

        except Exception as e:
            print(f"Error occurred while accessing {url}: {str(e)}")
            return []

    def start_scrape(self):
        """A wraper function for scraping RedBus web page."""
        all_bus_details = []
        pages = self.ispagenated()
        if pages:
            for page in range(1, pages + 1):
                self.load_url(self.url)
                try:
                    if page > 1:
                        pagination_tab = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                 f"//div[contains(@class, 'DC_117_pageTabs')][text()='{page}']"))
                        )
                        self.driver.execute_script("arguments[0].scrollIntoView();", pagination_tab)
                        self.driver.execute_script("arguments[0].click();", pagination_tab)
                        time.sleep(5)

                    all_bus_routes_link, all_bus_routes_name = self.scrape_bus_routes()
                    for link, name in zip(all_bus_routes_link, all_bus_routes_name):
                        bus_details = self.scrape_bus_details(link, name)
                        if bus_details:
                            all_bus_details.extend(bus_details)

                except Exception as e:
                    print(f"Error occurred while accessing page {page}: {str(e)}")
        else:
            all_bus_routes_link, all_bus_routes_name = self.scrape_bus_routes()
            for link, name in zip(all_bus_routes_link, all_bus_routes_name):
                bus_details = self.scrape_bus_details(link, name)
                if bus_details:
                    all_bus_details.extend(bus_details)

        self.driver.quit()
        return all_bus_details
