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

'---'

dynamic_filters.display_df()
