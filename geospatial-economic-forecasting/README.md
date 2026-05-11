# Geospatial Economic Forecasting Dashboard

A small Django web app for creating simple state-level and district-level
economic forecast records and viewing them on an interactive map.

## What The App Does

The dashboard lets a user:

1. Choose `State level` or `District level`.
2. Select a state or district from a dropdown, or click a marker on the map.
3. Enter observed input values:
   - NDVI (Normalized Difference Vegetation Index)
   - Nightlight intensity
   - Capital formation proxy
4. Create a forecast using a transparent demo formula.
5. View the result in a table with a plain-language explanation.
6. Hover over map markers to inspect forecast details.
7. Delete forecast rows when they are no longer needed.
8. Open a popup that lists open/official sources for the input variables.

## Explain It Like I Am 10

Imagine you have a map of India and a notebook.

You tell the app whether you want a forecast for a whole state or for one
district. Then you select the place, enter a few numbers about greenery,
nighttime brightness, and capital formation, and the app gives you a simple
forecast.

The app also explains the result in a sentence, so it is easier to understand
than just looking at a number.

## Important Data Note

This is a prototype. It does not automatically download real satellite or
government datasets.

The user must enter the observed values for:

- NDVI
- Nightlight intensity
- Capital formation proxy

The app includes a button called `Open Source Input Data` that shows where users
can find open or official sources for these variables.

## Forecast Methodology

The current forecast is a transparent demo formula:

```text
predicted yield = (NDVI x 100) + (capital formation x 0.02) + (nightlight intensity x 0.3)
```

This is not a trained machine learning model yet. It is a simple placeholder
method so the dashboard workflow can run end to end.

## App Workflow

```text
User chooses state-level or district-level forecast
        ↓
User selects state/district from dropdown or map marker
        ↓
User enters NDVI, nightlight, and capital formation values
        ↓
App calculates forecast
        ↓
App saves forecast in SQLite
        ↓
Dashboard displays map marker, table result, and plain meaning
```

## Run Locally

```bash
python3 manage.py migrate
python3 manage.py runserver 127.0.0.1:8002 --noreload
```

Open:

- Dashboard: http://127.0.0.1:8002/
- GeoJSON API: http://127.0.0.1:8002/api/map-data/

## How To Use

1. Start the server.
2. Open the dashboard.
3. Choose `State level` or `District level`.
4. Select a state or district from the dropdown, or click a marker on the map.
5. Enter NDVI, nightlight intensity, and capital formation proxy.
6. Click `Create forecast`.
7. Read the result in the table.
8. Hover over map markers for details.
9. Use `Delete` to remove a forecast.
10. Use `Open Source Input Data` to see where input data can be found.

## Input Ranges

| Input | Range | Meaning |
| --- | --- | --- |
| Forecast level | `State level` or `District level` | Choose whether the data represents a whole state or one district. |
| State | Dropdown list | Required for state-level forecasting. |
| District | Dropdown list | Required for district-level forecasting. |
| NDVI (Normalized Difference Vegetation Index) | `0.00` to `1.00` | Low values mean sparse vegetation; high values mean dense vegetation. |
| Nightlight intensity | `0` to `100` | Higher values mean brighter nighttime activity. |
| Capital formation proxy | `0` to `1,000,000` Rs crore | Use the same unit consistently. |

## Open Input Data Sources

The dashboard contains these links inside the `Open Source Input Data` popup.

| Variable | Source | How to use |
| --- | --- | --- |
| NDVI | NASA MODIS MOD13Q1: https://www.earthdata.nasa.gov/data/catalog/lpcloud-mod13q1-061 | Calculate average NDVI for the selected state or district. |
| NDVI | Copernicus Sentinel data: https://www.copernicus.eu/en/access-data | Use Sentinel-2 red and near-infrared bands to calculate NDVI. |
| Nightlight intensity | NASA Earthdata Nighttime Lights: https://www.earthdata.nasa.gov/learn/backgrounders/nighttime-lights | Calculate average nighttime light value for the selected area. |
| Nightlight intensity | NASA Black Marble / VIIRS: https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/science-domain/nighttime-lights/ | Use VIIRS/Black Marble radiance products. |
| Capital formation proxy | RBI Handbook of Statistics on Indian States: https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=Handbook+of+Statistics+on+Indian+States | Use state-wise gross fixed capital formation or gross capital formation tables. |
| Capital formation proxy | MoSPI capital formation tables: https://www.mospi.gov.in/gross-capital-formation-gross-fixed-capital-formation-net-capital-stock-economic-activity-current-1 | Use official capital formation tables in Rs crore. |

For district-level capital formation, official district-level capital formation
data may not always be available. In that case, use a clearly documented proxy,
such as district investment data, district credit/infrastructure data, or an
allocated share of state-level capital formation.

## Main Files

### `manage.py`

Django command-line entry point. Use it for `runserver`, `migrate`, and `shell`.

### `economic_forecasting/settings.py`

Main Django settings: installed apps, database, templates, timezone, middleware,
and allowed hosts.

### `economic_forecasting/urls.py`

Project-level URL router. It sends `/admin/` to Django admin and app routes to
the `forecasts` app.

### `forecasts/models.py`

Defines the database models:

- `District`: stores state/district area information, map center, and boundary metadata.
- `EconomicForecast`: stores forecast inputs, result, date, and forecast level.

### `forecasts/forms.py`

Defines the dashboard form:

- forecast level
- state dropdown
- district dropdown
- NDVI
- nightlight intensity
- capital formation proxy
- boundary fetch checkbox

### `forecasts/views.py`

Handles the main app logic:

- renders the dashboard
- processes submitted forecasts
- saves forecast records
- returns GeoJSON API data for the map
- deletes forecast records

### `forecasts/tasks.py`

Contains the forecast formula and creates `EconomicForecast` records.

### `forecasts/services.py`

Contains the optional OpenStreetMap/Nominatim boundary lookup helper used by the
app for map geometry.

### `forecasts/urls.py`

Defines app URLs:

- `/`
- `/api/map-data/`
- `/forecasts/<id>/delete/`

### `forecasts/templates/forecasts/dashboard.html`

Main dashboard page. It contains:

- form
- interactive Leaflet map
- clickable map markers
- result table
- delete buttons
- source popup modal
- JavaScript for dynamic form and map behavior

### `forecasts/admin.py`

Registers the models in Django admin.

### `forecasts/migrations/`

Database migration files for creating and updating the app tables.

## API Output

The API returns map-ready GeoJSON-style forecast data:

```text
http://127.0.0.1:8002/api/map-data/
```

## In One Sentence

This project lets a user create simple state-level or district-level economic
forecasts from observed inputs and view the results in a map-based Django
dashboard.
