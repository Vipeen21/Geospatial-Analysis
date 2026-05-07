
-----

# 🌏 Geospatial Analysis: Economics & Geography

This repository explores the intersection of **spatial data science** and **economic analysis**. It utilizes GeoJSON datasets and GIS software to visualize regional economic trends, specifically focusing on Indian states and demographic distributions.

-----

## 🚀 Key Features

  * **Interactive Visualization**: Leverages the `Altair` library for declarative statistical visualization.
  * **Regional Economics**: Mapping economic indicators across Indian states using high-fidelity GeoJSON data.
  * **Data Processing**: Workflows for cleaning and merging geographic boundaries with tabular economic datasets.

## 📊 Visualizations Included

| File | Description |
| :--- | :--- |
| **`INDIA_STATES.geojson`** | The spatial backbone of the project, providing precise state boundaries. |
| **`altair indian states.py`** | Python script generating interactive maps and choropleths. |
| **`altair_bar_chart.html`** | Statistical breakdown of economic metrics by region. |
| **`altair_scatter_plot.html`** | Correlation analysis between different geographic variables. |

-----

## 🛠️ Tech Stack

  * **Language**:  3.x
  * **Visualization**:  (Vega-Lite)
  * **Data Format**:  / GIS Standard

-----

## ⚡ Quick Start

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/Vipeen21/Geospatial-Analysis.git
    cd Geospatial-Analysis
    ```
2.  **Install Dependencies**:
    ```bash
    pip install altair pandas vegali_datasets
    ```
3.  **Run the Analysis**:
    Execute the Python scripts to generate `.html` visual reports:
    ```bash
    python "altair indian states.py"
    ```

-----

## 🎯 Use Case: Economic Mapping

By blending `GeoJSON` boundaries with economic data (like GDP per state, literacy rates, or industrial output), this project demonstrates how geographic location influences economic outcomes—a key component of **Regional Science**.

-----
