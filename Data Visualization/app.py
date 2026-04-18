import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Data Dashboard")

# Load data
df = pd.read_csv("sales_data.csv", encoding='latin1', low_memory=False)

# Clean columns
df.columns = df.columns.str.strip().str.lower()

st.write("Columns:", df.columns)

# 🔥 MANUAL FIX (based on your dataset)
date_col = 'orderdate' if 'orderdate' in df.columns else None
sales_col = 'sales' if 'sales' in df.columns else None
region_col = 'country' if 'country' in df.columns else None
category_col = 'dealsize' if 'dealsize' in df.columns else None
product_col = 'productline' if 'productline' in df.columns else None

# Convert date
if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

# Sidebar filters
st.sidebar.header("🔍 Filters")

if category_col:
    category = st.sidebar.multiselect(
        "Select Category",
        df[category_col].dropna().unique(),
        default=df[category_col].dropna().unique()
    )
else:
    category = None

if region_col:
    region = st.sidebar.multiselect(
        "Select Region",
        df[region_col].dropna().unique(),
        default=df[region_col].dropna().unique()
    )
else:
    region = None

# Apply filters
filtered_df = df.copy()

if category_col and category:
    filtered_df = filtered_df[filtered_df[category_col].isin(category)]

if region_col and region:
    filtered_df = filtered_df[filtered_df[region_col].isin(region)]

# KPIs
if sales_col:
    total_sales = filtered_df[sales_col].sum()
else:
    total_sales = 0

st.metric("💰 Total Sales", f"{total_sales:,.0f}")
st.metric("📦 Total Orders", filtered_df.shape[0])

# Charts
if category_col and sales_col:
    st.subheader("📊 Sales by Category")
    fig1, ax1 = plt.subplots()
    sns.barplot(x=category_col, y=sales_col, data=filtered_df, estimator=sum, ax=ax1)
    plt.xticks(rotation=30)
    st.pyplot(fig1)

if region_col and sales_col:
    st.subheader("🥧 Sales by Region")
    fig2, ax2 = plt.subplots()
    filtered_df.groupby(region_col)[sales_col].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax2)
    st.pyplot(fig2)

if date_col and sales_col:
    st.subheader("📈 Sales Trend")
    trend = filtered_df.groupby(date_col)[sales_col].sum()
    fig3, ax3 = plt.subplots()
    trend.plot(ax=ax3)
    st.pyplot(fig3)

if product_col and sales_col:
    st.subheader("🏆 Top Products")
    top_products = filtered_df.groupby(product_col)[sales_col].sum().nlargest(5)
    st.bar_chart(top_products)

st.write("✨ Created by Divyabharathi")