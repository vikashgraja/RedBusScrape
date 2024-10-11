"""This is the Streamlit app to display various filters for the scraped data."""

import streamlit as st
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters

from sql_connector import connect_scrape_database

st.set_page_config(page_title='Bus Filter',
                   page_icon='🚌',
                   layout="wide",
                   )

@st.cache_data()
def retrive_data():
    """A cached function for retrieving data from the database."""
    connection = connect_scrape_database()
    query = "SELECT * FROM bus_routes"
    df = pd.read_sql(query, connection, index_col='id')
    return df

data = retrive_data()

st.title('🚌 Bus-Routes App')

dynamic_filters = DynamicFilters(data, filters=['route_name',
                                                                 'busname', 'bustype',
                                                                 'departing_time',])
dynamic_filters.display_filters(location='columns', num_columns=2, gap='medium')

new_df = dynamic_filters.filter_df()

price_range = None
min_price = new_df['price'].min()
max_price = new_df['price'].max()

rating_range = None
min_rating = new_df['star_rating'].min()
max_rating = new_df['star_rating'].max()

if min_price != max_price:
    price_range = st.slider('Price Range', min_price, max_price, (min_price, max_price),1.0)
else:
    price_range = (min_price, max_price)

if min_rating != max_rating:
    rating_range = st.slider('Rating Range', min_rating, max_rating, (min_rating, max_rating),0.1)
else:
    rating_range = (min_rating, max_rating)

filtered_df = new_df[(
    new_df['price'].between(price_range[0], price_range[1]))
    & (new_df['star_rating'].between(rating_range[0], rating_range[1]))
]

'---'

st.dataframe(filtered_df)
