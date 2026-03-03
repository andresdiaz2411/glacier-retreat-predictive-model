# Glacier Retreat Predictive Modeling
### A Temporal Polynomial Regression Approach

## Abstract
This study develops a temporal predictive model to estimate long-term glacier retreat using historical area measurements from 1999 to 2023. A fourth-degree polynomial regression was applied to model glacier area dynamics and project future behavior until 2035.

---

## 1. Introduction

Glacier retreat is one of the most visible indicators of climate change. The objective of this project is to analyze historical glacier area measurements and construct a predictive model capable of estimating future reduction trends.

---

## 2. Data

The dataset includes publicly available glacier area measurements (km²) for selected years between 1999 and 2023.

Structure:
- year
- area_km2

---

## 3. Methodology

A polynomial regression model (degree 4) was fitted using NumPy.

The model performance was evaluated using the coefficient of determination (R²), calculated as:

R² = 1 − (SS_res / SS_tot)

Where:
- SS_res: residual sum of squares
- SS_tot: total sum of squares

---

## 4. Results

The fitted model achieved a high R² value, indicating strong explanatory capacity over historical data.

Projection analysis suggests a continued decreasing trend in glacier area through 2035.

Generated outputs include:

- Historical data visualization
- Polynomial regression fit with R²
- Long-term projection

See the `outputs/` folder for visual results.

---

## 5. Discussion

While polynomial regression captures non-linear temporal patterns, long-term projections should be interpreted cautiously. External climate variables were not incorporated in this simplified model.

Future improvements may include:
- Incorporation of temperature and precipitation data
- Comparison with exponential decay models
- Uncertainty estimation

---

## 6. Tools Used

- Python
- NumPy
- Pandas
- Matplotlib
- Scikit-learn

---

## Author

Andres Diaz  
GIS & Spatial Data Analyst  
Specialized in Spatial Modeling & Geospatial Data Quality  

Open to remote opportunities.
