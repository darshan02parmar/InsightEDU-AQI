# 📊 InsightEDU & AQI Dashboard

Welcome to **InsightEDU & AQI**, a data analytics dashboard that explores the correlation between **Student Performance** and **Air Pollution** in India. Built as a capstone project for the Edunet Foundation SAP course, this dashboard leverages powerful Python libraries to visualize and interpret insights from two major datasets.

## 🚀 Live App

👉 [Launch the Streamlit App](https://insightedu-aqi-fjpujpbyyxkzzpu8tvbhea.streamlit.app)

## 🧠 Project Objective

The aim of this project is to:
- Analyze literacy and performance data across districts
- Explore air quality metrics across major cities
- Correlate environmental conditions with student performance indicators

## 📂 Datasets Used

1. **Education Dataset:**  
   Contains district-wise literacy rates and other academic indicators.

2. **Pollution Dataset:**  
   Includes city-wise air quality data such as PM2.5, PM10, NO₂, etc.

## 📌 Features

- 📈 Trend analysis using line charts, bar graphs, and heatmaps
- 🗂 Data filtering based on region or pollution level
- 📊 Comparative visualization of education vs AQI
- 🧹 Cleaned and structured data using `pandas`, `numpy`
- 🎨 Interactive charts using `matplotlib`, `seaborn`, and `altair`
- 🌐 Deployed with Streamlit

## ⚙️ Technologies Used

- `Python`
- `pandas`, `numpy`
- `matplotlib`, `seaborn`
- `streamlit`
- `Jupyter Notebook` for initial exploration

## 🛠 Run Locally

```bash
git clone https://github.com/darshan02parmar/insightedu-aqi.git
cd insightedu-aqi
pip install -r requirements.txt
streamlit run app.py
