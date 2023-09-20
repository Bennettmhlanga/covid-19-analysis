import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Title
def run():
    img = Image.open('logo 1.jpg')
    st.image(img)
    st.title('Covid-19 Report Dashboard for Berlin City')

    link = '[By Bennett Mhlanga](https://www.linkedin.com/in/bennett-mhlanga-b24259185)'
    st.sidebar.markdown(link, unsafe_allow_html=True)

run()

st.write("""
------------
This dashboard gives you daily updates on the 7-day-incidence, which is the number of Covid-19 cases per 100,000 people in a specific area. It also provides the rolling 7-day average of new cases and the total number of new reported cases. You can choose the districts you want to see and compare.

The data comes directly from the Berlin government and is sourced from their official website berlin.de.

For mobile devices kindly tap the ">" symbol in the top left corner to select the district and timeframe you're interested in.
""")
st.write("---")

# Getting Data
def get_data():
    historic_district_cases_url = 'https://www.berlin.de/lageso/_assets/gesundheit/publikationen/corona/meldedatum_bezirk.csv'
    historic_district_cases = pd.read_csv(historic_district_cases_url, sep=';', encoding='unicode_escape')
    return historic_district_cases

historic_district_cases_df = get_data()
st.write(historic_district_cases_df)

# Adding a Total column for all Berlin
historic_district_cases_df['All Berlin'] = historic_district_cases_df.sum(axis=1)
st.write(historic_district_cases_df)

# Convert 'Datum' Column to datetime pandas format
historic_district_cases_df['Datum'] = pd.to_datetime(historic_district_cases_df['Datum'])

# Defining a list with the districts of Berlin and a list with the corresponding populations
districts = ['Lichtenberg', 'All Berlin', 'Mitte', 'Charlottenburg-Wilmersdorf', 'Friedrichshain-Kreuzberg', 'Neukoelln', 'Tempelhof-Schoeneberg', 'Pankow', 'Reinickendorf', 'Steglitz-Zehlendorf', 'Spandau', 'Marzahn-Hellersdorf', 'Treptow-Koepenick']
populations = [2.91452, 37.54418, 3.84172, 3.42332, 2.89762, 3.29691, 3.51644, 4.07765, 2.65225, 3.08697, 2.43977, 2.68548, 2.71153]

# Creating a pandas DataFrame with the populations of the districts
pop_dict = {'Bezirk': districts, 'Population': populations}
pop_df = pd.DataFrame(data=pop_dict)
st.write(pop_df)

# Sidebar for User Input
selected_districts = st.sidebar.multiselect('Select District(s):', districts, default=['Lichtenberg'])
if selected_districts == []:
    selected_districts = ['All Berlin']

days_to_show = st.sidebar.slider('Number of days to display:', 0, 365, 30)

st.sidebar.write('---')
st.sidebar.write('Chart Theme Settings:')
nocyber = st.sidebar.checkbox('Light Style')

# Manipulating Data based on User Input
data_to_plot = historic_district_cases_df.copy()

for i in selected_districts:
    seven_day_average = historic_district_cases_df[i].rolling(window=7).mean()
    new_col_name = i + ' 7-day Average'
    data_to_plot[new_col_name] = seven_day_average

# Plotting Data
fig, ax = plt.subplots(figsize=(10, 6))

for i in selected_districts:
    sns.lineplot(data=data_to_plot, x=data_to_plot['Datum'], y=i, ax=ax)

    if nocyber:
        plt.style.use('default')
    else:
        plt.style.use('cyberpunk')

plt.legend(selected_districts)
plt.xlabel('Date')
plt.ylabel('New Reported Cases')
plt.xticks(rotation=45)
plt.title('COVID-19 Cases in Berlin')
plt.tight_layout()

st.pyplot(fig)
