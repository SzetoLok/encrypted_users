
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
import numpy as np
import requests
import json
import mysql.connector
from aes_cipher import encrypt, decrypt
import pandas as pd
import datetime
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.write("DB username:", st.secrets["db_username"])
# with open('../config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)
# # hashed_passwords = stauth.Hasher(['abc', 'def']).generate()
# # print(hashed_passwords)
# authenticator = Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )
st.title("User Logs Extractor")
st.divider()
st.subheader("Select date and time")

#Date and time
col1, col2 = st.columns((1,1))
with col1:
    first_date = st.date_input("Start date",None ,None ,datetime.datetime.now())
    first_date_time = st.time_input('Start time', datetime.time(8, 45))

with col2:
    end_date = st.date_input("End date",None ,first_date,datetime.datetime.now())
    end_date_time = st.time_input('End time', datetime.time(8, 45))

first_day_result = first_date.strftime("%m/%d/%Y")+"T"+first_date_time.strftime("%H:%M:%S")+"Z"
end_day_result = end_date.strftime("%m/%d/%Y")+"T"+end_date_time.strftime("%H:%M:%S")+"Z"
# print('first: '+first_day_result)  
# print('end: '+end_day_result)
st.divider()

def main():
    st.subheader("Select Product")

# on the first run add variables to track in state
    if "all_option" not in st.session_state:
        st.session_state.all_option = True
        st.session_state.selected_options = ['MarketEye', 'GekkoSearch', 'GekkoGraph']

    def check_change():
    # this runs BEFORE the rest of the script when a change is detected 
    # from your checkbox to set selectbox
        if st.session_state.all_option:
            st.session_state.selected_options = ['MarketEye', 'GekkoSearch', 'GekkoGraph']
        else:
            st.session_state.selected_options = []
        return

    def multi_change():
    # this runs BEFORE the rest of the script when a change is detected
    # from your selectbox to set checkbox
        if len(st.session_state.selected_options) == 3:
         st.session_state.all_option = True
        else:
         st.session_state.all_option = False
        return

    selected_options = st.multiselect("Select one or more options:",
         ['MarketEye', 'GekkoSearch', 'GekkoGraph'],key="selected_options", on_change=multi_change)
    print(selected_options)

    all = st.checkbox("Select all", key='all_option',on_change= check_change)
    st.divider()

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="xx135367dra",
    database="gekko_users",
    )
    mycursor=mydb.cursor(buffered=True)
    
    # TODO_1: ... search and filter user objects
    # Define the filter criteria
    if 'filter' not in st.session_state:
        st.session_state.filter= ""
    keywords = st.session_state.filter.replace(" ","")
    command ="Select * from CLIENT1 WHERE email NOT LIKE '%old%'"
    if len(keywords) == 0:
        mycursor.execute(command)
    else:
        keywords = '%'+keywords+'%'
        command +="and email LIKE %s ;"
        mycursor.execute(command,(keywords, ))

    print(command, keywords)
    
    email, page = st.columns((4,1))
    with email:
        st.text_input("Email filter", key="filter") 
    with page:
        a=st.number_input('Item Per Page', min_value=1, value=10, step=1)

    # Create the table with filtered items
    mysql_users =[]
    for x in mycursor:
        mysql_users.append( {
            "id": x[0],
            'username': x[2],  
            'email': x[3] 
        })
    # mycursor.execute("Show tables")
    
    df_mysql_users= pd.DataFrame(mysql_users)
    gridoptions = GridOptionsBuilder.from_dataframe(df_mysql_users)
    gridoptions.configure_selection(selection_mode='multiple', use_checkbox=True, pre_selected_rows=mysql_users)
    gridoptions.configure_default_column(flex=1)
    gridoptions.configure_column("id", headerCheckboxSelection = True)
    gridoptions.configure_pagination(True,False,a)
    gridoptions.configure_auto_height(autoHeight=True)
    gridOptions = gridoptions.build()

    sql_grid_response = AgGrid(
    df_mysql_users,
    gridOptions=gridOptions,
    allow_unsafe_jscode=True,
    )

    mysql_usernames = sql_grid_response['selected_rows']
    print()

    # encrypt the usernames and format the results into a desire output format
    mysql_shoulds=[]
    # print('Selected usernames:', mysql_usernames)
    if len(mysql_usernames)>0:
        for item in mysql_usernames:
            mysql_shoulds.append({
            "match_phrase": {
                "uid": encrypt(item['username']),
                "decryped": decrypt(encrypt(item['username']))
            }
        })
    # print("final result:")
    # print(json.dumps(mysql_shoulds, indent=2))

    print()
    # Download button
    str='index' + df_mysql_users.to_csv()
    st.download_button("Download CSV",
                    str.encode('utf-8'),
                    file_name= 'output_table',
                    mime= 'text/csv')
 
    if mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("MySQL connection is closed")

if __name__ == '__main__':
    main()
