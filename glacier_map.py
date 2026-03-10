"""
glacier_map.py
--------------
Temporal glacier retreat visualization component.
Shows all years overlaid on the map with the selected year highlighted,
plus area stats and percentage comparisons.

Called from app.py as:
    from src.glacier_map import render_glacier_map
    render_glacier_map()

Data structure expected:
    data/NDSI/{year}/{year}_polygon.shp   (individual year polygons, EPSG:3116)
    data/NDSI/ALL/                        (comparative shapefile, optional)
"""

import os
import glob
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

DATA_DIR   = "data/NDSI"
BASE_YEAR  = 1989
CRS_WGS84  = "EPSG:4326"

# Color scale: light blue (old/large) → dark blue (recent/small)
INACTIVE_COLOR = "rgba(147, 197, 253, 0.25)"   # faint blue for background years
INACTIVE_LINE  = "rgba(147, 197, 253, 0.4)"
ACTIVE_COLOR   = "rgba(239, 68, 68, 0.45)"      # red fill for selected year
ACTIVE_LINE    = "#ef4444"
BASE_LINE      = "rgba(251, 191, 36, 0.9)"      # yellow outline for 1989 baseline


# ---------------------------------------------------
# DATA LOADING
# ---------------------------------------------------

@st.cache_data
def load_all_glaciers(data_dir: str) -> dict[int, gpd.GeoDataFrame]:
    """Load all individual year shapefiles, reproject to WGS84."""
    glaciers = {}

    year_dirs = sorted([
        d for d in os.listdir(data_dir)
        if os.path.isdir(os.path.join(data_dir, d)) and d.isdigit()
    ])

    for year_str in year_dirs:
        year = int(year_str)
        pattern = os.path.join(data_dir, year_str, f"{year_str}_polygon.shp")
        matches = glob.glob(pattern)

        if not matches:
            # Try any .shp in the folder
            matches = glob.glob(os.path.join(data_dir, year_str, "*.shp"))

        if matches:
            try:
                gdf = gpd.read_file(matches[0])
                if gdf.crs is None:
                    gdf = gdf.set_crs("EPSG:3116")
                gdf = gdf.to_crs(CRS_WGS84)
                glaciers[year] = gdf
            except Exception as e:
                st.warning(f"Could not load {year}: {e}")

    return glaciers


@st.cache_data
def build_area_table(_glaciers: dict) -> pd.DataFrame:
    """
    Build area summary table from loaded GDFs.
    Area computed from EPSG:3116 (metric) then converted to km².
    """
    rows = []
    for year, gdf in sorted(_glaciers.items()):
        # Reproject to metric CRS to get accurate area
        gdf_metric = gdf.to_crs("EPSG:3116")
        area_m2    = gdf_metric.geometry.area.sum()
        area_km2   = area_m2 / 1_000_000
        rows.append({"year": year, "area_km2": round(area_km2, 4)})

    df = pd.DataFrame(rows).sort_values("year").reset_index(drop=True)

    base_area = df.loc[df["year"] == BASE_YEAR, "area_km2"].values
    base_area = base_area[0] if len(base_area) > 0 else None

    df["pct_vs_base"] = df["area_km2"].apply(
        lambda a: round((a - base_area) / base_area * 100, 2)
        if base_area else None
    )

    df["pct_vs_prev"] = df["area_km2"].pct_change() * 100
    df["pct_vs_prev"] = df["pct_vs_prev"].round(2)

    return df


# ---------------------------------------------------
# MAP BUILDER
# ---------------------------------------------------

