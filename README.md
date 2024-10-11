# RedBusScrape
## Redbus Data Scraping Project

This project is a Python-based system for scraping RedBus website, managing SQL database connections, and providing a frontend interface for viewing the collected data using Streamlit.

## Features

- **Web Scraping:** Automates the extraction of data from RedBus website.
- **SQL Database Integration:** Handles the connection to SQL databases to store and retrieve scraped data.
- **Streamlit Dashboard:** Provides a simple web-based interface for viewing the data and to filter it.
- **Testing:** Includes tests to ensure the scraping logic is working correctly.

## Project Structure

- `connection_test.py`: Script to test database connections.
- `data_scrape.py`: Main script to handle the data extraction process.
- `scrape_test.py`: Contains tests to validate the web scraping functionality.
- `settings_template.py`: Template file for storing  database credentials.
- `sql_connector.py`: Manages SQL database connections and queries.
- `streamlit_app.py`: Provides a web interface using Streamlit to implement various data filters.
- `web_scraper.py`: Core web scraper functionality, responsible for scraping and processing web data.
- `requirement.txt`: A list of Python dependencies needed for the project.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/vikashgraja/RedBusScrape.git
   cd RedBusScrape
   ```

2. **Install dependencies:**

   Install the required Python packages using the following command:

   ```bash
   pip install -r requirement.txt
   ```

3. **Set up configuration:**

   Copy the `settings_template.py` to `settings.py` and fill in the database credentials.

   ```bash
   cp settings_template.py settings.py
   ```
## Usage

1. **Scrape the data:**

   First you have to scrape the data from RedBus Website.To scrape the website run:

   ```bash
   python data_scrape.py
   ```

2. **Run the application:**

   To launch the Streamlit app, run:

   ```bash
   streamlit run streamlit_app.py
   ```
