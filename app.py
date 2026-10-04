
import streamlit as st
import pandas as pd
import sqlite3
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_PATH, "pharmeasy.db")

conn = sqlite3.connect(DB_PATH)

orders = pd.read_sql_query("SELECT * FROM orders_clean", conn)
regions = pd.read_sql_query("SELECT * FROM regions_master", conn)

conn.close()

orders["order_date"] = pd.to_datetime(orders["order_date"])

st.title("PharmEasy Regional Pulse Dashboard")

st.subheader("Executive Summary")

st.write("""
The PharmEasy Regional Pulse analysis covers 2,100 distinct orders
from April to June, recording total sales of ₹3,265,191.42 and total
profit of ₹492,279.59. Guntur's sales increased by 122.19% from April
to May before declining in June, while Hyderabad recorded the highest
total sales among the regions. These changes highlight the need to
review regional performance and investigate the factors behind
significant sales movements before deciding on further action.
Use the regional filter, charts, and monthly breakdown below to
explore the results in more detail.
""")

region_list = ["All Regions"] + sorted(orders["region"].unique().tolist())

selected_region = st.selectbox(
    "Select Region",
    region_list
)

if selected_region == "All Regions":
    filtered_orders = orders.copy()
else:
    filtered_orders = orders[
        orders["region"] == selected_region
    ].copy()

total_sales = filtered_orders["sales_inr"].sum()
total_profit = filtered_orders["profit_inr"].sum()
total_orders = filtered_orders["order_id"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Sales (₹)",
    f"₹{total_sales:,.2f}"
)

col2.metric(
    "Total Profit (₹)",
    f"₹{total_profit:,.2f}"
)

col3.metric(
    "Distinct Orders",
    f"{total_orders:,}"
)

st.subheader("Monthly Sales Trend")

monthly_sales = filtered_orders.copy()

monthly_sales["month"] = monthly_sales["order_date"].dt.strftime("%B")

monthly_sales["month"] = pd.Categorical(
    monthly_sales["month"],
    categories=["April", "May", "June"],
    ordered=True
)

monthly_sales = monthly_sales.groupby(
    ["month", "region"],
    observed=False
)["sales_inr"].sum().reset_index()

import plotly.express as px

fig = px.line(
    monthly_sales,
    x="month",
    y="sales_inr",
    color="region",
    markers=True,
    title="Monthly Sales by Region",
    labels={
        "month": "Month",
        "sales_inr": "Sales (₹)",
        "region": "Region"
    }
)

fig.update_layout(
    yaxis=dict(rangemode="tozero")
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Total Sales by Region")

region_sales = filtered_orders.groupby(
    "region"
)["sales_inr"].sum().reset_index()

region_sales = region_sales.sort_values(
    by="sales_inr",
    ascending=False
)

fig2 = px.bar(
    region_sales,
    x="region",
    y="sales_inr",
    title="Total Sales by Region",
    labels={
        "region": "Region",
        "sales_inr": "Sales (₹)"
    },
    color="region"
)

fig2.update_layout(
    yaxis=dict(rangemode="tozero"),
    showlegend=False
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Sales Share by Category")

category_sales = filtered_orders.groupby(
    "category"
)["sales_inr"].sum().reset_index()

fig3 = px.pie(
    category_sales,
    names="category",
    values="sales_inr",
    title="Sales Share by Category",
    hole=0.4
)

fig3.update_traces(
    textinfo="percent+label"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Regional and Monthly Sales Breakdown")

monthly_table = filtered_orders.copy()

monthly_table["month"] = monthly_table["order_date"].dt.strftime("%B")

monthly_table = monthly_table.groupby(
    ["region", "month"]
).agg(
    total_sales=("sales_inr", "sum"),
    total_profit=("profit_inr", "sum"),
    total_orders=("order_id", "nunique")
).reset_index()

monthly_table["month"] = pd.Categorical(
    monthly_table["month"],
    categories=["April", "May", "June"],
    ordered=True
)

monthly_table = monthly_table.sort_values(
    ["region", "month"]
)

st.dataframe(
    monthly_table,
    use_container_width=True,
    hide_index=True
)
