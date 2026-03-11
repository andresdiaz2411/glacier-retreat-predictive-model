# 🏔️ Glacier Retreat Predictive Modeling — Nevado del Huila, Colombia

> **Multitemporal GIS analysis of glacier retreat (1989–2023) using Landsat satellite imagery, NDSI spectral classification in ArcMap & QGIS, and polynomial projection. Result: the Nevado del Huila glacier is projected to disappear by 2030.**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![ArcMap](https://img.shields.io/badge/ArcMap-10.x-green?logo=esri)](https://www.esri.com)
[![QGIS](https://img.shields.io/badge/QGIS-3.x-brightgreen?logo=qgis)](https://qgis.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://andresdiaz-glacier-model.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🌐 **[Live Dashboard →](https://andresdiaz-glacier-model.streamlit.app/)**

---

## 📌 Abstract

This study analyzes glacier retreat in the **Volcán Nevado del Huila (VNH)** — the highest point of Colombia's Central Andes — between 1989 and 2023, using 17 Landsat satellite images processed in ArcMap and QGIS. Glacier boundaries were delineated through **NDSI (Normalized Difference Snow Index)** spectral classification following the IDEAM official methodology. Historical areas were validated against IDEAM institutional records. A polynomial model (R² = 0.9934) was fitted to project glacier behavior through 2035.

**Key finding: if current conditions persist, the Nevado del Huila glacier will disappear entirely by 2030** — a loss of over 72% of its 1989 area by 2023.

---

## 🗺️ Study Area

| Parameter | Value |
|---|---|
| Glacier | Volcán Nevado del Huila (VNH) |
| Location | Cauca, Huila & Tolima, Colombia |
| Coordinates | 2°56' N, 76°02' W |
| Max elevation | 5,364 m.a.s.l. |
| Protected area | PNN Nevado del Huila |
| 1989 area | 14.72 km² |
| 2023 area | 4.00 km² |
| Total loss | −10.72 km² (−72.81%) |
| Study period | 1989–2023 (17 Landsat scenes) |

The VNH is the largest glacier-covered volcano in Colombia, part of the upper watersheds of the Magdalena and Cauca rivers — two of the country's most critical water sources.

---

## 🛰️ Methodology

### Phase 1 — Satellite Image Selection
- Source: **USGS Earth Explorer** (Landsat Collection 2, Level 2 Science Products)
- Images with cloud cover **< 30%** over the glacier zone
- Sensors: Landsat 5 TM, Landsat 7 ETM+, Landsat 8 OLI, Landsat 9 OLI-2
- Final dataset: **17 usable scenes** from 1989–2023

### Phase 2 — Digital Image Processing (ArcMap + QGIS)
- Study area clipped to the glacier bounding extent
- **NDSI Classification**: `NDSI = (Green − SWIR) / (Green + SWIR)`
- Raster-to-polygon conversion with manual refinement to remove water bodies, cloud shadows, and volcanic ash artifacts
- Coordinate system: **MAGNA-SIRGAS / Colombia Bogotá (EPSG:3116)**

### Phase 3 — Glacier Retreat Calculation
- Glacier area (km²) calculated per year using `Calculate Geometry` in ArcMap
- Annual and cumulative rate of change computed against 1989 baseline
- Dataset supplemented with IDEAM institutional records to fill temporal gaps

### Phase 4 — Projection via Polynomial Regression
- Polynomial model fitted to the complete 1989–2023 series
- R² = 0.9934 — high explanatory power across the full observation period
- Projections generated for 2024–2035 with climate acceleration scenarios

---

## 📊 Key Results

| Year | Area (km²) | vs 1989 |
|---|---|---|
| 1989 | 14.72 | — (baseline) |
| 1999 | 12.96 | −11.9% |
| 2005 | 9.31 | −36.7% |
| 2012 | 8.36 | −43.2% |
| 2020 | 9.84 | −33.1% |
| 2023 | 4.00 | −72.81% |
| **2030 (projected)** | **~0.00** | **−100%** |

**Model metrics:**

| Metric | Value |
|---|---|
| R² | 0.9934 |
| RMSE | 0.2431 km² |
| 95% Confidence Interval | ±0.48 km² |
| Projected area 2035 | 0.00 km² |

---

## 🖥️ Interactive Dashboard

The Streamlit dashboard allows users to explore the model interactively:

- **Adjust polynomial degree** (2–6) and observe fit changes
- **Select projection year** (2025–2050)
- **Apply climate acceleration scenarios** (sensitivity analysis)
- **Animated residual diagnostics** — model error evolution over time
- **Temporal glacier map** — interactive slider across all 17 years (1989–2023) with NDSI-derived polygons overlaid on satellite imagery, area stats, and percentage comparisons vs baseline
- **Geographic context map** — satellite view with PNN boundary and influence area

🔗 **[Open Dashboard](https://andresdiaz-glacier-model.streamlit.app/)**

---

## 🗂️ Repository Structure

```
glacier-retreat-predictive-model/
│
├── app.py                  # Streamlit dashboard
├── glacier_map.py          # Temporal glacier map component (NDSI polygons + slider)
├── requirements.txt        # Python dependencies
│
├── data/
│   ├── glacier_area.csv    # Historical glacier areas (km²), 1989–2023
│   └── NDSI/               # NDSI-derived glacier polygons per year (EPSG:3116)
│       ├── 1989/
│       │   └── 1989_polygon.shp
│       ├── 1997/
│       │   └── 1997_polygon.shp
│       └── ...             # 17 years total (1989–2023)
│
├── src/
│   ├── glacier_model.py    # Polynomial regression + projections
│   ├── data_loader.py      # CSV ingestion and validation
│   └── charts.py           # Plotly chart builders
│
└── outputs/                # Generated charts and projections
```

---

## 🔧 Tech Stack

| Category | Tools |
|---|---|
| GIS Processing | ArcMap 10.x, QGIS 3.x |
| Satellite Data | Landsat 5/7/8/9 (USGS Earth Explorer) |
| Reference Data | IDEAM Glacier Monitoring Program |
| Spectral Method | NDSI (Normalized Difference Snow Index) |
| Coordinate System | MAGNA-SIRGAS / Colombia Bogotá (EPSG:3116) |
| Python Libraries | GeoPandas, NumPy, Scikit-learn, Pandas, Plotly, Streamlit |
| Modeling | Polynomial Regression, Climate Scenario Analysis |
| Deployment | Streamlit Cloud |

---

## ⚡ Run Locally

```bash
git clone https://github.com/andresdiaz2411/glacier-retreat-predictive-model.git
cd glacier-retreat-predictive-model
pip install -r requirements.txt
streamlit run app.py
```

---

## 📖 References

- IDEAM (2022). *Guía para el cálculo del área glaciar mediante el uso de productos de sensoramiento remoto.*
- IDEAM (2021). *Glaciares Colombia.* http://www.ideam.gov.co/web/ecosistemas/glaciares
- USGS (2023). *Landsat Collection 2 Level 2 Science Product Guide.*
- Paul et al. (2015). *The glaciers climate change initiative: Methods for creating glacier area products.* Remote Sensing of Environment, 162, 408–426.
- Rabatel et al. (2013). *Changes in glacier equilibrium-line altitude in the western Alps.* The Cryosphere, 7, 1455–1471.

---

## 👤 Author

**German Andrés Diaz Gelves**
GIS & Spatial Data Analyst | Remote Sensing | Spatial Modeling

Specialist in Geographic Information Systems — Universidad de Manizales (2024)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/adiaz96/)
[![Email](https://img.shields.io/badge/Email-Contact-red?logo=gmail)](mailto:andresdgel96@gmail.com)

*Open to remote opportunities in GIS analysis, environmental monitoring, and geospatial data science.*
