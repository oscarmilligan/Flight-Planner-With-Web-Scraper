import streamlit as st
import pandas as pd
import datetime

df_airport_codes_unfiltered = pd.read_csv('data/airport-codes.csv')
types_to_drop = ['closed', 'heliport', 'balloonport', 'seaplane base']
df_airport_codes_unfiltered = df_airport_codes_unfiltered[~df_airport_codes_unfiltered['type'].isin(types_to_drop)]
df_airport_codes= df_airport_codes_unfiltered.drop(columns=['type','elevation_ft','gps_code','iata_code','local_code','iso_region','icao_code','coordinates'])
df_airport_codes['continent'] = df_airport_codes['continent'].replace({'OC': 'Oceania', 'EU': 'Europe', 'AN':'Antartica', None: 'North America', 'SA': 'South America', 'AS': 'Asia', 'AF': 'Africa'})
#print(df_airport_codes.columns)
unique_continents = df_airport_codes_unfiltered['continent']    

def Departure():
    # Create a list of continents from the DataFrame
    continents = df_airport_codes['continent'].sort_values().unique().tolist()
    s_continent = st.sidebar.selectbox("Select Continent", continents)
    
    # Filter the DataFrame based on the selected continent  
    df_filtered = df_airport_codes[df_airport_codes['continent'] == s_continent]

    # Create a list of countries from the filtered DataFrame
    countries = df_filtered['iso_country'].sort_values().unique().tolist()
    s_country = st.sidebar.selectbox("Select Country", countries)

    # Filter the DataFrame based on the selected country
    df_filtered = df_filtered[df_filtered['iso_country'] == s_country]

    # Create a list of cities from the filtered DataFrame
    cities = df_filtered['municipality'].sort_values().unique().tolist() 
    s_city = st.sidebar.selectbox("Select City", cities)

    # Filter the DataFrame based on the selected city
    df_filtered = df_filtered[df_filtered['municipality'] == s_city]

    # Create a list of airports from the filtered DataFrame
    airports = df_filtered['name'].sort_values().unique().tolist()
    Departure_airport = st.sidebar.selectbox("Select Airport", airports)
    return Departure_airport

def Destination():
    # Create a list of continents from the DataFrame
    continents = df_airport_codes['continent'].sort_values().unique().tolist()
    s_continent = st.sidebar.selectbox("Select destination continent", continents)
    
    # Filter the DataFrame based on the selected continent  
    df_filtered = df_airport_codes[df_airport_codes['continent'] == s_continent]

    # Create a list of countries from the filtered DataFrame
    countries = df_filtered['iso_country'].sort_values().unique().tolist()
    s_country = st.sidebar.selectbox("Select destination country", countries)

    # Filter the DataFrame based on the selected country
    df_filtered = df_filtered[df_filtered['iso_country'] == s_country]

    # Create a list of cities from the filtered DataFrame
    cities = df_filtered['municipality'].sort_values().unique().tolist() 
    s_city = st.sidebar.selectbox("Select destination city", cities)

    # Filter the DataFrame based on the selected city
    df_filtered = df_filtered[df_filtered['municipality'] == s_city]

    # Create a list of airports from the filtered DataFrame
    airports = df_filtered['name'].sort_values().unique().tolist()
    Destination_airport = st.sidebar.selectbox("Select destination airport", airports)
    return Destination_airport

def departure_date():
    # Get the date object from the user's input
    selected_date = st.sidebar.date_input(
        "Select Departure Date", 
        datetime.date.today() # It's good practice to provide a default value
    )

    # Format the date object into the desired string format
    formatted_date_string = selected_date.strftime("%A %d %B %Y")
    
    # Display the resultx
    st.write("Departure date:", formatted_date_string)
    
    return formatted_date_string
    

#streamlit configuration and page setup
st.set_page_config(
    page_title="Flight Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Flight Planner with Web Scraper")
st.markdown("Use this link https://www.iban.com/country-codes to find the country from the code.")
st.sidebar.subheader("When are you flying?")
departure_date()
st.sidebar.subheader("Where are you coming from?")
Departure()
st.sidebar.subheader("Where are you going to?")
Destination()
