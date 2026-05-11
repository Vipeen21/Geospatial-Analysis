import json
import urllib.parse
import urllib.request


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def fetch_district_boundary(district_name, state_name):
    if district_name == state_name:
        query = f"{state_name}, India"
    else:
        query = f"{district_name}, {state_name}, India"
    params = urllib.parse.urlencode(
        {
            "q": query,
            "format": "jsonv2",
            "polygon_geojson": 1,
            "limit": 1,
        }
    )
    request = urllib.request.Request(
        f"{NOMINATIM_URL}?{params}",
        headers={"User-Agent": "geospatial-economic-forecasting-local-demo"},
    )

    with urllib.request.urlopen(request, timeout=12) as response:
        results = json.loads(response.read().decode("utf-8"))

    if not results:
        return {}

    result = results[0]
    latitude = float(result["lat"]) if result.get("lat") else None
    longitude = float(result["lon"]) if result.get("lon") else None
    boundary = result.get("geojson") or {}

    return {
        "latitude": latitude,
        "longitude": longitude,
        "boundary_geojson": json.dumps(boundary) if boundary else "",
        "boundary_source": "OpenStreetMap Nominatim",
        "display_name": result.get("display_name", query),
    }
