import numpy as np
import matplotlib.pyplot as plt

# Load data
years = np.array([1999, 2000, 2002, 2005, 2008, 2009, 2011, 2015, 2020, 2021, 2023])
areas = np.array([12.96, 12.75, 11.44, 9.31, 8.44, 7.27, 6.68, 5.77, 5.73, 4.86, 4.01])

# Polynomial regression (degree 4)
coeffs = np.polyfit(years, areas, 4)
poly = np.poly1d(coeffs)

# Future projection
future_years = np.arange(1999, 2036)
future_projection = poly(future_years)

print("Projection for 2035:", round(poly(2035), 2), "km²")
