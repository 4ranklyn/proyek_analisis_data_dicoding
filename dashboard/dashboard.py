# -*- coding: utf-8 -*-


import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

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



yearly_monthly_user_totals = day_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()


casual_count = day_df['casual'].sum()
registered_count = day_df['registered'].sum()
total_count = day_df['cnt'].sum()


labels = ['Casual Users', 'Registered Users']
sizes = [casual_count, registered_count]
colors = ['#ff9999','#66b3ff']
explode = (0.1, 0)

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.title('Distribution of Casual Users vs Registered Users')


monthly_changes = day_df.groupby(['yr', 'mnth'])[['temp', 'atemp', 'hum', 'windspeed']].mean().reset_index()

# Separate data for 2011 and 2012
monthly_changes_2011 = monthly_changes[monthly_changes['yr'] == 2011]
monthly_changes_2012 = monthly_changes[monthly_changes['yr'] == 2012]


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

plt.tight_layout()  # Adjust subplot parameters for a tight layout



average_user_per_hour = hour_df.groupby('hr')['cnt'].mean()

plt.figure(figsize=(10, 6))
plt.plot(average_user_per_hour.index, average_user_per_hour.values)
plt.title('Average User Count per Hour')
plt.xlabel('Hour')
plt.ylabel('Average User Count')
plt.grid(True)

average_hourly_conditions = hour_df.groupby('hr')[['hum', 'temp', 'atemp', 'windspeed']].mean()

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


st.header('Bike Sharing Dashboard')

st.subheader('Total Users by Year and Month')

yearly_monthly_user_totals.columns = ['yr', 'mnth', 'cnt']

# Create a new 'yr_mnth' column for combined year and month label
yearly_monthly_user_totals['yr_mnth'] = yearly_monthly_user_totals['yr'].astype(str) + '-' + yearly_monthly_user_totals['mnth'].astype(str)

# Sort by yr and mnth for proper ordering
yearly_monthly_user_totals = yearly_monthly_user_totals.sort_values(by=['yr', 'mnth'])

# Use Altair to create the bar chart showing all 24 months
chart = alt.Chart(yearly_monthly_user_totals).mark_bar().encode(
    x=alt.X('yr_mnth:O', sort=None, title='Month-Year'),
    y='cnt:Q',
    color='yr:N',  # Color by year
    tooltip=['yr', 'mnth', 'cnt']
).properties(
    title="Monthly User Usage across 2011 and 2012"
).interactive()

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)

st.write(f"There are about {total_count} users who share bikes across 2011 and 2012.")


st.subheader('User Distribution: Casual vs Registered')

casual_percentage = (casual_count / total_count) * 100
registered_percentage = (registered_count / total_count) * 100

data = pd.DataFrame({
    'User Type': ['Casual Users', 'Registered Users'],
    'Count': [casual_count, registered_count]
})

# Create a donut chart with Altair
data = pd.DataFrame({
    'User Type': ['Casual Users', 'Registered Users'],
    'Count': [casual_count, registered_count],
    'Percentage': [casual_percentage, registered_percentage]
})

# Create a pie chart with Altair
chart = alt.Chart(data).mark_arc(innerRadius=0, outerRadius=100).encode(
    theta=alt.Theta(field="Count", type="quantitative"),
    color=alt.Color(field="User Type", type="nominal", scale=alt.Scale(range=['#ff9999','#66b3ff'])),
    tooltip=['User Type', 'Count', alt.Tooltip('Percentage:Q', format='.1f')]
).properties(
    title='Distribution of Casual Users vs Registered Users'
)
# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)
st.write(f"From {total_count} users, there are {registered_count} registered users. The rest are casual ones")

st.subheader("Monthly Climate Changes in 2011")

# Temperature and Feels Like Temperature in 2011
chart_temp_2011 = alt.Chart(monthly_changes_2011).mark_line(color='#1f77b4').encode(
    x='mnth:O',
    y='temp:Q',
    tooltip=['mnth', 'temp'],
    color=alt.value('#1f77b4')  # Blue for Temperature
).properties(
    title='Monthly Temperature (2011)'
)

