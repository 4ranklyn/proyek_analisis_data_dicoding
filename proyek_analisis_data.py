# -*- coding: utf-8 -*-

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


hour_df = pd.read_csv('https://raw.githubusercontent.com/4ranklyn/proyek_analisis_data_dicoding/refs/heads/main/data/hour.csv')
day_df = pd.read_csv('https://raw.githubusercontent.com/4ranklyn/proyek_analisis_data_dicoding/refs/heads/main/data/day.csv')


min_temp = -8
max_temp = 39
hour_df['temp'] = min_temp + (max_temp - min_temp) * hour_df['temp']
day_df['temp'] = min_temp + (max_temp - min_temp) * day_df['temp']

min_atemp = -16
max_atemp = 50
hour_df['atemp'] = min_atemp + (max_atemp - min_atemp) * hour_df['atemp']
day_df['atemp'] = min_atemp + (max_atemp - min_atemp) * day_df['atemp']

hour_df['hum'] = 100 * hour_df['hum']
day_df['hum'] = 100 * day_df['hum']
hour_df['windspeed'] = 67 * hour_df['windspeed']
day_df['windspeed'] = 67 * day_df['windspeed']

hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

year_mapping = {0: 2011, 1: 2012}

hour_df['yr'] = hour_df['yr'].map(year_mapping)
day_df['yr'] = day_df['yr'].map(year_mapping)


yearly_monthly_user_totals = day_df.groupby(['yr', 'mnth'])['cnt'].sum().unstack()

yearly_monthly_user_totals.plot(kind='bar', stacked=False)


casual_count = day_df['casual'].sum()
registered_count = day_df['registered'].sum()
total_count = day_df['cnt'].sum()


labels = ['Casual Users', 'Registered Users']
sizes = [casual_count, registered_count]
colors = ['#ff9999','#66b3ff']
explode = (0.1, 0)


monthly_changes = day_df.groupby(['yr', 'mnth'])[['temp', 'atemp', 'hum', 'windspeed']].mean()

monthly_changes_2011 = monthly_changes.loc[2011]
monthly_changes_2012 = monthly_changes.loc[2012]

average_user_per_hour = hour_df.groupby('hr')['cnt'].mean()

average_hourly_conditions = hour_df.groupby('hr')[['hum', 'temp', 'atemp', 'windspeed']].mean()

st.header('Bike Sharing Dashboard')

st.subheader('Total Users by Year and Month')
st.bar_chart(yearly_monthly_user_totals)
st.write(f"There are about {total_count} users who share bikes across 2011 and 2012.")


st.subheader('User Distribution: Casual vs Registered')


fig, ax = plt.subplots()
ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Distribution of Casual Users vs Registered Users')

st.pyplot(fig)
st.write(f"From {total_count} users, there are {registered_count} registered users. The rest are casual ones")

st.subheader('Monthly Temperature, Feels Like Temperature, Humidity, and Windspeed')


fig, ax = plt.subplots()
ax.plot(monthly_changes_2011.index, monthly_changes_2011['temp'], label='Temperature')
ax.plot(monthly_changes_2011.index, monthly_changes_2011['atemp'], label='Feels Like Temperature')
ax.plot(monthly_changes_2011.index, monthly_changes_2011['hum'], label='Humidity')
ax.plot(monthly_changes_2011.index, monthly_changes_2011['windspeed'], label='Windspeed')
ax.set_title('Monthly Temperature, Feels Like Temperature, Humidity, and Windspeed (2011)')
ax.set_xlabel('Month')
ax.set_ylabel('Temperature')
ax.legend()
st.pyplot(fig)


fig, ax = plt.subplots()
ax.plot(monthly_changes_2011.index, monthly_changes_2012['temp'], label='Temperature')
ax.plot(monthly_changes_2011.index, monthly_changes_2012['atemp'], label='Feels Like Temperature')
ax.plot(monthly_changes_2011.index, monthly_changes_2012['hum'], label='Humidity')
ax.plot(monthly_changes_2011.index, monthly_changes_2012['windspeed'], label='Windspeed')
ax.set_title('Monthly Temperature, Feels Like Temperature, Humidity, and Windspeed (2012)')
ax.set_xlabel('Month')
ax.set_ylabel('Temperature')
ax.legend()
st.pyplot(fig)


st.subheader('Average User Count per Hour')
st.line_chart(average_user_per_hour)
st.write("Most users use the service around 8 AM and 5 PM.")

st.subheader('Average Hourly Conditions')
st.line_chart(average_hourly_conditions)

st.write("Summary: The busiest months were September 2011 and September 2012, possibly due to favorable weather. Rush hour appears to be around 8 AM and 5 PM, when people commute to work or school.  Comfortable temperature and humidity levels appear to contribute to higher user counts. ")
