import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard",page_icon='🌏',layout='wide')
st.subheader("💨 Air Quality Analysis")
st.markdown("##")

# Membaca data
s1 = pd.read_csv("Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Aotizhongxin_20130301-20170228.csv")
s2 = pd.read_csv("Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Changping_20130301-20170228.csv")
s3 = pd.read_csv("Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Dingling_20130301-20170228.csv")
s4 = pd.read_csv("Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Dongsi_20130301-20170228.csv")
s5 = pd.read_csv("Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Guanyuan_20130301-20170228.csv")
s6 = pd.read_csv("Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Gucheng_20130301-20170228.csv")
s7 = pd.read_csv("Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Huairou_20130301-20170228.csv")
s8 = pd.read_csv("Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Nongzhanguan_20130301-20170228.csv")
s9 = pd.read_csv("Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Shunyi_20130301-20170228.csv")
s10 = pd.read_csv("Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Tiantan_20130301-20170228.csv")
s11 = pd.read_csv("Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Wanliu_20130301-20170228.csv")
s12 = pd.read_csv("Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Wanshouxigong_20130301-20170228.csv")
df = pd.concat([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12])
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day','hour']])
df = df.drop(columns=['year', 'month', 'day', 'hour'])


st.sidebar.image("logo.webp",caption="Air Quality Monitoring")

