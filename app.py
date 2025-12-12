import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, timezone
from streamlit_lottie import st_lottie

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="SkyCast Pro", page_icon="⛈️", layout="wide")

# CONSTANTS
API_KEY = st.secrets["OPENWEATHER_API_KEY"]
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

# LOTTIE ANIMATION ASSETS
LOTTIE_ASSETS = {
    "Clear": "https://assets2.lottiefiles.com/packages/lf20_xlky4kvh.json",
    "Clouds": "https://assets9.lottiefiles.com/packages/lf20_kljxfos1.json",
    "Rain": "https://assets7.lottiefiles.com/packages/lf20_b88nh30c.json",
    "Snow": "https://assets2.lottiefiles.com/packages/lf20_wi1lo50l.json",
    "Thunderstorm": "https://assets2.lottiefiles.com/packages/lf20_kuotoz5l.json",
    "Mist": "https://assets2.lottiefiles.com/packages/lf20_k6wspxco.json",
    "Drizzle": "https://assets7.lottiefiles.com/packages/lf20_b88nh30c.json",
    "Default": "https://assets2.lottiefiles.com/packages/lf20_xlky4kvh.json"
}

# --- 2. HELPER FUNCTIONS ---

@st.cache_data(ttl=600) # Cache data for 10 mins to save API calls
def get_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

def get_data(url, params):
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return None

def get_local_time(timezone_offset):
    # Get current UTC time
    utc_now = datetime.now(timezone.utc)
    # Apply the offset (seconds) to get local time
    local_time = utc_now + timedelta(seconds=timezone_offset)
    return local_time.strftime("%A, %I:%M %p")

def resolve_aqi(aqi_score):
    aqi_map = {
        1: ("Good", "🟢", "Air quality is satisfactory."),
        2: ("Fair", "🔵", "Air quality is acceptable."),
        3: ("Moderate", "🟡", "Sensitive groups should reduce outdoor exertion."),
        4: ("Poor", "🟠", "Unhealthy. Everyone may begin to experience health effects."),
        5: ("Very Poor", "🔴", "Health alert: everyone may experience serious health effects.")
    }
    return aqi_map.get(aqi_score, ("Unknown", "⚪", "No data available"))

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1163/1163661.png", width=60)
    st.title("SkyCast Pro")
    
    city_input = st.text_input("📍 Search City", "London")
    
    st.markdown("### ⚙️ Preferences")
    unit_system = st.radio("Units", ["Metric (°C, m/s)", "Imperial (°F, mph)"])
    
    units = "metric" if "Metric" in unit_system else "imperial"
    temp_unit = "°C" if units == "metric" else "°F"
    speed_unit = "m/s" if units == "metric" else "mph"

    st.markdown("---")
    st.markdown("Developed with ❤️ using Streamlit")

# --- 4. MAIN APP LOGIC ---

