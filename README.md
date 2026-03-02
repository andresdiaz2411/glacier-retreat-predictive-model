# Glacier Retreat Predictive Model

## Overview
This project develops a predictive spatial model to estimate long-term glacier area reduction using historical measurements and polynomial regression techniques.

## Objective
Analyze the historical area of the **Nevado del Ruiz glacier** and project future behavior over a 20-year horizon.

## Data
Data used in this project is compiled from public glacier area measurements (1999–2023).  
The file `glacier_area.csv` contains the year and corresponding glacier area in km².

## Methodology
- Polynomial regression (degree 4) was fitted to the historical data.
- Temporal rate of change was analyzed.
- Model projections were generated until 2035.

## Tools
- Python
- NumPy
- Matplotlib

## Results
See the `outputs/` folder for visualizations:
- `glacier_historical.png` – Historical glacier area
- `glacier_polynomial_fit.png` – Regression model
- `glacier_projection_2035.png` – Projected glacier area

## Author
Andres Diaz  
GIS & Spatial Data Analyst  
Open to remote opportunities

LinkedIn: https://linkedin.com/in/adiaz96
