import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
sys.path.append(os.path.dirname(__file__))

import streamlit as st

from data_loader import load_glacier_data
from glacier_model import (
    fit_polynomial,
    generate_projections,
    compute_metrics,
    compute_risk_index,
)
from charts import build_projection_chart, build_residuals_chart, build_map_chart

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Climate Risk Dashboard",
    layout="wide",
    page_icon="🌍",
)

st.markdown("""
<style>
[data-testid="stSidebar"] {
    min-width: 180px !important;
    max-width: 180px !important;
    width: 180px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 Climate Risk Dashboard — Glacier Retreat Analysis")
st.caption("Nevado del Huila, Colombia | Landsat multitemporal analysis 2000–2022")

# ---------------------------------------------------
# DATA
# ---------------------------------------------------
try:
    years, areas = load_glacier_data("data/glacier_area.csv")
except (FileNotFoundError, ValueError) as e:
    st.error(f"⚠️ Data loading error: {e}")
    st.stop()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("⚙️ Scenario Settings")

degree = st.sidebar.slider("Polynomial Degree", 2, 6, 4)
projection_year = st.sidebar.slider("Projection Year", 2025, 2050, 2035)
climate_factor = st.sidebar.slider(
    "Climate Acceleration Factor (%)",
    0, 50, 10,
    help="Sensitivity analysis only — not calibrated against IPCC projections.",
)

# ---------------------------------------------------
# MODEL
# ---------------------------------------------------
model = fit_polynomial(years, areas, degree)
metrics = compute_metrics(years, areas, model)

future_years, baseline, adjusted = generate_projections(
    model=model,
    start_year=int(min(years)),
    end_year=projection_year,
    climate_factor=climate_factor,
    use_richardson=True,
    richardson_iterations=10,
)

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------
st.markdown("## 📊 Model Performance")

col1, col2, col3, col4 = st.columns(4)
col1.metric("R²", f"{metrics['r2']:.4f}")
col2.metric("RMSE", f"{metrics['rmse']:.4f} km²")
col3.metric("95% Confidence Interval", f"±{metrics['ci_95']:.2f} km²")
col4.metric(
    f"Projected Area {projection_year}",
    f"{adjusted[-1]:.2f} km²",
)

# Risk index
risk_index = compute_risk_index(adjusted[-1], float(max(areas)))

if risk_index > 70:
    st.error(f"🔴 High Climate Risk — Risk Index: {risk_index:.1f}/100")
elif risk_index > 40:
    st.warning(f"🟠 Moderate Climate Risk — Risk Index: {risk_index:.1f}/100")
else:
    st.success(f"🟢 Low Climate Risk — Risk Index: {risk_index:.1f}/100")

# ---------------------------------------------------
# TEMPORAL PROJECTION CHART
# ---------------------------------------------------
st.markdown("## 📈 Temporal Projection")

st.plotly_chart(
    build_projection_chart(years, areas, future_years, baseline, adjusted),
    use_container_width=True,
)

# ---------------------------------------------------
# RESIDUAL ANALYSIS
# ---------------------------------------------------
st.markdown("## 🎞️ Animated Residual Diagnostics")

st.plotly_chart(
    build_residuals_chart(years, metrics["residuals"]),
    use_container_width=True,
)

st.markdown("""
**How to interpret this chart:**
- Residuals close to zero indicate a well-fitted model.
- Increasing dispersion over time suggests growing uncertainty.
- Consistent bias above or below zero indicates systematic model error.
""")

# ---------------------------------------------------
# TEMPORAL GLACIER MAP
# ---------------------------------------------------
st.markdown("## 🗾 Glacier Retreat — Spatial Timeline")

from glacier_map import render_glacier_map
render_glacier_map()

# ---------------------------------------------------
# GEOGRAPHIC CONTEXT MAP
# ---------------------------------------------------
st.markdown("## 🗺️ Geographic Context — Nevado del Huila")

st.plotly_chart(build_map_chart(), use_container_width=True)

st.markdown("---")
st.markdown(
    "Developed by **Andres Diaz** | GIS & Spatial Data Analyst | "
    "[GitHub](https://github.com/andresdiaz2411/glacier-retreat-predictive-model) · "
    "[LinkedIn](https://linkedin.com/in/adiaz96/)"

)

