import streamlit as st
from views import home_view, orders_view, customers_view, products_view

st.set_page_config(page_title="Sales Dashboard", layout="wide")

PAGES = {
    "Home": home_view,
    "Orders Report": orders_view,
    "Customers Report": customers_view,
    "Products Report": products_view,
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page.show()
