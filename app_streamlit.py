import streamlit as st
import pandas as pd
from database_scripts.pipelines import (
    orders_sales_by_category_month,
    customers_top_by_orders,
    customer_top_by_orders_in_range,
    products_bucket_by_price_by_subcategory,
)

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("Sales Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start date", value=pd.to_datetime("2012-01-01"))
end_date = st.sidebar.date_input("End date", value=pd.to_datetime("2012-12-31"))
top_n = st.sidebar.number_input("Top N customers", min_value=1, max_value=100, value=10)

# Sales by category and month
st.header("Sales by Category and Month")
if st.button("Run sales report"):
    results = orders_sales_by_category_month(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    df = pd.DataFrame(results)
    if not df.empty:
        st.dataframe(df)
        pivot = df.pivot_table(index="month", columns="category", values="totalSales", aggfunc="sum").fillna(0)
        st.line_chart(pivot)
    else:
        st.info("No results for the selected date range")

# Top customers
st.header("Top Customers")
if st.button("Show top customers"):
    top = customers_top_by_orders(limit=top_n)
    df_top = pd.DataFrame(top)
    st.dataframe(df_top)

# Top customer in range
st.header("Top Customer in Date Range")
if st.button("Top customer in date range"):
    top_customer = customer_top_by_orders_in_range(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    if top_customer:
        st.metric("Customer", top_customer.get("customerName") or top_customer.get("customerId"))
        st.write(top_customer)
    else:
        st.info("No orders in the selected range")

# Price buckets by sub-category
st.header("Price Buckets by Sub-Category")
if st.button("Compute buckets"):
    buckets = products_bucket_by_price_by_subcategory()
    st.write(buckets)
