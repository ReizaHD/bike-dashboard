import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_casual_df = df.resample(rule='D', on='dteday').agg({
    "instant": "nunique",
    "casual": "sum",
    "registered":"sum"
    })
    daily_casual_df.index = daily_casual_df.index.strftime('%A')
    daily_casual_df = daily_casual_df.reset_index()

    new_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_casual_df_grouped = daily_casual_df.groupby(by="dteday").sum().reindex(new_order)
    return daily_casual_df
    
def creat_hourly_order_df(df):
    hourly_df_grouped = df.groupby(by="hr").agg({
    "instant" : "nunique",
    "casual":"sum",
    "registered":"sum",
    "cnt":"sum"
    })
    return hourly_df_grouped
    
def creat_monthly_order_df():
    monthly_casual_df = all_df.resample(rule='M', on='dteday').agg({
    "instant": "nunique",
    "casual": "sum"
    })
    monthly_casual_df.index = monthly_casual_df.index.strftime('%B')
    monthly_casual_df = monthly_casual_df.reset_index()


    monthly_casual_df.rename(columns={
        "dteday": "Month",
        "casual": "Casual Total"
    }, inplace=True)
    df_casual1 = monthly_casual_df.loc[:12]
    df_casual2 = monthly_casual_df.loc[12:]
    
    monthly_registered_df = day_df.resample(rule='M', on='dteday').agg({
    "instant": "nunique",
    "registered": "sum"
    })
    monthly_registered_df.index = monthly_registered_df.index.strftime('%B')
    monthly_registered_df = monthly_registered_df.reset_index()


    monthly_registered_df.rename(columns={
        "dteday": "Month",
        "registered": "Registered Total"
    }, inplace=True)
    df_registered1 = monthly_registered_df.loc[:12]
    df_registered2 = monthly_registered_df.loc[12:]
    
    return df_casual1, df_casual2, df_registered1, df_registered2
    
def create_holiday_df():
    holiday_casual_df = main_df.groupby(by="holiday").agg({
    "instant": "nunique",
    "casual": "mean",
    })
    holiday_casual_df.index = holiday_casual_df.index.map({0: "No", 1: "Yes"})
    
    holiday_registered_df = main_df.groupby(by="holiday").agg({
    "instant": "nunique",
    "registered": "mean",
    })
    holiday_registered_df.index = holiday_registered_df.index.map({0: "No", 1: "Yes"})
    
    return holiday_casual_df, holiday_registered_df

day_df = pd.read_csv("bike_sharing_dataset/day.csv")
all_df = pd.read_csv("bike_sharing_dataset/hour.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://www.shutterstock.com/image-vector/bike-icon-vector-logo-template-600nw-1388480312.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]
                
main_day_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]
                
daily_orders_df = create_daily_orders_df(main_df)

st.header('Bike Renting Dashboard :sparkles:')

st.subheader("Statistics of All Bike Renting data")
st.write(all_df[['casual','registered','cnt']].describe(include='all'))

col1_1, col2_1 = st.columns(2)

with col1_1:
    total_orders = all_df.casual.sum()
    st.metric("Total Casual Renters", value=total_orders)
    
with col2_1:
    total_orders = all_df.registered.sum()
    st.metric("Total Registered Renters", value=total_orders)

st.metric("Total of the Two Renters",value=all_df.cnt.sum())

st.subheader("Number of Renters per Month (2011-2012)")

df_casual1, df_casual2, df_registered1, df_registered2 = creat_monthly_order_df()

plt.figure(figsize=(15, 7)) 
plt.plot(df_casual1["Month"], df_casual1["Casual Total"], marker='o', linewidth=2, color="#72BCD4", label="Tahun 2011") 
plt.plot(df_casual2["Month"], df_casual2["Casual Total"], marker='o', linewidth=2, color="red", label="Tahun 2012")
plt.title("Number of Casual Renters", loc="center", fontsize=20)
plt.legend(['Tahun 2011', 'Tahun 2012']) 
plt.xticks(fontsize=10) 
plt.yticks(fontsize=10) 
st.pyplot(plt)

plt.figure(figsize=(15, 7)) 
plt.plot(df_registered1["Month"], df_registered1["Registered Total"], marker='o', linewidth=2, color="#72BCD4", label="Tahun 2011") 
plt.plot(df_registered2["Month"], df_registered2["Registered Total"], marker='o', linewidth=2, color="red", label="Tahun 2012")
plt.title("Number of Registered Renters", loc="center", fontsize=20)
plt.legend(['Tahun 2011', 'Tahun 2012'])
plt.xticks(fontsize=10) 
plt.yticks(fontsize=10) 
st.pyplot(plt)

st.subheader('Daily Renters')

col1_2, col2_2 = st.columns(2)

with col1_2:
    total_orders = daily_orders_df.casual.sum()
    st.metric("Total Casual Renters", value=total_orders)
    
with col2_2:
    total_orders = daily_orders_df.registered.sum()
    st.metric("Total Registered Renters", value=total_orders)
    
st.write()
    
col1_3, col2_3, col3_3 = st.columns(3)

with col1_3:
    total_orders = main_day_df.cnt.mean()
    st.metric("Average of Renters", value=round(total_orders+1.0))
    
with col2_3:
    total_orders = main_day_df.cnt.min()
    st.metric("Min of Renters", value=total_orders)
    
with col3_3:
    total_orders = main_day_df.cnt.max()
    st.metric("Max of Renters", value=total_orders)
st.subheader("Number of Daily Renters")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 15))
 
 
sns.barplot(x="dteday", y="casual", data=daily_orders_df, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("", fontsize=30)
ax[0].set_title("Number of Casual Renters", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="dteday", y="registered", data=daily_orders_df, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Number of Registered Renters", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

 
st.pyplot(fig)

st.subheader("Number of Renters Hourly")

hourly_df_grouped = creat_hourly_order_df(main_df)

plt.figure(figsize=(10, 6))
plt.bar(hourly_df_grouped.index, hourly_df_grouped['casual'], color='blue', alpha=0.5, width=0.4)
plt.bar(hourly_df_grouped.index, hourly_df_grouped['registered'], color='green', alpha=0.5, width=0.4)
plt.xlabel('Hour')
plt.ylabel('Total')
plt.title('Number of Renters Hourly')
plt.legend(['Casual', 'Registered'])
st.pyplot(plt)

holiday_casual_df, holiday_registered_df = create_holiday_df()

st.subheader("Average of Renters on Holiday")
if main_df.holiday.nunique() < 2:
    st.write("Tidak ada hari libur dalam jangka waktu yang dipilih")
else:
    plt.figure(figsize=(10, 5))
    sns.barplot(
        y="casual", 
        x="holiday",
        data=holiday_casual_df
    )
    plt.title("Average of Casual Renters on Holiday", loc="center", fontsize=15)
    plt.ylabel(None)
    st.pyplot(plt)
    
    plt.figure(figsize=(10, 5))
    sns.barplot(
        y="registered", 
        x="holiday",
        data=holiday_registered_df
    )
    plt.title("Average of Registered Renters on Holiday", loc="center", fontsize=15)
    plt.ylabel(None)
    st.pyplot(plt)