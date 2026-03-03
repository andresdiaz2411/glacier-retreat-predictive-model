import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import r2_score, mean_squared_error

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Climate Risk Dashboard",
    layout="wide",
    page_icon="🌍"
)

st.title("🌍 Climate Risk Dashboard - Glacier Retreat Analysis")

# ---------------------------------------------------
# DATA
# ---------------------------------------------------
df = pd.read_csv("data/glacier_area.csv")
years = df["year"].values
areas = df["area_km2"].values

# Coordinates Nevado del Ruiz
glacier_lat = 4.895
glacier_lon = -75.322

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("⚙️ Scenario Settings")

degree = st.sidebar.slider("Polynomial Degree", 2, 6, 4)
projection_year = st.sidebar.slider("Projection Year", 2025, 2050, 2035)
climate_factor = st.sidebar.slider(
    "Climate Acceleration Factor (%)",
    0, 50, 10
)

# ---------------------------------------------------
# MODEL
# ---------------------------------------------------
poly_model = np.poly1d(np.polyfit(years, areas, degree))

predicted = poly_model(years)

future_years = np.arange(min(years), projection_year + 1)
baseline_projection = poly_model(future_years)

# Apply climate acceleration
adjusted_projection = baseline_projection * (1 - climate_factor / 100)

r2_poly = r2_score(areas, predicted)
rmse_poly = np.sqrt(mean_squared_error(areas, predicted))

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------
st.markdown("## 📊 Model Performance")

col1, col2, col3 = st.columns(3)

col1.metric("R²", f"{r2_poly:.4f}")
col2.metric("RMSE", f"{rmse_poly:.4f}")
col3.metric(
    f"Projected Area {projection_year}",
    f"{adjusted_projection[-1]:.2f} km²"
)

# Risk index
risk_index = max(0, 100 - (adjusted_projection[-1] / max(areas)) * 100)

if risk_index > 70:
    st.error("🔴 High Climate Risk")
elif risk_index > 40:
    st.warning("🟠 Moderate Climate Risk")
else:
    st.success("🟢 Low Climate Risk")

# ---------------------------------------------------
# TEMPORAL GRAPH
# ---------------------------------------------------
st.markdown("## 📈 Temporal Projection")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=years,
    y=areas,
    mode='markers',
    name='Observed'
))

fig.add_trace(go.Scatter(
    x=future_years,
    y=baseline_projection,
    mode='lines',
    name='Baseline Projection'
))

fig.add_trace(go.Scatter(
    x=future_years,
    y=adjusted_projection,
    mode='lines',
    name='Climate Accelerated Scenario'
))

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Year",
    yaxis_title="Glacier Area (km²)",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# RESIDUAL ANALYSIS (AGREGADO)
# ---------------------------------------------------
st.markdown("## 🔬 Residual Diagnostics")

residuals = areas - predicted

residual_fig = go.Figure()

residual_fig.add_trace(go.Scatter(
    x=years,
    y=residuals,
    mode='markers',
    name='Residuals'
))

residual_fig.add_hline(y=0, line_dash="dash")

residual_fig.update_layout(
    template="plotly_dark",
    xaxis_title="Year",
    yaxis_title="Residual (Observed - Predicted)",
    height=500
)

st.plotly_chart(residual_fig, use_container_width=True)

st.markdown("""
**Interpretation:**

- Residuals randomly distributed around zero suggest adequate model fit.
- Systematic patterns may indicate underfitting or model misspecification.
- Increasing dispersion over time may indicate non-stationarity.
""")

# ---------------------------------------------------
# MAP SECTION
# ---------------------------------------------------
st.markdown("## 🗺️ Geographic Context")

map_fig = go.Figure(go.Scattermapbox(
    lat=[glacier_lat],
    lon=[glacier_lon],
    mode='markers',
    marker=go.scattermapbox.Marker(size=14),
    text=["Nevado del Ruiz Glacier"],
))

map_fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_zoom=8,
    mapbox_center={"lat": glacier_lat, "lon": glacier_lon},
    height=500,
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(map_fig, use_container_width=True)

st.markdown("---")
st.markdown("Developed by Andres Diaz | GIS & Spatial Data Analyst")
