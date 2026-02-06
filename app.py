import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Traffic Volume Dashboard", layout="wide")

st.title("🚦 Metro Interstate Traffic Volume Dashboard")
st.markdown("""
This interactive dashboard analyzes traffic volume patterns based on
time and weather conditions using the Metro Interstate Traffic dataset.
""")

@st.cache_data
def load_data():
    df = pd.read_csv("Metro_Interstate_Traffic_Volume.csv")
    df['date_time'] = pd.to_datetime(df['date_time'])
    df['year'] = df['date_time'].dt.year
    df['month'] = df['date_time'].dt.month
    df['hour'] = df['date_time'].dt.hour
    df['day_of_week'] = df['date_time'].dt.day_name()
    df['is_weekend'] = df['day_of_week'].isin(['Saturday','Sunday'])
    return df

df = load_data()

st.sidebar.header("🔎 Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df['year'].unique())
)

weather = st.sidebar.multiselect(
    "Select Weather Condition",
    df['weather_main'].unique(),
    default=df['weather_main'].unique()
)

filtered_df = df[
    (df['year'] == year) &
    (df['weather_main'].isin(weather))
]
st.subheader("⏰ Average Traffic Volume by Hour")

hourly = filtered_df.groupby('hour')['traffic_volume'].mean()

fig, ax = plt.subplots()
hourly.plot(ax=ax)
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Traffic Volume")
st.pyplot(fig)

st.subheader("📆 Weekday vs Weekend Traffic")

weekend_avg = filtered_df.groupby('is_weekend')['traffic_volume'].mean()

fig, ax = plt.subplots()
weekend_avg.plot(kind='bar', ax=ax)
ax.set_xticks([0,1])
ax.set_xticklabels(['Weekday','Weekend'], rotation=0)
ax.set_ylabel("Traffic Volume")
st.pyplot(fig)

st.subheader("📈 Monthly Traffic Trend")

monthly = filtered_df.groupby('month')['traffic_volume'].mean()

fig, ax = plt.subplots()
monthly.plot(ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Traffic Volume")
st.pyplot(fig)

st.subheader("🌦 Traffic Volume by Weather Condition")

weather_avg = (
    filtered_df
    .groupby('weather_main')['traffic_volume']
    .mean()
    .sort_values()
)

fig, ax = plt.subplots()
weather_avg.plot(kind='barh', ax=ax)
ax.set_xlabel("Traffic Volume")
st.pyplot(fig)

st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head(50))

st.subheader("🧠 Key Insights")

st.markdown("""
- Traffic volume peaks during morning and evening rush hours.
- Weekday traffic is consistently higher than weekend traffic.
- Clear weather conditions are associated with higher traffic volume.
- Temporal variables have a stronger influence on traffic than weather variables.
""")