def build_glacier_map(
    glaciers: dict[int, gpd.GeoDataFrame],
    selected_year: int,
    years: list[int],
) -> go.Figure:
    """Build Plotly map with all years overlaid, selected year highlighted."""

    fig = go.Figure()

    # Draw all years as faint background
    for year in years:
        gdf = glaciers[year]
        is_base     = year == BASE_YEAR
        is_selected = year == selected_year

        if is_selected or is_base:
            continue  # drawn separately below

        for _, row in gdf.iterrows():
            geom = row.geometry
            if geom is None or geom.is_empty:
                continue
            _add_polygon_trace(
                fig, geom,
                fill_color=INACTIVE_COLOR,
                line_color=INACTIVE_LINE,
                line_width=0.5,
                name=str(year),
                showlegend=False,
                hoverinfo="skip",
            )

    # Draw 1989 baseline outline (if not selected)
    if BASE_YEAR in glaciers and selected_year != BASE_YEAR:
        for _, row in glaciers[BASE_YEAR].iterrows():
            geom = row.geometry
            if geom is None or geom.is_empty:
                continue
            _add_polygon_trace(
                fig, geom,
                fill_color="rgba(251,191,36,0.08)",
                line_color=BASE_LINE,
                line_width=1.5,
                name=f"{BASE_YEAR} (baseline)",
                showlegend=True,
                hovertemplate=f"<b>{BASE_YEAR} — Baseline</b><extra></extra>",
            )

    # Draw selected year highlighted
    if selected_year in glaciers:
        for _, row in glaciers[selected_year].iterrows():
            geom = row.geometry
            if geom is None or geom.is_empty:
                continue
            _add_polygon_trace(
                fig, geom,
                fill_color=ACTIVE_COLOR,
                line_color=ACTIVE_LINE,
                line_width=2.5,
                name=f"{selected_year} (selected)",
                showlegend=True,
                hovertemplate=f"<b>{selected_year}</b><extra></extra>",
            )

    # Center map on glacier
    all_geoms = pd.concat([
        glaciers[y] for y in years if y in glaciers
    ])
    center_lat = all_geoms.geometry.centroid.y.mean()
    center_lon = all_geoms.geometry.centroid.x.mean()

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=12.3,
        ),
        height=520,
        margin=dict(t=0, b=0, l=0, r=0),
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


def _add_polygon_trace(fig, geom, fill_color, line_color, line_width,
                        name, showlegend, hoverinfo=None, hovertemplate=None):
    """Add a polygon (or multipolygon) as a Scattermapbox trace."""
    polys = list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]
    first = True
    for poly in polys:
        x, y = poly.exterior.xy
        lons, lats = list(x) + [None], list(y) + [None]
        kwargs = dict(
            lon=lons, lat=lats,
            mode="lines",
            fill="toself",
            fillcolor=fill_color,
            line=dict(color=line_color, width=line_width),
            name=name,
            showlegend=showlegend and first,
        )
        if hovertemplate:
            kwargs["hovertemplate"] = hovertemplate
        elif hoverinfo:
            kwargs["hoverinfo"] = hoverinfo
        fig.add_trace(go.Scattermapbox(**kwargs))
        first = False


# ---------------------------------------------------
# STATS CARDS
# ---------------------------------------------------

