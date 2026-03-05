# 🏔️ Glacier Retreat Predictive Modeling — Nevado del Huila, Colombia

> **Multitemporal GIS analysis of glacier retreat (2000–2022) using Landsat satellite imagery, spectral classification in ArcMap & QGIS, and polynomial projection via Richardson Extrapolation. Result: the Nevado del Huila glacier is projected to disappear by 2030.**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![ArcMap](https://img.shields.io/badge/ArcMap-10.8-green?logo=esri)](https://www.esri.com)
[![QGIS](https://img.shields.io/badge/QGIS-3.28.10-brightgreen?logo=qgis)](https://qgis.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://andresdiaz-glacier-model.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🌐 **[Live Dashboard →](https://andresdiaz-glacier-model.streamlit.app/)**

---

## 📌 Abstract

This study analyzes glacier retreat in the **Volcán Nevado del Huila (VNH)** — the highest point of Colombia's Central Andes — between 2000 and 2022, using 11 Landsat satellite images processed in ArcMap and QGIS. Glacier boundaries were delineated through spectral band ratio classification (B3/B5) following the IDEAM official methodology. Historical areas were validated against IDEAM institutional records. A fifth-degree polynomial model (R² = 0.9612) was fitted and refined through Richardson Extrapolation (10 iterations) to project glacier behavior through 2030.

**Key finding: if current conditions persist, the Nevado del Huila glacier will disappear entirely by 2030** — a loss of over 54% of its 1989 area.

---

## 🗺️ Study Area

| Parameter | Value |
|---|---|
| Glacier | Volcán Nevado del Huila (VNH) |
| Location | Cauca, Huila & Tolima, Colombia |
| Coordinates | 2°55' N, 76°03' W |
| Max elevation | 5,364 m.a.s.l. |
| 1989 area | 14.72 km² |
| 2022 area | 7.46 km² |
| Total loss | −7.26 km² (−49.32%) |
| Study period | 2000–2022 (11 Landsat scenes) |

The VNH is the largest glacier-covered volcano in Colombia, part of the upper watersheds of the Magdalena and Cauca rivers — two of the country's most critical water sources.

---

## 🛰️ Methodology

The workflow was structured in four phases:

### Phase 1 — Satellite Image Selection
- Source: **USGS Earth Explorer** (Landsat Collection 2, Level 2 Science Products — L2SP)
- Images with cloud cover **< 30%** over the glacier zone
- Landsat 7 scan line corrector (SLC-off) gaps filled using QGIS interpolation
- Final dataset: **11 usable scenes** from 2000–2022 (years 2003, 2004, 2006 and others discarded)

### Phase 2 — Digital Image Processing (ArcMap + QGIS)
- Study area clipped using a shapefile with bounding coordinates (2°53'–2°58' N, 76°00'–76°03' W)
- **Band Ratio Classification**: `Band_Ratio = Float(Band 3) / Float(Band 5)` — following the [IDEAM glacier mapping guide (2022)](http://www.ideam.gov.co/web/ecosistemas/glaciares)
- Threshold identification using ArcMap's `Identify` tool and `Raster Calculator`
- Raster-to-polygon conversion, followed by **manual polygon refinement** to remove water bodies, cloud shadows, and volcanic ash artifacts
- Coordinate system: **MAGNA Colombia Bogotá**

### Phase 3 — Glacier Retreat Calculation
- Glacier area (km²) calculated per year using `Calculate Geometry` in ArcMap
- Annual rate of change calculated as:

```
r = [(N / N₀)^(1/t) − 1] × 100
```

- Dataset supplemented with IDEAM institutional records for 2010, 2016, 2017, and 2019 to bridge the 2012–2020 data gap

### Phase 4 — Projection via Polynomial Regression + Richardson Extrapolation
- Missing years (2003–2022) filled via polynomial interpolation
- Fifth-degree polynomial fitted to the complete series (R² = 0.9612)
- **Richardson Extrapolation** applied (step size h=1 year, 10 iterations) to refine projection accuracy
- Projections generated for 2023–2030

---

## 📊 Key Results

| Year | Area (km²) | Cumulative Loss |
|---|---|---|
| 1989 | 14.72 | — (baseline) |
| 2000 | 12.75 | −13.38% |
| 2011 | 8.22 | −44.16% |
| 2020 | 6.67 | −54.69% |
| 2022 | 7.46 | −49.32% |
| **2025 (projected)** | **6.57** | — |
| **2027 (projected)** | **4.67** | — |
| **2030 (projected)** | **0.00** | **−100%** |

**Model metrics:**

| Metric | Value |
|---|---|
| R² | 0.9612 |
| MSE | 0.1431 km² |
| Residual Std Dev | 0.3783 km² |
| Confidence Interval (95%) | ±0.74 km² |
| Mean annual retreat (2000–2022) | −2.28% / −0.427 km²/year |
| Mean projected retreat (2023–2030) | −0.93 km²/year |

---

## 🖥️ Interactive Dashboard

The Streamlit dashboard allows users to explore the model interactively:

- **Adjust polynomial degree** (2–6) and observe fit changes
- **Select projection year** (2025–2050)
- **Apply climate acceleration scenarios** (sensitivity analysis)
- **Animated residual diagnostics** — see how model error evolves over time
- **Climate risk index** — real-time risk classification based on projected area
- **Geographic context map** of the Nevado del Huila location

🔗 **[Open Dashboard](https://andresdiaz-glacier-model.streamlit.app/)**

---

## 🗂️ Repository Structure

```
glacier-retreat-predictive-model/
│
├── app.py                  # Streamlit dashboard (interactive model)
├── requirements.txt        # Python dependencies
│
├── data/
│   └── glacier_area.csv    # Historical glacier areas (km²), 1999–2022
│                           # Sources: Landsat imagery + IDEAM institutional records
│
├── outputs/                # Generated charts and projections
│
├── src/                    # Supporting scripts
│
└── .streamlit/             # Streamlit configuration
```

---

## 🔧 Tech Stack

| Category | Tools |
|---|---|
| GIS Processing | ArcMap 10.8., QGIS 3.28.10 |
| Satellite Data | Landsat 5 TM, Landsat 7 ETM+, Landsat 8 OLI (USGS Earth Explorer) |
| Reference Data | IDEAM Glacier Monitoring Program |
| Spectral Method | Band Ratio (B3/B5), NDSI |
| Python Libraries | NumPy, SciPy, Scikit-learn, Pandas, Matplotlib, Plotly, Streamlit |
| Modeling | Polynomial Regression (degree 5), Richardson Extrapolation |
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
- Richardson, L.F. (1911). *The approximate arithmetical solution by finite differences.* Philosophical Transactions of the Royal Society.
- Rabatel et al. (2013). *Changes in glacier equilibrium-line altitude in the western Alps.* The Cryosphere, 7, 1455–1471.

---

## 👤 Author

**German Andrés Diaz Gelves**
GIS & Spatial Data Analyst | Remote Sensing | Spatial Modeling

Specialist in Geographic Information Systems — Universidad de Manizales (2024)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)]((https://www.linkedin.com/in/adiaz96/))
[![Email](https://img.shields.io/badge/Email-Contact-red?logo=gmail)](mailto:andresdgel96@gmail.com)

*Open to remote opportunities in GIS analysis, environmental monitoring, and geospatial data science.*
