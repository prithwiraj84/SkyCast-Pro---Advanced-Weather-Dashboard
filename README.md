# ⛈️ SkyCast Pro - Advanced Weather Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_DEPLOYED_APP_LINK_HERE)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![API](https://img.shields.io/badge/API-OpenWeatherMap-orange)

**SkyCast Pro** is a production-grade weather analytics dashboard built with Python and Streamlit. It goes beyond simple temperature readings by providing real-time data visualization, air quality assessments, and interactive geographic mapping.

[**🔴 Live Demo**]((https://skycast-pro.streamlit.app/))

---

## 📸 Screenshots

![Dashboard Screenshot](<img width="1904" height="902" alt="image" src="https://github.com/user-attachments/assets/1216935c-1238-4b9d-91d9-90c98ffa200d" />
)

---

## ✨ Key Features

* **Real-Time Data:** Fetches live weather conditions using the OpenWeatherMap API.
* **📍 Local Time Calculation:** Automatically calculates and displays the local time of the searched city (not just the server time).
* **📊 Interactive Analytics:** Uses **Plotly** to visualize temperature trends, humidity levels, and "feels like" comparisons over a 5-day forecast.
* **🍃 Air Quality Index (AQI):** Displays current air pollution levels with health recommendations (Good, Fair, Poor, etc.).
* **🎨 Dynamic UI:** Background animations (Lottie Files) change automatically based on weather conditions (Rain, Snow, Clear, Clouds).
* **🌍 Geospatial Mapping:** Renders an interactive map of the location using Latitude/Longitude data.
* **⚙️ Unit Conversion:** Toggle between Metric (°C, m/s) and Imperial (°F, mph) systems.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Data Processing:** Pandas
* **Visualization:** Plotly Express & Plotly Graph Objects
* **API:** OpenWeatherMap (REST API)
* **Animation:** Streamlit-Lottie

---

## 🚀 How to Run Locally

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
