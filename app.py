import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import r2_score, mean_squared_error

# ---------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------
st.set_page_config(
    page_title="Glacier Climate Modeling Dashboard",
    layout="wide",
    page_icon="🌍"
)

st.title("🌍 Glacier Retreat Climate Modeling Dashboard")
st.markdown("Advanced Comparative Statistical Analysis")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_csv("data/glacier_area.csv")
years = df["year"].values
areas = df["area_km2"].values

# Sidebar
st.sidebar.header("⚙️ Model Configuration")
degree = st.sidebar.slider("Polynomial Degree", 2, 6, 4)
projection_year = st.sidebar.slider("Projection Year", 2025, 2050, 2035)

# ---------------------------------------------------
# MODELS
# ---------------------------------------------------
linear_model = np.poly1d(np.polyfit(years, areas, 1))
poly_model = np.poly1d(np.polyfit(years, areas, degree))

linear_pred = linear_model(years)
poly_pred = poly_model(years)

r2_linear = r2_score(areas, linear_pred)
r2_poly = r2_score(areas, poly_pred)

rmse_linear = np.sqrt(mean_squared_error(areas, linear_pred))
rmse_poly = np.sqrt(mean_squared_error(areas, poly_pred))

future_years = np.arange(min(years), projection_year + 1)

# ---------------------------------------------------
# METRICS SECTION
# ---------------------------------------------------
st.markdown("## 📊 Model Performance Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Linear R²", f"{r2_linear:.4f}")
col2.metric("Polynomial R²", f"{r2_poly:.4f}")
col3.metric("Linear RMSE", f"{rmse_linear:.4f}")
col4.metric("Polynomial RMSE", f"{rmse_poly:.4f}")

if r2_poly > r2_linear:
    st.success("Polynomial model provides superior explanatory power.")
else:
    st.info("Linear model performs comparably or better.")

# ---------------------------------------------------
# MAIN GRAPH (INTERACTIVE)
# ---------------------------------------------------
st.markdown("## 📈 Model Comparison")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=years,
    y=areas,
    mode='markers',
    name='Observed Data'
))

fig.add_trace(go.Scatter(
    x=future_years,
    y=linear_model(future_years),
    mode='lines',
    name='Linear Model'
))

fig.add_trace(go.Scatter(
    x=future_years,
    y=poly_model(future_years),
    mode='lines',
    name=f'Polynomial (deg {degree})'
))

fig.add_vline(x=max(years), line_dash="dash")

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Year",
    yaxis_title="Glacier Area (km²)",
    legend_title="Models",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# RESIDUALS GRAPH
# ---------------------------------------------------
st.markdown("## 🔬 Residual Diagnostics")

residual_fig = go.Figure()

residual_fig.add_trace(go.Scatter(
    x=years,
    y=areas - linear_pred,
    mode='markers',
    name='Linear Residuals'
))

residual_fig.add_trace(go.Scatter(
    x=years,
    y=areas - poly_pred,
    mode='markers',
    name='Polynomial Residuals'
))

residual_fig.add_hline(y=0, line_dash="dash")

residual_fig.update_layout(
    template="plotly_dark",
    xaxis_title="Year",
    yaxis_title="Residual (Observed - Predicted)",
    height=500
)

st.plotly_chart(residual_fig, use_container_width=True)

# ---------------------------------------------------
# PROJECTION SECTION
# ---------------------------------------------------
st.markdown("## 🔮 Projection Results")

proj_col1, proj_col2 = st.columns(2)

proj_col1.metric(
    f"Linear Projection ({projection_year})",
    f"{linear_model(projection_year):.2f} km²"
)

proj_col2.metric(
    f"Polynomial Projection ({projection_year})",
    f"{poly_model(projection_year):.2f} km²"
)

st.markdown("---")
st.markdown("Developed by Andres Diaz | GIS & Spatial Data Analyst")
