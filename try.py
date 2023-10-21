import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

# Define the data and column definitions
data = [
    {"id": 1, "username": "John", "email": "john@example.com"},
    {"id": 2, "username": "Alice", "email": "alice@example.com"},
    {"id": 3, "username": "Bob", "email": "bob@example.com"},
    {"id": 4, "username": "Emily", "email": "emily@example.com"},
]

column_defs = [
    {"field": "id", "checkboxSelection": True},
    {"field": "username"},
    {"field": "email"},
]

# Build the GridOptions
gob = GridOptionsBuilder()
gob.configure_pagination(enabled=True, paginationAutoPageSize=True, paginationPageSize=10)
gob.configure_selection(selection_mode  = 'multiple', use_checkbox = False, pre_selected_rows = [])
gob.set_column_defs(column_defs)
gob.set_default_col_def(flex=1)

grid_options = gob.build()

# Create the Ag Grid
with st.expander("Ag Grid"):
    AgGrid(data, gridOptions=grid_options)