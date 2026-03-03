import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# Page config
st.set_page_config(page_title="Glacier Retreat Dashboard", layout="wide")

st.title("Glacier Retreat Predictive Dashboard")
st.markdown("Interactive temporal modeling of glacier area reduction.")

# Load data
df = pd.read_csv("data/glacier_area.csv")

years = df["year"].values
areas = df["area_km2"].values

# Sidebar controls
st.sidebar.header("Model Settings")

degree = st.sidebar.slider("Polynomial Degree", 1, 6, 4)
projection_year = st.sidebar.slider("Projection Year", 2025, 2050, 2035)

# Model
coeffs = np.polyfit(years, areas, degree)
poly = np.poly1d(coeffs)

predicted = poly(years)
r2 = r2_score(areas, predicted)

future_years = np.arange(min(years), projection_year + 1)
future_projection = poly(future_years)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Historical Data & Model Fit")

    fig, ax = plt.subplots()
    ax.scatter(years, areas, label="Observed Data")
    ax.plot(future_years, future_projection, label="Polynomial Fit")
    ax.axvline(x=max(years), linestyle="--")
    ax.set_xlabel("Year")
    ax.set_ylabel("Area (km²)")
    ax.set_title("Glacier Area Modeling")
    ax.legend()

    st.pyplot(fig)

with col2:
    st.subheader("Model Performance")

    st.metric("R² Score", f"{r2:.4f}")
    projected_value = poly(projection_year)
    st.metric(f"Projected Area in {projection_year}", f"{projected_value:.2f} km²")

st.markdown("---")
st.markdown("Developed by Andres Diaz | GIS & Spatial Data Analyst")