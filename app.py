import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error

# ---------------------------------------------------
# Configuración
# ---------------------------------------------------
st.set_page_config(page_title="Glacier Modeling Dashboard", layout="wide")

st.title("Advanced Glacier Retreat Modeling Dashboard")
st.markdown("Comparative Statistical Analysis: Linear vs Polynomial Regression")

# ---------------------------------------------------
# Cargar datos
# ---------------------------------------------------
df = pd.read_csv("data/glacier_area.csv")

years = df["year"].values
areas = df["area_km2"].values

# Sidebar
st.sidebar.header("Model Settings")
degree = st.sidebar.slider("Polynomial Degree", 2, 6, 4)
projection_year = st.sidebar.slider("Projection Year", 2025, 2050, 2035)

# ---------------------------------------------------
# MODELO LINEAL
# ---------------------------------------------------
linear_coeffs = np.polyfit(years, areas, 1)
linear_model = np.poly1d(linear_coeffs)
linear_pred = linear_model(years)

r2_linear = r2_score(areas, linear_pred)
mse_linear = mean_squared_error(areas, linear_pred)
rmse_linear = np.sqrt(mse_linear)

# ---------------------------------------------------
# MODELO POLINÓMICO
# ---------------------------------------------------
poly_coeffs = np.polyfit(years, areas, degree)
poly_model = np.poly1d(poly_coeffs)
poly_pred = poly_model(years)

r2_poly = r2_score(areas, poly_pred)
mse_poly = mean_squared_error(areas, poly_pred)
rmse_poly = np.sqrt(mse_poly)

# Proyección futura
future_years = np.arange(min(years), projection_year + 1)
linear_future = linear_model(future_years)
poly_future = poly_model(future_years)

# ---------------------------------------------------
# LAYOUT PRINCIPAL
# ---------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Model Comparison")

    fig, ax = plt.subplots(figsize=(8,5))
    ax.scatter(years, areas, label="Observed Data")
    ax.plot(future_years, linear_future, label="Linear Model")
    ax.plot(future_years, poly_future, label=f"Polynomial (deg {degree})")
    ax.axvline(x=max(years), linestyle="--")
    ax.set_xlabel("Year")
    ax.set_ylabel("Area (km²)")
    ax.legend()

    st.pyplot(fig)

with col2:
    st.subheader("Statistical Performance")

    st.markdown("### Linear Model")
    st.metric("R²", f"{r2_linear:.4f}")
    st.metric("RMSE", f"{rmse_linear:.4f}")
    st.metric("MSE", f"{mse_linear:.4f}")

    st.markdown("---")

    st.markdown("### Polynomial Model")
    st.metric("R²", f"{r2_poly:.4f}")
    st.metric("RMSE", f"{rmse_poly:.4f}")
    st.metric("MSE", f"{mse_poly:.4f}")

    st.markdown("---")

    if r2_poly > r2_linear:
        st.success("Polynomial model provides better fit (higher R²).")
    else:
        st.info("Linear model provides comparable or better fit.")

    if degree >= 5:
        st.warning("High polynomial degrees may cause overfitting.")

# ---------------------------------------------------
# RESIDUAL ANALYSIS
# ---------------------------------------------------
st.subheader("Residual Analysis")

residuals_linear = areas - linear_pred
residuals_poly = areas - poly_pred

fig2, ax2 = plt.subplots(figsize=(8,5))
ax2.scatter(years, residuals_linear, label="Linear Residuals")
ax2.scatter(years, residuals_poly, label="Polynomial Residuals")
ax2.axhline(y=0, linestyle="--")
ax2.set_xlabel("Year")
ax2.set_ylabel("Residual (Observed - Predicted)")
ax2.legend()

st.pyplot(fig2)

st.markdown("""
**Interpretation:**
- Residuals close to zero indicate good model fit.
- Random distribution around zero suggests no systematic bias.
- Patterns may indicate model misspecification.
""")

# ---------------------------------------------------
# PROJECTION SECTION
# ---------------------------------------------------
st.subheader("Projection Comparison")

st.write(f"Projected Area in {projection_year}:")
st.write(f"Linear Model: **{linear_model(projection_year):.2f} km²**")
st.write(f"Polynomial Model: **{poly_model(projection_year):.2f} km²**")

st.markdown("---")
st.markdown("Developed by Andres Diaz | GIS & Spatial Data Analyst")
