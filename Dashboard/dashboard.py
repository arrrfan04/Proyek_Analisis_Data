import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_season_orders_df(df):
    season_orders_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "season": "sum"
    })
    season_orders_df = season_orders_df.reset_index()
    season_orders_df.rename(columns={
        "instant": "season",
    }, inplace=True)

    return season_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("season").quantity_x.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_weather_orders_df(df):
    weather_orders_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "weathersit": "sum"
    })
    weather_orders_df = weather_orders_df.reset_index()
    weather_orders_df.rename(columns={
        "instant": "weathersit",
    }, inplace=True)

    return weather_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("weathersit").quantity_x.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df


# Load cleaned data
all_df = pd.read_csv("https://raw.githubusercontent.com/arrrfan04/Proyek_Analisis_Data/main/Dashboard/main_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) &
               (all_df["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
season_orders_df = create_season_orders_df(main_df)

# plot number of daily orders (2011-2012)
st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Season Orders')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    season_orders_df["dteday"],
    season_orders_df["season"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

weather_orders_df = create_weather_orders_df(main_df)

st.subheader('Weather Orders')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    weather_orders_df["dteday"],
    weather_orders_df["weathersit"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.caption('Copyright (c) Dicoding 2023')
