"""
charts.py
---------
Plotly chart builders for the glacier retreat dashboard.
All functions return go.Figure objects ready for st.plotly_chart().
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Glacier coordinates — Nevado del Huila, Colombia
GLACIER_LAT = 2.9167
GLACIER_LON = -76.05


# ---------------------------------------------------------------------------
# Temporal projection chart
# ---------------------------------------------------------------------------

def build_projection_chart(
    years: np.ndarray,
    areas: np.ndarray,
    future_years: np.ndarray,
    baseline: np.ndarray,
    adjusted: np.ndarray,
) -> go.Figure:
    """
    Build the main temporal projection chart.

    Parameters
    ----------
    years : np.ndarray
        Historical observation years.
    areas : np.ndarray
        Observed glacier areas (km²).
    future_years : np.ndarray
        Full projection year range.
    baseline : np.ndarray
        Baseline projected areas (km²).
    adjusted : np.ndarray
        Climate-adjusted projected areas (km²).

    Returns
    -------
    go.Figure
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years,
        y=areas,
        mode="markers",
        name="Observed Data",
        marker=dict(size=9, color="#00B4D8"),
    ))

    fig.add_trace(go.Scatter(
        x=future_years,
        y=baseline,
        mode="lines",
        name="Baseline Projection",
        line=dict(color="#90E0EF", width=2, dash="dash"),
    ))

    fig.add_trace(go.Scatter(
        x=future_years,
        y=adjusted,
        mode="lines",
        name="Climate Accelerated Scenario",
        line=dict(color="#FF6B6B", width=2),
    ))

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Year",
        yaxis_title="Glacier Area (km²)",
        height=600,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40),
    )

    return fig


# ---------------------------------------------------------------------------
# Animated residuals chart
# ---------------------------------------------------------------------------

def build_residuals_chart(years: np.ndarray, residuals: np.ndarray) -> go.Figure:
    """
    Build an animated residual diagnostics chart.

    Parameters
    ----------
    years : np.ndarray
        Historical observation years.
    residuals : np.ndarray
        Model residuals (observed - predicted).

    Returns
    -------
    go.Figure
    """
    residual_df = pd.DataFrame({"Year": years, "Residual": residuals})

    fig = go.Figure()

    # Final state trace (visible on load)
    fig.add_trace(go.Scatter(
        x=residual_df["Year"],
        y=residual_df["Residual"],
        mode="lines+markers",
        name="Residual Evolution",
        line=dict(color="#90E0EF"),
        marker=dict(color="#00B4D8", size=7),
    ))

    # Animation frames
    frames = [
        go.Frame(
            data=[go.Scatter(
                x=residual_df["Year"][:i + 1],
                y=residual_df["Residual"][:i + 1],
                mode="lines+markers",
                line=dict(color="#90E0EF"),
                marker=dict(color="#00B4D8", size=7),
            )],
            name=str(residual_df["Year"].iloc[i]),
        )
        for i in range(len(residual_df))
    ]
    fig.frames = frames

    fig.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.4)

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Year",
        yaxis_title="Residual (Observed − Predicted)",
        height=500,
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "buttons": [{
                "label": "▶ Play",
                "method": "animate",
                "args": [None, {"frame": {"duration": 300, "redraw": True}, "fromcurrent": True}],
            }],
        }],
        margin=dict(t=40),
    )

    return fig


# ---------------------------------------------------------------------------
# Geographic context map
# ---------------------------------------------------------------------------

def build_map_chart() -> go.Figure:
    """
    Build a geographic context map showing the Nevado del Huila
    location with influence area on satellite imagery.
    """
    import math

    # Generate influence area circle (8 km radius)
    radius_km = 8
    circle_lats, circle_lons = [], []
    for i in range(361):
        angle = math.radians(i)
        dlat = (radius_km / 111.32) * math.cos(angle)
        dlon = (radius_km / (111.32 * math.cos(math.radians(GLACIER_LAT)))) * math.sin(angle)
        circle_lats.append(GLACIER_LAT + dlat)
        circle_lons.append(GLACIER_LON + dlon)

    fig = go.Figure()

    # Influence area fill
    fig.add_trace(go.Scattermapbox(
        lat=circle_lats,
        lon=circle_lons,
        mode="lines",
        fill="toself",
        fillcolor="rgba(0, 180, 216, 0.15)",
        line=dict(color="rgba(0, 180, 216, 0.6)", width=1.5),
        name="Influence Area (~8 km)",
        hoverinfo="skip",
    ))

    # Glacier marker
    fig.add_trace(go.Scattermapbox(
        lat=[GLACIER_LAT],
        lon=[GLACIER_LON],
        mode="markers+text",
        marker=go.scattermapbox.Marker(
            size=14,
            color="#00B4D8",
        ),
        text=["Nevado del Huila"],
        textposition="top right",
        textfont=dict(color="#ffffff", size=13),
        name="Nevado del Huila",
        hovertemplate="<b>Nevado del Huila</b><br>Lat: 2.9167°N<br>Lon: 76.05°W<br>Elev: ~5,364 m<extra></extra>",
    ))

    fig.update_layout(
        mapbox=dict(
            style="white-bg",
            layers=[{
                "below": "traces",
                "sourcetype": "raster",
                "source": [
                    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                ],
            }],
            zoom=10,
            center={"lat": GLACIER_LAT, "lon": GLACIER_LON},
        ),
        height=500,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="#151820",
        legend=dict(
            bgcolor="rgba(21,24,32,0.85)",
            bordercolor="#1e2433",
            borderwidth=1,
            font=dict(color="#e2e8f0", size=11, family="IBM Plex Mono"),
            x=0.01, y=0.99,
        ),
    )

    return fig