def render_stats(area_df: pd.DataFrame, selected_year: int):
    """Render KPI cards for the selected year."""

    row = area_df[area_df["year"] == selected_year]
    if row.empty:
        return

    area    = row["area_km2"].values[0]
    vs_base = row["pct_vs_base"].values[0]
    vs_prev = row["pct_vs_prev"].values[0]

    # Find previous year
    prev_years = area_df[area_df["year"] < selected_year]["year"].values
    prev_year  = prev_years[-1] if len(prev_years) > 0 else None

    def pct_color(val):
        if val is None or pd.isna(val):
            return "#64748b"
        return "#ef4444" if val < 0 else "#22c55e"

    def pct_arrow(val):
        if val is None or pd.isna(val):
            return "—"
        return f"▼ {abs(val):.2f}%" if val < 0 else f"▲ {abs(val):.2f}%"

    st.markdown(f"""
    <div style="display:grid; grid-template-columns: repeat(3,1fr); gap:1rem; margin:1rem 0 1.5rem 0;">

      <div style="background:#151820; border:1px solid #1e2433; border-top:3px solid #3b82f6;
                  border-radius:8px; padding:1.2rem 1.4rem;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#64748b;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">
          Glacier Area
        </div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:1.8rem;
                    font-weight:600; color:#3b82f6; line-height:1;">
          {area:.4f} km²
        </div>
      </div>

      <div style="background:#151820; border:1px solid #1e2433; border-top:3px solid {pct_color(vs_base)};
                  border-radius:8px; padding:1.2rem 1.4rem;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#64748b;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">
          vs {BASE_YEAR} Baseline
        </div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:1.8rem;
                    font-weight:600; color:{pct_color(vs_base)}; line-height:1;">
          {pct_arrow(vs_base)}
        </div>
      </div>

      <div style="background:#151820; border:1px solid #1e2433; border-top:3px solid {pct_color(vs_prev)};
                  border-radius:8px; padding:1.2rem 1.4rem;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#64748b;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">
          vs {f'{prev_year}' if prev_year else 'Previous'}
        </div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:1.8rem;
                    font-weight:600; color:{pct_color(vs_prev)}; line-height:1;">
          {pct_arrow(vs_prev) if prev_year else '—'}
        </div>
      </div>

    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------
# AREA TREND CHART
# ---------------------------------------------------

def build_trend_chart(area_df: pd.DataFrame, selected_year: int) -> go.Figure:
    """Build area over time line chart with selected year highlighted."""

    fig = go.Figure()

    # Full line
    fig.add_trace(go.Scatter(
        x=area_df["year"],
        y=area_df["area_km2"],
        mode="lines+markers",
        line=dict(color="#3b82f6", width=2),
        marker=dict(
            size=[14 if y == selected_year else 6 for y in area_df["year"]],
            color=["#ef4444" if y == selected_year else "#3b82f6" for y in area_df["year"]],
            line=dict(color="#0d0f14", width=2),
        ),
        hovertemplate="<b>%{x}</b><br>%{y:.4f} km²<extra></extra>",
        showlegend=False,
    ))

    # Vertical line for selected year
    selected_area = area_df.loc[area_df["year"] == selected_year, "area_km2"]
    if not selected_area.empty:
        fig.add_vline(
            x=selected_year,
            line_dash="dot",
            line_color="#ef4444",
            line_width=1.5,
        )

    fig.update_layout(
        height=200,
        margin=dict(t=10, b=30, l=10, r=10),
        paper_bgcolor="#151820",
        plot_bgcolor="#151820",
        font=dict(family="IBM Plex Mono", color="#94a3b8", size=11),
        xaxis=dict(
            gridcolor="#1e2433",
            tickmode="array",
            tickvals=area_df["year"].tolist(),
            ticktext=[str(y)[2:] for y in area_df["year"].tolist()],
            tickangle=-90,
            tickfont=dict(size=9)
        ),
        yaxis=dict(
            gridcolor="#1e2433",
            title="km²",
            title_font_size=10,
        ),
    )

    return fig


# ---------------------------------------------------
# MAIN RENDER FUNCTION
# ---------------------------------------------------

def render_glacier_map():
    """Main entry point — call this from app.py."""

    st.markdown("""
    <div style="border-left:4px solid #f59e0b; padding:0.5rem 0 0.5rem 1.2rem; margin-bottom:1.5rem;">
      <div style="font-family:'IBM Plex Mono',monospace; font-size:0.75rem; color:#f59e0b;
                  text-transform:uppercase; letter-spacing:2px;">
        Temporal Glacier Retreat
      </div>
      <div style="font-size:0.83rem; color:#94a3b8; margin-top:0.3rem;">
        Nevado del Huila — NDSI-derived polygons · EPSG:3116 → WGS84
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    with st.spinner("Loading glacier shapefiles..."):
        glaciers = load_all_glaciers(DATA_DIR)

    if not glaciers:
        st.error(f"No shapefiles found in `{DATA_DIR}`. "
                 f"Expected structure: `{DATA_DIR}/{{year}}/{{year}}_polygon.shp`")
        return

    years      = sorted(glaciers.keys())
    area_df    = build_area_table(glaciers)

    # Year slider
    selected_year = st.select_slider(
        "Select year",
        options=years,
        value=years[-1],
        format_func=lambda y: str(y),
    )

    # Stats cards
    render_stats(area_df, selected_year)

    # Map + trend chart side by side
    col_map, col_chart = st.columns([1.8, 1])

    with col_map:
        fig_map = build_glacier_map(glaciers, selected_year, years)
        st.plotly_chart(fig_map, use_container_width=True)

    with col_chart:
        st.markdown(
            "<div style='font-family:IBM Plex Mono; font-size:0.7rem; color:#f59e0b;"
            "text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;'>"
            "Area Trend</div>",
            unsafe_allow_html=True,
        )
        fig_trend = build_trend_chart(area_df, selected_year)
        st.plotly_chart(fig_trend, use_container_width=True)

        # Mini table
        st.markdown(
            "<div style='font-family:IBM Plex Mono; font-size:0.7rem; color:#64748b;"
            "text-transform:uppercase; letter-spacing:1px; margin:1rem 0 0.3rem 0;'>"
            "All Years</div>",
            unsafe_allow_html=True,
        )
        display_df = area_df[["year", "area_km2", "pct_vs_base"]].copy()
        display_df.columns = ["Year", "Area km²", "Δ vs 1989"]
        display_df["Δ vs 1989"] = display_df["Δ vs 1989"].apply(
            lambda x: f"{x:+.1f}%" if pd.notna(x) else "—"
        )
        st.dataframe(
            display_df,
            use_container_width=True,
            height=300,
            hide_index=True,
        )
