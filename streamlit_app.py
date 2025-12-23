# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f"Customize your Smoothie! :cup_with_straw:")
st.write(
  """Choose the  fruits you want in your custom Smoothie!""")

name_on = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session \
    .table("smoothies.public.fruit_options") \
    .select(col("FRUIT_NAME"),col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
fruitop_pd = my_dataframe.to_pandas()

ingridients_list = st.multiselect(
    "Choose up to 5 ingridients"
    ,my_dataframe
    ,max_selections=5
    ,key="st_ingredients_list")

def clear_ingredients(sql_stmt,ord_name):
    # Safe: modifying the widget's key inside a callback
    session.sql(sql_stmt).collect()
    st.success(f'Your Smoothie is ordered, {ord_name}!', icon="✅")
    st.session_state.st_ingredients_list = []
    ingridients_list = []

if ingridients_list:
    #st.write(ingridients_list)
    ingredients_string = ' '.join(ingridients_list)
    #st.write(ingredients_string)

    for eachFruit in ingridients_list:
      search_on=pd_df.loc[fruitop_pd['FRUIT_NAME'] == eachFruit, 'SEARCH_ON'].iloc[0]
      #st.write('The search value for ', eachFruit,' is ', search_on, '.')
      smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
      #st.text(smoothiefroot_response)
      api_response_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on + """');"""

    #st.write(my_insert_stmt)
    #st.stop()

    submit_btn = st.button(
        "Submit Order!"
        ,on_click=clear_ingredients
        ,args=(my_insert_stmt,name_on)
    )
    #if submit_btn:
        #session.sql(my_insert_stmt).collect()
        #st.success(f'Your Smoothie is ordered, {name_on}!', icon="✅")
