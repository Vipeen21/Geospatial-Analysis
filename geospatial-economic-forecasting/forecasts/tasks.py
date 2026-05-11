from django.utils import timezone

from .models import District, EconomicForecast


try:
    from celery import shared_task
except ImportError:
    def shared_task(func):
        return func


def predict_yield(features):
    ndvi = features["ndvi_avg"]
    capital = float(features["capital_formation"] or 0)
    nightlight = features["nightlight_intensity"]
    return round((ndvi * 100) + (capital * 0.02) + (nightlight * 0.3), 2)


@shared_task
def run_spatial_forecast(
    district_id,
    vegetation_index_avg,
    nightlight_intensity,
    capital_formation_proxy,
    area_level="district",
    data_source="User supplied observed inputs",
):
    district = District.objects.get(id=district_id)
    prediction = predict_yield(
        {
            "ndvi_avg": vegetation_index_avg,
            "capital_formation": capital_formation_proxy,
            "nightlight_intensity": nightlight_intensity,
        }
    )

    return EconomicForecast.objects.create(
        district=district,
        area_level=area_level,
        prediction_date=timezone.localdate(),
        predicted_yield=prediction,
        nightlight_intensity=nightlight_intensity,
        vegetation_index_avg=vegetation_index_avg,
        capital_formation_proxy=capital_formation_proxy,
        data_source=data_source,
        latitude=district.centroid_latitude,
        longitude=district.centroid_longitude,
    ).id
