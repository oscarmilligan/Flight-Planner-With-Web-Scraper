import streamlit as st
import pandas as pd
import datetime
from scrapers.wizzair import wizzair_scraper

# --- Data Loading and Preparation ---
df_airport_codes_unfiltered = pd.read_csv('data/airport-codes.csv')
types_to_drop = ['closed', 'heliport', 'balloonport', 'seaplane base', 'small_airport', 'medium_airport']
df_airport_codes_unfiltered = df_airport_codes_unfiltered[~df_airport_codes_unfiltered['type'].isin(types_to_drop)]
df_airport_codes = df_airport_codes_unfiltered.drop(columns=['type', 'elevation_ft', 'gps_code', 'iata_code', 'local_code', 'iso_region', 'icao_code', 'coordinates'])
df_airport_codes['continent'] = df_airport_codes['continent'].replace({'OC': 'Oceania', 'EU': 'Europe', 'AN': 'Antarctica', 'NA': 'North America', 'SA': 'South America', 'AS': 'Asia', 'AF': 'Africa'})

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Flight Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Flight Planner with Web Scraper")
st.markdown("Use this link [https://www.iban.com/country-codes](https://www.iban.com/country-codes) to find the country from the code.")

# --- Sidebar Widgets ---

# -- Departure Date --
st.sidebar.subheader("When are you flying?")
selected_date = st.sidebar.date_input(
    "Select Departure Date",
    datetime.date.today()
)

# -- Departure Selection --
st.sidebar.subheader("Where are you coming from?")
continents = sorted(df_airport_codes['continent'].dropna().unique().tolist())

dep_continent = st.sidebar.selectbox("Select Continent", continents, key='dep_continent')
df_dep_filtered_continent = df_airport_codes[df_airport_codes['continent'] == dep_continent]

dep_countries = sorted(df_dep_filtered_continent['iso_country'].dropna().unique().tolist())
dep_country = st.sidebar.selectbox("Select Country", dep_countries, key='dep_country')
df_dep_filtered_country = df_dep_filtered_continent[df_dep_filtered_continent['iso_country'] == dep_country]

dep_cities = sorted(df_dep_filtered_country['municipality'].dropna().unique().tolist())
dep_city = st.sidebar.selectbox("Select City", dep_cities, key='dep_city')
df_dep_filtered_city = df_dep_filtered_country[df_dep_filtered_country['municipality'] == dep_city]

dep_airports = sorted(df_dep_filtered_city['name'].dropna().unique().tolist())
departure_airport = st.sidebar.selectbox("Select Airport", dep_airports, key='dep_airport')

# -- Destination Selection --
st.sidebar.subheader("Where are you going to?")
dest_continent = st.sidebar.selectbox("Select Continent", continents, key='dest_continent')
df_dest_filtered_continent = df_airport_codes[df_airport_codes['continent'] == dest_continent]

dest_countries = sorted(df_dest_filtered_continent['iso_country'].dropna().unique().tolist())
dest_country = st.sidebar.selectbox("Select Country", dest_countries, key='dest_country')
df_dest_filtered_country = df_dest_filtered_continent[df_dest_filtered_continent['iso_country'] == dest_country]

dest_cities = sorted(df_dest_filtered_country['municipality'].dropna().unique().tolist())
dest_city = st.sidebar.selectbox("Select City", dest_cities, key='dest_city')
df_dest_filtered_city = df_dest_filtered_country[df_dest_filtered_country['municipality'] == dest_city]

dest_airports = sorted(df_dest_filtered_city['name'].dropna().unique().tolist())
destination_airport = st.sidebar.selectbox("Select Airport", dest_airports, key='dest_airport')

# --- Scraper Execution ---
if st.sidebar.button("Run Scraper"):
    formatted_date = selected_date.strftime("%A %d %B %Y")
    
    with st.spinner(f"Searching for flights from {departure_airport} to {destination_airport}..."):
        # Call the scraper function with the selected values from the sidebar
        scraper_result = wizzair_scraper(departure_airport, destination_airport, formatted_date)
        
        if not scraper_result.empty:
            st.success("Scraper ran successfully!")
            st.write(scraper_result)  # Display the scraper results
        else:
            st.warning("Scraper did not return any results.")