# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
# snow park import function to import specific column

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the Fruits in your Custom Smootie!
    """
)



name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be', name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect('Choose upto 5 Ingredients:',my_dataframe,max_selections=5)

if ingredients_list:
    

    ingredients_string=''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
        st.subheader(each_fruit + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon" + each_fruit)
        fv_df = st.dataframe(data=fruityvice_response.json())
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fv_df = st.dataframe(data=fruityvice_response.json())
