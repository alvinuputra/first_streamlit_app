import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocker Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

df = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
df.set_index('Fruit', inplace = True)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(df.index),['Avocado','Strawberries'])
fruits_to_show = df.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    fruityvice_normalized = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

streamlit.header("The fruit load list contains:")
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.dataframe(get_fruit_load_list())

fruit_choice2 = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', fruit_choice2)
