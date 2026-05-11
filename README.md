

---

# 🌍 Geospatial Analysis & Economic Forecasting

This repository is a comprehensive toolkit for spatial economic analysis. It evolved from standalone Python visualization scripts into a full-stack **Geospatial Economic Forecasting Dashboard**.

## 🏗 Project Structure

The project is divided into two main components:

1. **[Geospatial Economic Forecasting Dashboard](https://www.google.com/search?q=./geospatial-economic-forecasting/) (Django App)**:
* A web-based interface for state and district-level forecasting.
* Features interactive Leaflet maps, SQLite persistence, and plain-language economic interpretations.
* Allows manual entry of NDVI, Nightlight intensity, and Capital Formation proxies.


2. **Standalone Geospatial Visualizations (Python/Altair)**:
* `altair indian states.py`: Scripts to generate high-fidelity, interactive choropleth maps.
* Pre-rendered reports: `altair_bar_chart.html` and `altair_scatter_plot.html`.



---

## 🚀 Getting Started

### Option A: Run the Interactive Dashboard (Recommended)

Navigate to the application folder and initialize the Django server:

```bash
cd geospatial-economic-forecasting
python manage.py migrate
python manage.py runserver 127.0.0.1:8002

```

*View the detailed [Application README](https://www.google.com/search?q=./geospatial-economic-forecasting/README.md) for usage instructions.*

### Option B: Generate Static Maps

To run the analysis scripts directly:

```bash
python "altair indian states.py"

```

---

## 📊 Core Variables & Methodology

The forecasting logic (found in `tasks.py`) utilizes three primary pillars of regional economic health:

| Variable | Description | Proxy For |
| --- | --- | --- |
| **NDVI** | Normalized Difference Vegetation Index | Agricultural health and ecological productivity. |
| **Nightlight** | Satellite-derived nighttime radiance | Urbanization, electrification, and industrial activity. |
| **Capital Formation** | Gross Fixed Capital Formation (GFCF) | Long-term investment and infrastructure growth. |

> **Note:** The current forecasting model uses a weighted linear formula as a prototype methodology. It is designed to be replaced with trained Machine Learning models in future iterations.

---

## 🛠 Tech Stack

* **Web Framework:** Django (Python)
* **Frontend Maps:** Leaflet.js (Dashboard) & Altair/Vega-Lite (Static)
* **Geospatial Data:** GeoJSON (India State/District boundaries)
* **Data Handling:** Pandas, Numpy

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

---