st.markdown(
    """
    <style>
    .css-1d391kg {
        background-color: #0083B8; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("Please Filter Here")
station = st.sidebar.multiselect(
    "Select Stasiun",
    options = df["station"].unique(),
    default = df["station"].unique()
)
wind = st.sidebar.multiselect(
    "Select Wind Direction",
    options = df["wd"].unique(),
    default = df["wd"].unique()
)

df_selection = df[(df["station"].isin(station)) & (df["wd"].isin(wind))]


average_pm2 = round(df_selection["PM2.5"].mean(),1)
average_pm10 = round(df_selection["PM10"].mean(), 1)
average_SO2 = round(df_selection["SO2"].mean(), 1)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Average PM2.5:")
    st.subheader(f"{average_pm2} µg/m³")
with middle_column:
    st.subheader("Average PM10:")
    st.subheader(f"{average_pm10} µg/m³")
with right_column:
    st.subheader("Average SO2:")
    st.subheader(f"{average_SO2} µg/m³")

st.markdown("""---""")

wind_prop = df_selection["wd"].value_counts().reset_index()
wind_prop.columns = ["wd", "count"]

fig_wind_pie = px.pie(
    wind_prop,
    names="wd",
    values="count",
    title="<b>Wind Direction Proportion</b>",
    template="plotly_white"
)

# Display in Streamlit
st.plotly_chart(fig_wind_pie, use_container_width=True)


# CO BY STATION [BAR CHART]
co_by_station = df_selection.groupby(by=["station"])[["CO"]].mean().sort_values(by="CO")
fig_CO = px.bar(
    co_by_station,
    x="CO",
    y=co_by_station.index,
    orientation="h",
    title="<b>CO by station</b>",
    color_discrete_sequence=["#64690c"] * len(co_by_station),
    template="plotly_white",
)
fig_CO.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# temp BY wd [BAR CHART]
temp_by_wd = df_selection.groupby(by=["wd"])[["TEMP"]].mean()
fig_temp = px.bar(
    temp_by_wd,
    x=temp_by_wd.index,
    y="TEMP",
    title="<b>Temperature by Wind Direction</b>",
    color_discrete_sequence=["#64690c"] * len(temp_by_wd),
    template="plotly_white",
)
fig_temp.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_CO, use_container_width=True)
right_column.plotly_chart(fig_temp, use_container_width=True)

st.subheader("PM2.5 and CO Trends in Air Quality")

# Membuat layout dua kolom
col1, col2 = st.columns(2)

# Plot pertama (PM2.5)
fig1, ax1 = plt.subplots(figsize=(10, 6))  
ax1.plot(df_selection['datetime'], df_selection['PM2.5'], color='#f59c00', linewidth=2.5, alpha=0.85)
ax1.set_xlabel('Date', fontsize=12, color='#333333')
ax1.set_ylabel('Concentration (µg/m³)', fontsize=12, color='#333333')
ax1.set_title('PM2.5 Trends Over Time', fontsize=15, fontweight='bold', color='#333333')
ax1.set_facecolor('#f0f0f0')
plt.xticks(rotation=45)

# Menghapus outline
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.grid(False)
plt.tight_layout()

# Tampilkan plot pertama di kolom pertama
with col1:
    st.pyplot(fig1)

# Plot kedua (CO)
fig2, ax2 = plt.subplots(figsize=(14, 8))  
ax2.plot(df['datetime'], df['CO'], color='#f59c00', alpha=0.7)
ax2.set_xlabel('Date', fontsize=12)
ax2.set_ylabel('Concentration (µg/m³)', fontsize=12)
ax2.set_title('CO Trends Over Time', fontsize=14)

# Menghapus outline
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.grid(False)
ax2.set_facecolor('#f0f0f0')
plt.xticks(rotation=45)
ax2.grid(False)
plt.tight_layout()

# Tampilkan plot kedua di kolom kedua
with col2:
    st.pyplot(fig2)

st.subheader("Air quality at various measurement stations")

# Menghitung nilai maksimum untuk PM2.5 dan SO2
max_pm2 = round(df_selection["PM2.5"].max(), 1)
max_so2 = round(df_selection["SO2"].max(), 1)

# Membuat layout dengan 2 kolom
left_column, right_column = st.columns(2)

with left_column:
    st.markdown(f"<h4 style='color:#333333;'>Max PM2.5:</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:24px; color:#e60060;'>{max_pm2} µg/m³</p>", unsafe_allow_html=True)

with right_column:
    st.markdown(f"<h4 style='color:#333333;'>Max SO2:</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:24px; color:#e60060;'>{max_so2} µg/m³</p>", unsafe_allow_html=True)

# Garis pemisah
st.markdown("""---""")


# Hitung rata-rata PM2.5
station_avg_pm25 = df.groupby('station')['PM2.5'].mean()
station_avg_pm25_sorted = station_avg_pm25.sort_values(ascending=False)

# Hitung rata-rata SO2
station_avg_so2 = df.groupby('station')['SO2'].mean()
station_avg_so2_sorted = station_avg_so2.sort_values(ascending=False)

# Membuat layout dua kolom
col1, col2 = st.columns(2)


# Bar Plot untuk PM2.5
fig1, ax1 = plt.subplots(figsize=(14, 8))
ax1.bar(station_avg_pm25_sorted.index, station_avg_pm25_sorted.values, color='#e60060')
ax1.set_xlabel('Station', fontsize=12)
ax1.set_ylabel('Average PM2.5 Concentration (µg/m³)', fontsize=12)
ax1.set_title('Average PM2.5 Concentration by Station', fontsize=14)

# Menghilangkan outline
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
plt.xticks(rotation=45)
plt.tight_layout()

# Tampilkan plot pertama di kolom pertama
with col1:
    st.pyplot(fig1)

# Bar Plot untuk SO2
fig2, ax2 = plt.subplots(figsize=(14, 8))
ax2.bar(station_avg_so2_sorted.index, station_avg_so2_sorted.values, color='#e60060')
ax2.set_xlabel('Station', fontsize=12)
ax2.set_ylabel('Average SO2 Concentration (µg/m³)', fontsize=12)
ax2.set_title('Average SO2 Concentration by Station', fontsize=14)

# Menghilangkan outline
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
plt.xticks(rotation=45)
plt.tight_layout()

# Tampilkan plot kedua di kolom kedua
with col2:
    st.pyplot(fig2)

st.markdown("""---""")

# Menghapus duplikat pada kolom 'TEMP', 'DEWP', dan 'PM2.5' jika ada
df_clean = df.drop_duplicates(subset=['TEMP', 'DEWP', 'PM2.5'])

# Pastikan index unik dengan reset_index
df_clean = df_clean.reset_index(drop=True)

# Membuat scatter plot tanpa outline dan grid untuk 'TEMP' vs 'PM2.5'
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='TEMP', y='PM2.5', data=df_clean, color='#ffcc00', alpha=0.7, ax=ax)
ax.set_title('Relationship between Temperature and PM2.5', fontsize=14, fontweight='bold', color='#333333')
ax.set_xlabel('Temperature (°C)', fontsize=12, color='#333333')
ax.set_ylabel('PM2.5 Concentration (µg/m³)', fontsize=12, color='#333333')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.grid(False)
st.pyplot(fig)

# Membuat scatter plot tanpa outline dan grid untuk 'DEWP' vs 'PM2.5'
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='DEWP', y='PM2.5', data=df_clean, color='#ffcc00', alpha=0.7, ax=ax)
ax.set_title('Relationship between Dew Point and PM2.5', fontsize=14, fontweight='bold', color='#333333')
ax.set_xlabel('Dew Point (°C)', fontsize=12, color='#333333')
ax.set_ylabel('PM2.5 Concentration (µg/m³)', fontsize=12, color='#333333')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.grid(False)
st.pyplot(fig)
