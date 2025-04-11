import streamlit as st
import pandas as pd
import sqlite3

# Connect with SQL database
conn = sqlite3.connect('data/mercadolivre.db')

# Load into dataframe using sql
df = pd.read_sql_query("SELECT * FROM notebook", conn)

# Close connection
conn.close()

# Add tittle
st.title('📊 Market Research - Notebooks from Mercado Livre')

# KPI
st.subheader('💡 KPIs ')
col1, col2, col3 = st.columns(3)

# KPI 1: Total of itens
total_itens = df.shape[0]
col1.metric(label="🖥️ Total Notebooks Number", value=total_itens)

# KPI 2: Unique Brands
unique_brands = df['brand'].nunique()
col2.metric(label="🏷️ Unique Brands", value=unique_brands)

# KPI 3: Average price
average_new_price = df['new_money'].mean()
col3.metric(label="💰 Average Price (R$)", value=f"{average_new_price:.2f}")

# Most frequent brands
st.subheader('🏆 Most frequent brands until page 20º')
col1, col2 = st.columns([4, 2])
top_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_brands)
col2.write(top_brands)

# Average price by brand
st.subheader('💵 Average price by brand')
col1, col2 = st.columns([4, 2])
df_non_zero_prices = df[df['new_money'] > 0]
average_price_by_brand = df_non_zero_prices.groupby('brand')['new_money'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

# Average ratings by brand
st.subheader('⭐ Average ratings by brand')
col1, col2 = st.columns([4, 2])
df_non_zero_reviews = df[df['reviews_rating_number'] > 0]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)