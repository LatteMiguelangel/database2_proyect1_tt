import streamlit as st
import pandas as pd
from database_scripts.pipelines import products_bucket_by_price_by_subcategory

def show():
    st.title("Products Report")
    st.write("Analyze product prices by sub-category.")

    if st.button("Compute buckets"):
        buckets = products_bucket_by_price_by_subcategory()
        df = pd.DataFrame(buckets)
        st.dataframe(df)
        if not df.empty:
            st.bar_chart(df.set_index("subCategory")[["counts"]].applymap(lambda x: x.get("high", 0)))
