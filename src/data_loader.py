"""
data_loader.py
--------------
Handles loading and validation of glacier area data.
"""

import pandas as pd
import numpy as np


def load_glacier_data(filepath: str = "data/glacier_area.csv") -> tuple[np.ndarray, np.ndarray]:
    """
    Load glacier area data from CSV file.

    Parameters
    ----------
    filepath : str
        Path to the CSV file containing 'year' and 'area_km2' columns.

    Returns
    -------
    years : np.ndarray
        Array of years.
    areas : np.ndarray
        Array of glacier areas in km².

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist at the specified path.
    ValueError
        If required columns are missing from the file.
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Data file not found at '{filepath}'. "
            "Make sure 'glacier_area.csv' exists in the data/ folder."
        )

    required_columns = {"year", "area_km2"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"CSV must contain columns: {required_columns}. "
            f"Found: {set(df.columns)}"
        )

    years = df["year"].values
    areas = df["area_km2"].values
    return years, areas

