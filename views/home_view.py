import streamlit as st

def show():
    st.title("Welcome to the Sales Dashboard")
    st.write("""
    This project demonstrates how to use MongoDB Atlas with Python and Streamlit
    to analyze sales data. You can explore reports for Orders, Customers, and Products.
    """)
    st.info("Use the sidebar to navigate between pages.")
