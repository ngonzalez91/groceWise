import streamlit as st
import sqlite3
import pandas as pd

# DB connection
conn = sqlite3.connect("./bills.db")

# Title
st.title("🧾 GroceWise Receipt Insights")

# Tabs or filters
view = st.sidebar.selectbox("Choose a view:", ["All Receipts", "Store Summary", "Item Prices", "Unnormalized Items"])

# Load data
@st.cache_data
def load_data():
    df = pd.read_sql_query("""
        SELECT r.store_name, r.name AS raw_item, r.unit_price, n.canonical_name
        FROM receipts r
        LEFT JOIN item_normalization n ON r.name = n.variant_name
    """, conn)
    return df

df = load_data()

# Views
if view == "All Receipts":
    st.subheader("📋 All Receipt Items")
    st.dataframe(df)

elif view == "Store Summary":
    st.subheader("🏪 Total Spend Per Store")
    summary = df.groupby("store_name")["unit_price"].sum().reset_index()
    st.bar_chart(summary.set_index("store_name"))

elif view == "Item Prices":
    st.subheader("📊 Price Distribution by Item")
    canonical_items = df["canonical_name"].dropna().unique()
    item = st.selectbox("Choose item:", sorted(canonical_items))
    item_df = df[df["canonical_name"] == item]
    st.dataframe(item_df[["store_name", "raw_item", "unit_price"]])
    st.bar_chart(item_df.groupby("store_name")["unit_price"].mean())

elif view == "Unnormalized Items":
    st.subheader("❓ Items Missing Normalization")
    missing = df[df["canonical_name"].isna()]
    st.dataframe(missing)