chart_atemp_2011 = alt.Chart(monthly_changes_2011).mark_line(color='#ff7f0e').encode(
    x='mnth:O',
    y='atemp:Q',
    tooltip=['mnth', 'atemp'],
    color=alt.value('#ff7f0e')  # Orange for Feels Like Temperature
).properties(
    title='Feels Like Temperature (2011)'
)

# Combine the charts for temperature and feels like temperature with a legend
combined_temp_2011 = alt.layer(chart_temp_2011, chart_atemp_2011).resolve_scale(
    y='independent'
).configure_legend(
    title=None,
    orient='bottom',
    labelFontSize=12
).encode(
    color=alt.condition(
        alt.datum.atemp == alt.datum.atemp,  # Ensure both colors are represented in the legend
        alt.Color('key:N', scale=alt.Scale(domain=['Temperature', 'Feels Like Temperature'], range=['#1f77b4', '#ff7f0e']))
    )
).properties(
    title='Monthly Temperature vs Feels Like Temperature In Celcius (2011)',
    width=600,
    height=300
)
# Humidity in 2011
chart_hum_2011 = alt.Chart(monthly_changes_2011).mark_line(color='green').encode(
    x='mnth:O',
    y='hum:Q',
    tooltip=['mnth', 'hum']
).properties(
    title='Monthly Humidity (2011)'
)

# Windspeed in 2011
chart_windspeed_2011 = alt.Chart(monthly_changes_2011).mark_line(color='blue').encode(
    x='mnth:O',
    y='windspeed:Q',
    tooltip=['mnth', 'windspeed']
).properties(
    title='Monthly Windspeed (2011)'
)

# Display 2011 charts in columns
st.altair_chart(combined_temp_2011, use_container_width=True)
st.altair_chart(chart_hum_2011, use_container_width=True)
st.altair_chart(chart_windspeed_2011, use_container_width=True)

# Create charts for 2012
st.subheader("Monthly Climate Changes in 2012")


# Temperature and Feels Like Temperature in 2012
chart_temp_2012 = alt.Chart(monthly_changes_2012).mark_line(color='#1f77b4').encode(
    x='mnth:O',
    y='temp:Q',
    tooltip=['mnth', 'temp'],
    color=alt.value('#1f77b4')  # Blue for Temperature
).properties(
    title='Monthly Temperature (2012)'
)

chart_atemp_2012 = alt.Chart(monthly_changes_2012).mark_line(color='#ff7f0e').encode(
    x='mnth:O',
    y='atemp:Q',
    tooltip=['mnth', 'atemp'],
    color=alt.value('#ff7f0e')  # Orange for Feels Like Temperature
).properties(
    title='Feels Like Temperature (2012)'
)

# Combine the charts for temperature and feels like temperature with a legend
combined_temp_2012 = alt.layer(chart_temp_2012, chart_atemp_2012).resolve_scale(
    y='independent'
).configure_legend(
    title=None,
    orient='bottom',
    labelFontSize=12
).properties(
    title='Monthly Temperature vs Feels Like Temperature In Celcius (2012)',
    width=600,
    height=300
)

# Humidity in 2012
chart_hum_2012 = alt.Chart(monthly_changes_2012).mark_line(color='green').encode(
    x='mnth:O',
    y='hum:Q',
    tooltip=['mnth', 'hum']
).properties(
    title='Monthly Humidity (2012)'
)

# Windspeed in 2012
chart_windspeed_2012 = alt.Chart(monthly_changes_2012).mark_line(color='blue').encode(
    x='mnth:O',
    y='windspeed:Q',
    tooltip=['mnth', 'windspeed']
).properties(
    title='Monthly Windspeed (2012)'
)

# Display 2012 charts in columns
st.altair_chart(combined_temp_2012, use_container_width=True)
st.altair_chart(chart_hum_2012, use_container_width=True)
st.altair_chart(chart_windspeed_2012, use_container_width=True)

st.subheader('Average User Count per Hour')
st.line_chart(average_user_per_hour)
st.write("Most users use the service around 8 AM and 5 PM.")

st.subheader('Average Hourly Conditions')
st.line_chart(average_hourly_conditions)
st.subheader("Summary:")
st.write("The busiest months were September 2011 and September 2012, possibly due to favorable weather. Rush hour appears to be around 8 AM and 5 PM, when people commute to work or school.  Comfortable temperature and humidity levels appear to contribute to higher user counts. ")
