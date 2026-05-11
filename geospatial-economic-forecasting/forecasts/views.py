import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .district_choices import (
    DISTRICT_CHOICES,
    DISTRICT_COORDINATES,
    STATE_CHOICES,
    STATE_COORDINATES,
)
from .forms import ForecastForm
from .models import District, EconomicForecast
from .services import fetch_district_boundary
from .tasks import run_spatial_forecast


def dashboard(request):
    if request.method == "POST":
        form = ForecastForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            district, _ = District.objects.get_or_create(
                name=cleaned["district_name"].strip(),
                state=cleaned["state_name"].strip(),
                area_level=cleaned["forecast_level"],
            )

            district.latest_capital_formation = cleaned["capital_formation_proxy"]
            district.centroid_latitude = cleaned["fallback_latitude"]
            district.centroid_longitude = cleaned["fallback_longitude"]
            if not district.boundary_source:
                district.boundary_source = "Built-in district center coordinate"

            if cleaned["fetch_boundary"]:
                try:
                    boundary_data = fetch_district_boundary(
                        district.name,
                        district.state,
                    )
                except Exception as exc:
                    messages.warning(
                        request,
                        f"Boundary lookup failed, so the forecast was saved with a district center marker instead: {exc}",
                    )
                else:
                    if boundary_data:
                        district.centroid_latitude = boundary_data["latitude"]
                        district.centroid_longitude = boundary_data["longitude"]
                        district.boundary_geojson = boundary_data["boundary_geojson"]
                        district.boundary_source = boundary_data["boundary_source"]
                    else:
                        messages.warning(
                            request,
                            "No boundary was found for that district. The forecast was saved with a district center marker.",
                        )

            district.save()
            run_spatial_forecast(
                district.id,
                cleaned["vegetation_index_avg"],
                cleaned["nightlight_intensity"],
                cleaned["capital_formation_proxy"],
                cleaned["forecast_level"],
            )
            messages.success(request, f"Forecast saved for {district.name}.")
            return redirect("dashboard")
    else:
        form = ForecastForm()

    forecasts = (
        EconomicForecast.objects.select_related("district")
        .order_by("-prediction_date", "district__name")[:50]
    )
    return render(
        request,
        "forecasts/dashboard.html",
        {
            "form": form,
            "forecasts": forecasts,
            "district_map_points": json.dumps(
                [
                    {
                        "value": value,
                        "label": label,
                        "level": "district",
                        "lat": DISTRICT_COORDINATES[value][0],
                        "lon": DISTRICT_COORDINATES[value][1],
                    }
                    for value, label in DISTRICT_CHOICES
                ]
                + [
                    {
                        "value": value,
                        "label": label,
                        "level": "state",
                        "lat": STATE_COORDINATES[value][0],
                        "lon": STATE_COORDINATES[value][1],
                    }
                    for value, label in STATE_CHOICES
                ]
            ),
        },
    )


def map_data_api(request):
    forecasts = (
        EconomicForecast.objects.select_related("district")
        .order_by("-prediction_date", "district__name")[:50]
    )
    features = []
    for forecast in forecasts:
        geometry = None
        if forecast.district.boundary_geojson:
            try:
                geometry = json.loads(forecast.district.boundary_geojson)
            except json.JSONDecodeError:
                geometry = None

        if geometry is None and forecast.longitude is not None and forecast.latitude is not None:
            geometry = {
                "type": "Point",
                "coordinates": [forecast.longitude, forecast.latitude],
            }

        features.append(
            {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "district": forecast.district.name,
                    "state": forecast.district.state,
                    "area_level": forecast.area_level,
                    "area_label": (
                        forecast.district.name
                        if forecast.area_level == "state"
                        else f"{forecast.district.name}, {forecast.district.state}"
                    ),
                    "area_value": (
                        forecast.district.state
                        if forecast.area_level == "state"
                        else f"{forecast.district.name}|{forecast.district.state}"
                    ),
                    "prediction_date": forecast.prediction_date.isoformat(),
                    "predicted_yield": forecast.predicted_yield,
                    "nightlight_intensity": forecast.nightlight_intensity,
                    "vegetation_index_avg": forecast.vegetation_index_avg,
                    "capital_formation_proxy": str(forecast.capital_formation_proxy),
                    "data_source": forecast.data_source,
                    "boundary_source": forecast.district.boundary_source,
                    "result_sentence": (
                        f"For {forecast.district.name}, the app estimates a {forecast.area_level}-level "
                        f"predicted yield of "
                        f"{forecast.predicted_yield:.2f} metric tons using the entered NDVI, "
                        f"nightlight, and capital formation values."
                    ),
                },
            }
        )

    return JsonResponse({"type": "FeatureCollection", "features": features})


@require_POST
def delete_forecast(request, forecast_id):
    forecast = get_object_or_404(
        EconomicForecast.objects.select_related("district"),
        id=forecast_id,
    )
    district_name = forecast.district.name
    forecast.delete()
    messages.success(request, f"Deleted forecast for {district_name}.")
    return redirect("dashboard")
