# -*- coding: utf-8 -*-


import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

hour_df = pd.read_csv('https://raw.githubusercontent.com/4ranklyn/proyek_analisis_data_dicoding/refs/heads/main/data/hour.csv')
day_df = pd.read_csv('https://raw.githubusercontent.com/4ranklyn/proyek_analisis_data_dicoding/refs/heads/main/data/day.csv')

st.header('Bike Sharing Dashboard')

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

casual_count = day_df['casual'].sum()
registered_count = day_df['registered'].sum()
total_count = day_df['cnt'].sum()


st.subheader('Total Users by Year and Month')

yearly_monthly_user_totals = day_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()

yearly_monthly_user_totals.plot(kind='bar', stacked=True)

plt.title("Monthly User Usage across 2011 and 2012")
plt.xlabel("Month")
plt.ylabel("Total User Usage (cnt)")
plt.legend(title="Year")
st.pyplot(plt)
st.write(f"There are about {total_count} users who share bikes across 2011 and 2012.")






labels = ['Casual Users', 'Registered Users']
sizes = [casual_count, registered_count]
colors = ['#ff9999','#66b3ff']
explode = (0.1, 0)

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.title('Distribution of Casual Users vs Registered Users')

st.subheader('User Distribution: Casual vs Registered')

st.pyplot(plt)
st.write(f"From {total_count} users, there are {registered_count} registered users. The rest are casual ones")


monthly_changes = day_df.groupby(['yr', 'mnth'])[['temp', 'atemp', 'hum', 'windspeed']].mean()

# Separate data for 2011 and 2012
monthly_changes_2011 = monthly_changes.loc[2011]
monthly_changes_2012 = monthly_changes.loc[2012]


plt.figure(figsize=(20, 5))  # Adjust figure size for better readability

# First chart: temp and atemp
plt.subplot(1, 3, 1)  # 1 row, 3 columns, first subplot
plt.plot(monthly_changes_2011.index, monthly_changes_2011['temp'], label='Temperature')
plt.plot(monthly_changes_2011.index, monthly_changes_2011['atemp'], label='Feels Like Temperature')
plt.title('Monthly Temperature and Feels Like Temperature in Celcius (2011)')
plt.xlabel('Month')
plt.ylabel('Temperature')
plt.legend()

# Second chart: hum
plt.subplot(1, 3, 2)  # 1 row, 3 columns, second subplot
plt.plot(monthly_changes_2011.index, monthly_changes_2011['hum'], label='Humidity')
plt.title('Monthly Humidity (2011)')
plt.xlabel('Month')
plt.ylabel('Humidity')
plt.legend()

# Third chart: windspeed
plt.subplot(1, 3, 3)  # 1 row, 3 columns, third subplot
plt.plot(monthly_changes_2011.index, monthly_changes_2011['windspeed'], label='Windspeed')
plt.title('Monthly Windspeed (2011)')
plt.xlabel('Month')
plt.ylabel('Windspeed')
plt.legend()

plt.tight_layout()  # Adjust subplot parameters for a tight layout
plt.show()


plt.figure(figsize=(20, 5))  # Adjust figure size for better readability

# First chart: temp and atemp
plt.subplot(1, 3, 1)  # 1 row, 3 columns, first subplot
plt.plot(monthly_changes_2012.index, monthly_changes_2012['temp'], label='Temperature')
plt.plot(monthly_changes_2012.index, monthly_changes_2012['atemp'], label='Feels Like Temperature')
plt.title('Monthly Temperature and Feels Like Temperature in Celcius (2012)')
plt.xlabel('Month')
plt.ylabel('Temperature')
plt.legend()

# Second chart: hum
plt.subplot(1, 3, 2)  # 1 row, 3 columns, second subplot
plt.plot(monthly_changes_2012.index, monthly_changes_2012['hum'], label='Humidity')
plt.title('Monthly Humidity (2012)')
plt.xlabel('Month')
plt.ylabel('Humidity')
plt.legend()

# Third chart: windspeed
plt.subplot(1, 3, 3)  # 1 row, 3 columns, third subplot
plt.plot(monthly_changes_2012.index, monthly_changes_2012['windspeed'], label='Windspeed')
plt.title('Monthly Windspeed (2012)')
plt.xlabel('Month')
plt.ylabel('Windspeed')
plt.legend()
st.subheader('Monthly Conditions in 2011 and 2012')

plt.tight_layout()  # Adjust subplot parameters for a tight layout
st.pyplot(plt)

# Group daily changes of weathersit across each 24 month
for year in [2011, 2012]:
  for month in range(1, 13):
    monthly_data = day_df[(day_df['yr'] == year) & (day_df['mnth'] == month)]
    if not monthly_data.empty:
      plt.figure(figsize=(12, 6))
      plt.plot(monthly_data['dteday'], monthly_data['weathersit'], marker='o')
      plt.title(f"Daily Weather Situation Changes ({year}-{month})")
      plt.xlabel("Date")
      plt.ylabel("Weather Situation (1-4)")
      plt.yticks(range(1, 5))
      plt.ylim(0.5, 4.5)  # Add some deviation for better readability
      plt.grid(True)
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      plt.show()


average_user_per_hour = hour_df.groupby('hr')['cnt'].mean()
print(average_user_per_hour)

plt.figure(figsize=(10, 6))
plt.plot(average_user_per_hour.index, average_user_per_hour.values)
plt.title('Average User Count per Hour')
plt.xlabel('Hour')
plt.ylabel('Average User Count')
plt.grid(True)

st.subheader('Average User Count per Hour')
st.pyplot(plt)
st.write("Most users use the service around 8 AM and 5 PM.")

average_hourly_conditions = hour_df.groupby('hr')[['hum', 'temp', 'atemp', 'windspeed']].mean()
print(average_hourly_conditions)

plt.figure(figsize=(12, 6))

plt.plot(average_hourly_conditions.index, average_hourly_conditions['hum'], label='Humidity')
plt.plot(average_hourly_conditions.index, average_hourly_conditions['temp'], label='Temperature')
plt.plot(average_hourly_conditions.index, average_hourly_conditions['atemp'], label='Feels Like Temperature')
plt.plot(average_hourly_conditions.index, average_hourly_conditions['windspeed'], label='Windspeed')


plt.title('Average Hourly Conditions')
plt.xlabel('Hour')
plt.ylabel('Average Value')
plt.grid(True)
plt.legend()
plt.show()
st.subheader('Average Hourly Conditions')
st.pyplot(plt)


st.header('Bike Sharing Dashboard')

st.subheader('Total Users by Year and Month')
yearly_monthly_user_totals['Year_Month'] = yearly_monthly_user_totals['Year'].astype(str) + '-' + yearly_monthly_user_totals['Month'].astype(str)

# Use Altair to create the stacked bar chart
chart = alt.Chart(yearly_monthly_user_totals).mark_bar().encode(
    x='Month:O',
    y='Total_User_Usage:Q',
    color='Year:N',
    tooltip=['Year', 'Month', 'Total_User_Usage']
).properties(
    title="Monthly User Usage across 2011 and 2012"
).interactive()

st.altair_chart(chart, use_container_width=True)
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
st.subheader("Summary:")
st.write("The busiest months were September 2011 and September 2012, possibly due to favorable weather. Rush hour appears to be around 8 AM and 5 PM, when people commute to work or school.  Comfortable temperature and humidity levels appear to contribute to higher user counts. ")
