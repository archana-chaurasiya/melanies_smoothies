# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothies :cup_with_straw:")
# st.write("Choose the Fruits you want in your custom smoothie !")


st.write("Choose the fruit you want in your custom smoothies!")


cnx = st.connection('snowflake')
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
#Convert the snowpark dataframe to pandas dataframe so we can use loc function
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

name_on_order = st.text_input("Name on Smoothies", "")
st.write("Name on Your Smoothie will be: ", name_on_order)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ', 
    my_dataframe,
    max_selections=5
    )

ingredients_string = ''

if ingredients_list:
   
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen +' ' 

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_choosen,' is ', search_on, '.')

        # smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        if search_on :
            st.subheader(fruit_choosen + " Nutrition Information")
        
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        
#st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

#st.write(my_insert_stmt)
#st.stop()
time_to_insert = st.button('Submit Order')

if time_to_insert and ingredients_string:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, ' + name_on_order+'!', icon="✅")



#st.text(smoothiefroot_response.json())


