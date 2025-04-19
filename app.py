import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set visualization styles
sns.set(style='whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

# 🧑‍💻 PHASE 2: Load Datasets
def load_data():
    education_df = pd.read_csv('datasets/literacy.csv')
    pollution_df = pd.read_csv('datasets/city_day.csv')
    return education_df, pollution_df

# 🧼 PHASE 3: Data Cleaning
def clean_data(education_df, pollution_df):
    # Clean Education Dataset
    education_df.columns = education_df.columns.str.strip()
    education_df = education_df.dropna(subset=['Literacy'])
    
    # Clean Pollution Dataset
    pollution_df.columns = pollution_df.columns.str.strip()
    pollution_df['Date'] = pd.to_datetime(pollution_df['Date'])
    pollution_df = pollution_df[['City', 'Date', 'PM2.5', 'PM10', 'NO2', 'SO2', 'AQI']]
    pollution_df = pollution_df.dropna(subset=['AQI'])
    
    return education_df, pollution_df

# 📊 PHASE 4: Education Dashboard
def education_dashboard(education_df):
    st.title("📘 Education Analysis Dashboard")
    
    # overview section
    st.markdown("### 🔍 Overview")
    st.info("""
        This dashboard presents a comprehensive analysis of literacy rates across different states and districts in India. 
        Use the filters in the sidebar to explore specific states and their educational metrics.
    """)
    
    # Sidebar filters
    st.sidebar.header("Education Filters")
    
    selected_state = st.sidebar.selectbox(
        "Select State",
        ['All'] + sorted(education_df['State'].unique().tolist())
    )
    
    # Filter data based on selection
    if selected_state != 'All':
        education_df = education_df[education_df['State'] == selected_state]
    
    # Metrics 
    st.markdown("### 📈 Key Metrics")
    st.markdown("These metrics provide a quick summary of the selected region's educational status.")
    
    # Create two columns for metrics
    col1, col2 = st.columns(2)
    
    with col1:
        avg_literacy = education_df['Literacy'].mean()
        st.metric("Average Literacy Rate", f"{avg_literacy:.1f}%")
        st.caption("The mean literacy rate across all selected districts")
    
    with col2:
        total_districts = len(education_df)
        st.metric("Number of Districts", total_districts)
        st.caption("Total number of districts in the selected region")
    
    # Top 10 districts by literacy rate
    st.subheader("Top 10 Districts by Literacy Rate")
    top_districts = education_df.nlargest(10, 'Literacy')
    fig, ax = plt.subplots()
    sns.barplot(data=top_districts, x='Literacy', y='District', palette='viridis')
    plt.xlabel('Literacy Rate (%)')
    plt.ylabel('District')
    st.pyplot(fig)
    st.caption("Tip: Hover over the bars to see exact literacy rates. Use sidebar to filter by state.")
    
    # Literacy rate distribution
    st.subheader("Literacy Rate Distribution")
    fig, ax = plt.subplots()
    sns.histplot(data=education_df, x='Literacy', bins=20, kde=True)
    plt.xlabel('Literacy Rate (%)')
    plt.ylabel('Count')
    st.pyplot(fig)
    st.caption("Tip: This distribution shows how literacy rates are spread across districts.")
    
    # State-wise comparison
    st.subheader("State-wise Literacy Comparison")
    state_stats = education_df.groupby('State')['Literacy'].agg(['mean', 'count']).reset_index()
    state_stats = state_stats.sort_values('mean', ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=state_stats, x='State', y='mean', palette='viridis')
    plt.xticks(rotation=90)
    plt.xlabel('State')
    plt.ylabel('Average Literacy Rate (%)')
    st.pyplot(fig)
    st.caption("Tip: This chart shows average literacy rates by state. Use sidebar to filter by state.")
    
    # Alert Zones - Low Literacy
    st.subheader("🚨 Alert Zones - Low Literacy")
    low_literacy = education_df[education_df['Literacy'] < 60]
    if len(low_literacy) > 0:
        st.warning(f"Found {len(low_literacy)} districts with literacy rate below 60%")
        st.dataframe(low_literacy[['District', 'State', 'Literacy']].sort_values('Literacy'))
    else:
        st.success("No districts with literacy rate below 60% in the selected region")
    
    # State/District Comparison Tool
    st.subheader("🧩 State/District Comparison Tool")
    col1, col2 = st.columns(2)
    
    with col1:
        state1 = st.selectbox("Select First State", sorted(education_df['State'].unique().tolist()))
        state1_data = education_df[education_df['State'] == state1]
        district1 = st.selectbox("Select First District", ['All'] + sorted(state1_data['District'].unique().tolist()))
        
        if district1 != 'All':
            state1_data = state1_data[state1_data['District'] == district1]
    
    with col2:
        state2 = st.selectbox("Select Second State", sorted(education_df['State'].unique().tolist()))
        state2_data = education_df[education_df['State'] == state2]
        district2 = st.selectbox("Select Second District", ['All'] + sorted(state2_data['District'].unique().tolist()))
        
        if district2 != 'All':
            state2_data = state2_data[state2_data['District'] == district2]
    
    if st.button("Compare"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"{state1} {district1 if district1 != 'All' else ''}")
            st.metric("Average Literacy", f"{state1_data['Literacy'].mean():.1f}%")
            st.metric("Number of Districts", len(state1_data))
            st.metric("Min Literacy", f"{state1_data['Literacy'].min():.1f}%")
            st.metric("Max Literacy", f"{state1_data['Literacy'].max():.1f}%")
        
        with col2:
            st.subheader(f"{state2} {district2 if district2 != 'All' else ''}")
            st.metric("Average Literacy", f"{state2_data['Literacy'].mean():.1f}%")
            st.metric("Number of Districts", len(state2_data))
            st.metric("Min Literacy", f"{state2_data['Literacy'].min():.1f}%")
            st.metric("Max Literacy", f"{state2_data['Literacy'].max():.1f}%")
        
        # Comparison chart
        fig, ax = plt.subplots(figsize=(10, 6))
        data = pd.DataFrame({
            'Region': [f"{state1} {district1 if district1 != 'All' else ''}", f"{state2} {district2 if district2 != 'All' else ''}"],
            'Literacy Rate': [state1_data['Literacy'].mean(), state2_data['Literacy'].mean()]
        })
        sns.barplot(data=data, x='Region', y='Literacy Rate', palette=['#3498db', '#e74c3c'])
        plt.title("Literacy Rate Comparison")
        plt.ylabel("Literacy Rate (%)")
        st.pyplot(fig)
        st.caption("Tip: This chart compares literacy rates between the selected regions.")

# 📊 PHASE 5:  Pollution Dashboard
def pollution_dashboard(pollution_df):
    st.title("🌫️ AQI Insights Dashboard")
    
    # overview section
    st.markdown("### 🔍 Overview")
    st.info("""
        This dashboard monitors air quality trends across various cities. The Air Quality Index (AQI) 
        and other pollutant measurements help assess environmental health risks.
        Use the sidebar filters to analyze specific cities and time periods.
    """)
    
    # Sidebar filters
    st.sidebar.header("Air Quality Filters")
    
    selected_city = st.sidebar.selectbox(
        "Select City",
        ['All'] + sorted(pollution_df['City'].unique().tolist())
    )
    
    # Date range filter
    min_date = pollution_df['Date'].min()
    max_date = pollution_df['Date'].max()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data based on selection
    if selected_city != 'All':
        pollution_df = pollution_df[pollution_df['City'] == selected_city]
    
    if len(date_range) == 2:
        pollution_df = pollution_df[
            (pollution_df['Date'] >= pd.to_datetime(date_range[0])) &
            (pollution_df['Date'] <= pd.to_datetime(date_range[1]))
        ]
    
    # Metrics 
    st.markdown("### 📈 Key Air Quality Indicators")
    st.markdown("These metrics provide crucial information about air quality levels in the selected region.")
    
    # three columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_aqi = pollution_df['AQI'].mean()
        st.metric("Average AQI", f"{avg_aqi:.1f}")
        st.caption("""
            0-50: Good
            51-100: Moderate
            101-150: Unhealthy for Sensitive Groups
            151+: Unhealthy
        """)
    
    with col2:
        max_pm25 = pollution_df['PM2.5'].max()
        st.metric("Maximum PM2.5", f"{max_pm25:.1f} µg/m³")
        st.caption("Fine particulate matter, dangerous when > 35.5 µg/m³")
    
    with col3:
        max_pm10 = pollution_df['PM10'].max()
        st.metric("Maximum PM10", f"{max_pm10:.1f} µg/m³")
        st.caption("Coarse particulate matter, concerning when > 150 µg/m³")
    
    # AQI trend over time
    st.subheader("AQI Trend Over Time")
    fig, ax = plt.subplots(figsize=(12, 6))
    pollution_df.groupby('Date')['AQI'].mean().plot(ax=ax)
    plt.xlabel('Date')
    plt.ylabel('AQI')
    plt.grid(True)
    st.pyplot(fig)
    st.caption("Tip: This chart shows how AQI has changed over time. Use sidebar to filter by date range.")
    
    # Top 10 most polluted cities
    st.subheader("Top 10 Most Polluted Cities")
    city_stats = pollution_df.groupby('City')['AQI'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=city_stats.values, y=city_stats.index, palette='Reds_r')
    plt.xlabel('Average AQI')
    plt.ylabel('City')
    st.pyplot(fig)
    st.caption("Tip: This chart shows the cities with the highest average AQI. Use sidebar to filter by date range.")
    
    # Pollutant correlation
    st.subheader("Pollutant Correlations")
    corr_matrix = pollution_df[['PM2.5', 'PM10', 'NO2', 'SO2', 'AQI']].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    st.pyplot(fig)
    st.caption("Tip: This heatmap shows correlations between different pollutants. Darker colors indicate stronger correlations.")
    
    # Monthly/Yearly AQI Trends
    st.subheader("📅 Monthly/Yearly AQI Trends")
    trend_type = st.radio("Select Trend Type", ["Monthly", "Yearly"])
    
    if trend_type == "Monthly":
        pollution_df['Month'] = pollution_df['Date'].dt.month
        monthly_aqi = pollution_df.groupby('Month')['AQI'].mean().reset_index()
        monthly_aqi['Month'] = monthly_aqi['Month'].map({
            1: 'January', 2: 'February', 3: 'March', 4: 'April', 
            5: 'May', 6: 'June', 7: 'July', 8: 'August', 
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        })
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=monthly_aqi, x='Month', y='AQI', palette='viridis')
        plt.xticks(rotation=45)
        plt.xlabel('Month')
        plt.ylabel('Average AQI')
        st.pyplot(fig)
        st.caption("Tip: This chart shows average AQI by month. Use sidebar to filter by city and date range.")
    else:
        pollution_df['Year'] = pollution_df['Date'].dt.year
        yearly_aqi = pollution_df.groupby('Year')['AQI'].mean().reset_index()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=yearly_aqi, x='Year', y='AQI', palette='viridis')
        plt.xlabel('Year')
        plt.ylabel('Average AQI')
        st.pyplot(fig)
        st.caption("Tip: This chart shows average AQI by year. Use sidebar to filter by city.")
    
    # Alert Zones - High Pollution
    st.subheader("🚨 Alert Zones - High Pollution")
    high_pollution = pollution_df[pollution_df['AQI'] > 200]
    if len(high_pollution) > 0:
        st.warning(f"Found {len(high_pollution)} records with AQI above 200")
        high_pollution_cities = high_pollution.groupby('City')['AQI'].mean().sort_values(ascending=False)
        st.dataframe(pd.DataFrame({
            'City': high_pollution_cities.index,
            'Average AQI': high_pollution_cities.values
        }))
    else:
        st.success("No records with AQI above 200 in the selected region")
    
    # City Comparison Tool
    st.subheader("🧩 City Comparison Tool")
    col1, col2 = st.columns(2)
    
    with col1:
        city1 = st.selectbox("Select First City", sorted(pollution_df['City'].unique().tolist()))
        city1_data = pollution_df[pollution_df['City'] == city1]
    
    with col2:
        city2 = st.selectbox("Select Second City", sorted(pollution_df['City'].unique().tolist()))
        city2_data = pollution_df[pollution_df['City'] == city2]
    
    if st.button("Compare Cities"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(city1)
            st.metric("Average AQI", f"{city1_data['AQI'].mean():.1f}")
            st.metric("Max AQI", f"{city1_data['AQI'].max():.1f}")
            st.metric("Average PM2.5", f"{city1_data['PM2.5'].mean():.1f} µg/m³")
            st.metric("Average PM10", f"{city1_data['PM10'].mean():.1f} µg/m³")
        
        with col2:
            st.subheader(city2)
            st.metric("Average AQI", f"{city2_data['AQI'].mean():.1f}")
            st.metric("Max AQI", f"{city2_data['AQI'].max():.1f}")
            st.metric("Average PM2.5", f"{city2_data['PM2.5'].mean():.1f} µg/m³")
            st.metric("Average PM10", f"{city2_data['PM10'].mean():.1f} µg/m³")
        
        # Comparison chart
        fig, ax = plt.subplots(figsize=(10, 6))
        data = pd.DataFrame({
            'City': [city1, city2],
            'Average AQI': [city1_data['AQI'].mean(), city2_data['AQI'].mean()]
        })
        sns.barplot(data=data, x='City', y='Average AQI', palette=['#3498db', '#e74c3c'])
        plt.title("AQI Comparison")
        plt.ylabel("Average AQI")
        st.pyplot(fig)
        st.caption("Tip: This chart compares average AQI between the selected cities.")

# 🧑‍💻 PHASE 7: Main Function to Execute All Dashboards
def main():
    st.set_page_config(page_title="InsightEDU & AQI Analysis", layout="wide")
    
    # Load and clean data
    education_df, pollution_df = load_data()
    education_df, pollution_df = clean_data(education_df, pollution_df)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["📘 Education Analysis", "🌫️ AQI Insights"])
    
    if page == "📘 Education Analysis":
        education_dashboard(education_df)
        
        # Auto Summary Box
        if 'selected_state' in locals() and selected_state != 'All':
            st.sidebar.markdown("### 📊 Auto Summary")
            st.sidebar.info(f"In {selected_state}, average literacy is {education_df['Literacy'].mean():.1f}%.")
    
    elif page == "🌫️ AQI Insights":
        pollution_dashboard(pollution_df)
        
        # Auto Summary Box
        if 'selected_city' in locals() and selected_city != 'All':
            st.sidebar.markdown("### 📊 Auto Summary")
            avg_aqi = pollution_df[pollution_df['City'] == selected_city]['AQI'].mean()
            aqi_category = "Good" if avg_aqi <= 50 else "Moderate" if avg_aqi <= 100 else "Unhealthy for Sensitive Groups" if avg_aqi <= 150 else "Unhealthy"
            st.sidebar.info(f"Average AQI in {selected_city} is {avg_aqi:.1f} ({aqi_category}).")

# Run Main
if __name__ == "__main__":
    main()