if city_input:
    # Prepare API Parameters
    params = {"q": city_input, "appid": API_KEY, "units": units}
    
    # FETCH 1: Current Weather
    current_data = get_data(BASE_URL, params)
    
    if current_data:
        # Extract Coordinates for other APIs
        lat = current_data['coord']['lat']
        lon = current_data['coord']['lon']
        
        # FETCH 2 & 3: Forecast & AQI
        forecast_params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": units}
        aqi_params = {"lat": lat, "lon": lon, "appid": API_KEY}
        
        forecast_data = get_data(FORECAST_URL, forecast_params)
        aqi_data = get_data(AQI_URL, aqi_params)

        # --- HEADER SECTION (Dynamic) ---
        weather_main = current_data['weather'][0]['main']
        lottie_url = LOTTIE_ASSETS.get(weather_main, LOTTIE_ASSETS["Default"])
        lottie_json = get_lottie(lottie_url)

        local_time_str = get_local_time(current_data['timezone'])

        # Layout: Animation | Title Info
        top_col1, top_col2 = st.columns([1, 2])
        
        with top_col1:
            if lottie_json:
                st_lottie(lottie_json, height=180, key="hero_anim")
        
        with top_col2:
            st.markdown(f"# {city_input.title()}")
            st.markdown(f"### {current_data['weather'][0]['description'].title()}")
            st.markdown(f"🕒 Local Time: **{local_time_str}**")
            
            # Big Temp Display
            current_temp = round(current_data['main']['temp'])
            st.metric("Current", f"{current_temp}{temp_unit}", delta=f"Feels like {round(current_data['main']['feels_like'])}{temp_unit}")

        # --- TABS LAYOUT ---
        tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 Analytics", "🌍 Map & Details"])

        # === TAB 1: DASHBOARD ===
        with tab1:
            # 1. Row of 4 Metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💧 Humidity", f"{current_data['main']['humidity']}%")
            col2.metric("🌬️ Wind", f"{current_data['wind']['speed']} {speed_unit}")
            col3.metric("🎈 Pressure", f"{current_data['main']['pressure']} hPa")
            col4.metric("👁️ Visibility", f"{current_data.get('visibility', 0)/1000} km")

            st.markdown("---")
            
            # 2. AQI Section
            if aqi_data:
                aqi_val = aqi_data['list'][0]['main']['aqi']
                aqi_status, aqi_emoji, aqi_desc = resolve_aqi(aqi_val)
                
                st.subheader("🍃 Air Quality Index")
                c_aqi1, c_aqi2 = st.columns([1, 3])
                with c_aqi1:
                    st.markdown(f"<h1 style='text-align: center; color: gray;'>{aqi_val}</h1>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='text-align: center;'>{aqi_status} {aqi_emoji}</h3>", unsafe_allow_html=True)
                with c_aqi2:
                    st.info(aqi_desc)

        # === TAB 2: ANALYTICS ===
        with tab2:
            st.subheader("📅 5-Day Forecast Trends")
            if forecast_data:
                # Process Forecast Data
                dates = [x['dt_txt'] for x in forecast_data['list']]
                temps = [x['main']['temp'] for x in forecast_data['list']]
                feels = [x['main']['feels_like'] for x in forecast_data['list']]
                humid = [x['main']['humidity'] for x in forecast_data['list']]

                df = pd.DataFrame({'Date': dates, 'Temperature': temps, 'Feels Like': feels, 'Humidity': humid})

                # Interactive Plotly Chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df['Date'], y=df['Temperature'], mode='lines+markers', name='Temp'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['Feels Like'], mode='lines', name='Feels Like', line=dict(dash='dot')))
                
                fig.update_layout(title="Temperature Projection", xaxis_title="Date/Time", yaxis_title=f"Temp ({temp_unit})", hovermode="x unified")
                st.plotly_chart(fig, use_container_width=True)

                # Humidity Bar Chart
                fig_bar = px.bar(df, x="Date", y="Humidity", title="Humidity Levels (%)", color="Humidity", color_continuous_scale="Blues")
                st.plotly_chart(fig_bar, use_container_width=True)

        # === TAB 3: MAP & DETAILS ===
        with tab3:
            m_col1, m_col2 = st.columns([2, 1])
            with m_col1:
                st.subheader("🗺️ Geographic Location")
                map_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
                st.map(map_df, zoom=10)
            
            with m_col2:
                st.subheader("☀️ Sun Cycle")
                sunrise = datetime.fromtimestamp(current_data['sys']['sunrise'] + current_data['timezone'], timezone.utc).strftime("%H:%M")
                sunset = datetime.fromtimestamp(current_data['sys']['sunset'] + current_data['timezone'], timezone.utc).strftime("%H:%M")
                
                st.metric("🌅 Sunrise", sunrise)
                st.metric("🌇 Sunset", sunset)
                
                with st.expander("🛠️ Debug Data"):
                    st.json(current_data)

    else:
        # Error UI
        st.error("🚫 City not found! Please check the spelling.")
        st_lottie("https://assets9.lottiefiles.com/packages/lf20_kshjkz2c.json", height=200) # Error animation
else:
    # Idle UI (Welcome Screen)
    st.info("👈 Please enter a city name in the sidebar to begin!")
    st_lottie(LOTTIE_ASSETS["Clear"], height=300)
