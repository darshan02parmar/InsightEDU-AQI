import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

# 📊 PHASE 4: Refined Education Dashboard
def education_dashboard(education_df):
    st.title("Education Analysis Dashboard")
    
    # Add overview section
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
    
    # Metrics with explanations
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
    
    # Literacy rate distribution
    st.subheader("Literacy Rate Distribution")
    fig, ax = plt.subplots()
    sns.histplot(data=education_df, x='Literacy', bins=20, kde=True)
    plt.xlabel('Literacy Rate (%)')
    plt.ylabel('Count')
    st.pyplot(fig)
    
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

# 📊 PHASE 5: Refined Pollution Dashboard
def pollution_dashboard(pollution_df):
    st.title("Air Quality Analysis Dashboard")
    
    # Add overview section
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
    
    # Metrics with explanations
    st.markdown("### 📈 Key Air Quality Indicators")
    st.markdown("These metrics provide crucial information about air quality levels in the selected region.")
    
    # Create three columns for metrics
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
    
    # Top 10 most polluted cities
    st.subheader("Top 10 Most Polluted Cities")
    city_stats = pollution_df.groupby('City')['AQI'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=city_stats.values, y=city_stats.index, palette='Reds_r')
    plt.xlabel('Average AQI')
    plt.ylabel('City')
    st.pyplot(fig)
    
    # Pollutant correlation
    st.subheader("Pollutant Correlations")
    corr_matrix = pollution_df[['PM2.5', 'PM10', 'NO2', 'SO2', 'AQI']].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    st.pyplot(fig)

# 🧑‍💻 PHASE 7: Main Function to Execute All Dashboards
def main():
    st.set_page_config(page_title="InsightEDU & AQI Analysis", layout="wide")
    
    # Load and clean data
    education_df, pollution_df = load_data()
    education_df, pollution_df = clean_data(education_df, pollution_df)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Education Analysis", "Air Quality Analysis"])
    
    if page == "Education Analysis":
        education_dashboard(education_df)
    else:
        pollution_dashboard(pollution_df)

# 🚀 Run Main
if __name__ == "__main__":
    main()
