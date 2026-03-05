"""
glacier_model.py
----------------
Core modeling logic for glacier retreat analysis.
Includes polynomial regression, Richardson Extrapolation,
projections, and model performance metrics.
"""

import numpy as np
from sklearn.metrics import r2_score, mean_squared_error


# ---------------------------------------------------------------------------
# Polynomial model
# ---------------------------------------------------------------------------

def fit_polynomial(years: np.ndarray, areas: np.ndarray, degree: int) -> np.poly1d:
    """
    Fit a polynomial regression model to historical glacier area data.

    Parameters
    ----------
    years : np.ndarray
        Array of observation years.
    areas : np.ndarray
        Array of glacier areas in km².
    degree : int
        Degree of the polynomial (recommended: 4–6).

    Returns
    -------
    np.poly1d
        Fitted polynomial model.
    """
    coeffs = np.polyfit(years, areas, degree)
    return np.poly1d(coeffs)


# ---------------------------------------------------------------------------
# Richardson Extrapolation
# ---------------------------------------------------------------------------

def richardson_extrapolation(model: np.poly1d, x: float, iterations: int = 10) -> float:
    """
    Refine a polynomial model prediction using Richardson Extrapolation.

    This technique improves the accuracy of numerical approximations by
    combining estimates at different step sizes. Based on the methodology
    used in the original VNH glacier study (step size h=1 year, 10 iterations).

    Parameters
    ----------
    model : np.poly1d
        Fitted polynomial model.
    x : float
        Year for which to compute the refined prediction.
    iterations : int
        Number of refinement iterations (default: 10).

    Returns
    -------
    float
        Refined area estimate in km². Clamped to 0 (glacier cannot be negative).
    """
    h = 1.0
    estimate = model(x)

    for _ in range(iterations):
        h /= 2
        new_estimate = (model(x + h) + model(x - h)) / 2
        estimate = new_estimate

    return max(0.0, estimate)


# ---------------------------------------------------------------------------
# Projections
# ---------------------------------------------------------------------------

def generate_projections(
    model: np.poly1d,
    start_year: int,
    end_year: int,
    climate_factor: float = 0.0,
    use_richardson: bool = True,
    richardson_iterations: int = 10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate baseline and climate-adjusted glacier area projections.

    Parameters
    ----------
    model : np.poly1d
        Fitted polynomial model.
    start_year : int
        First year of the projection range.
    end_year : int
        Last year of the projection range (inclusive).
    climate_factor : float
        Climate acceleration factor as a percentage (0–50).
        Applies a proportional reduction to the baseline projection.
        NOTE: This is a sensitivity analysis tool, not an IPCC-calibrated scenario.
    use_richardson : bool
        If True, applies Richardson Extrapolation to each projected year
        beyond the historical period (year > 2022).
    richardson_iterations : int
        Number of Richardson Extrapolation iterations (default: 10).

    Returns
    -------
    future_years : np.ndarray
        Array of projected years.
    baseline : np.ndarray
        Baseline projected areas (km²), clamped to 0.
    adjusted : np.ndarray
        Climate-adjusted projected areas (km²), clamped to 0.
    """
    future_years = np.arange(start_year, end_year + 1)
    baseline = np.array([
        richardson_extrapolation(model, int(y), richardson_iterations)
        if (use_richardson and y > 2022)
        else max(0.0, model(y))
        for y in future_years
    ])
    adjusted = np.clip(baseline * (1 - climate_factor / 100), 0, None)
    return future_years, baseline, adjusted


# ---------------------------------------------------------------------------
# Model metrics
# ---------------------------------------------------------------------------

def compute_metrics(
    years: np.ndarray,
    areas: np.ndarray,
    model: np.poly1d,
) -> dict:
    """
    Compute performance metrics for the fitted polynomial model.

    Parameters
    ----------
    years : np.ndarray
        Historical observation years.
    areas : np.ndarray
        Observed glacier areas in km².
    model : np.poly1d
        Fitted polynomial model.

    Returns
    -------
    dict with keys:
        r2        : float — Coefficient of determination
        rmse      : float — Root Mean Squared Error (km²)
        mse       : float — Mean Squared Error (km²)
        ci_95     : float — 95% confidence interval half-width (km²)
        residuals : np.ndarray — Observed minus predicted values
    """
    predicted = model(years)
    residuals = areas - predicted
    mse = mean_squared_error(areas, predicted)
    rmse = np.sqrt(mse)
    r2 = r2_score(areas, predicted)
    ci_95 = 1.96 * rmse  # Z-critical for 95% confidence level

    return {
        "r2": round(r2, 4),
        "rmse": round(rmse, 4),
        "mse": round(mse, 4),
        "ci_95": round(ci_95, 4),
        "residuals": residuals,
    }


# ---------------------------------------------------------------------------
# Risk index
# ---------------------------------------------------------------------------

def compute_risk_index(projected_area: float, max_area: float) -> float:
    """
    Compute a climate risk index based on projected glacier area loss.

    The index ranges from 0 (no risk) to 100 (glacier fully lost).

    Parameters
    ----------
    projected_area : float
        Projected glacier area at the target year (km²).
    max_area : float
        Maximum historical glacier area in the dataset (km²).

    Returns
    -------
    float
        Risk index value between 0 and 100.
    """
    return max(0.0, 100 - (projected_area / max_area) * 100)
