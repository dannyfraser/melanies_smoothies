# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your smoothie
  """
)

name_on_order = st.text_input("Name on smoothie:")
st.write(f"The name on your smoothie will be {name_on_order}")

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    ingredients_string = " ".join(ingredients_list)
    st.write(ingredients_string)

    insert_button = st.button("Submit order")
    if insert_button:
    
        sql = f"""
            insert into smoothies.public.orders(ingredients, name_on_order) values ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(sql).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
