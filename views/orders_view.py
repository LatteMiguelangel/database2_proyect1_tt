import streamlit as st
import pandas as pd
from database_scripts.pipelines import orders_sales_by_category_month

def show():
    st.title("Orders Report")
    st.write("Analyze sales by category and month.")

    start_date = st.date_input("Start date", value=pd.to_datetime("2012-01-01"))
    end_date = st.date_input("End date", value=pd.to_datetime("2012-12-31"))

    if st.button("Run report"):
        results = orders_sales_by_category_month(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        df = pd.DataFrame(results)
        if not df.empty:
            st.dataframe(df)
            pivot = df.pivot_table(index="month", columns="category", values="totalSales", aggfunc="sum").fillna(0)
            st.line_chart(pivot)
        else:
            st.info("No results for the selected date range.")