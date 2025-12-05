import streamlit as st
import pandas as pd
from database_scripts.pipelines import customers_top_by_orders, customer_top_by_orders_in_range

def show():
    st.title("Customers Report")
    st.write("Explore top customers and their orders.")

    top_n = st.number_input("Top N customers", min_value=1, max_value=100, value=10)
    if st.button("Show top customers"):
        top = customers_top_by_orders(limit=top_n)
        st.dataframe(pd.DataFrame(top))

    st.subheader("Top customer in date range")
    start_date = st.date_input("Start date", value=pd.to_datetime("2012-01-01"))
    end_date = st.date_input("End date", value=pd.to_datetime("2012-12-31"))
    if st.button("Find top customer in range"):
        top_customer = customer_top_by_orders_in_range(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        if top_customer:
            st.metric("Customer", top_customer.get("customerName") or top_customer.get("customerId"))
            st.write(top_customer)
        else:
            st.info("No orders in the selected range.")
