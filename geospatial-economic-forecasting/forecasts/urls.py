from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("api/map-data/", views.map_data_api, name="map_data_api"),
    path("forecasts/<int:forecast_id>/delete/", views.delete_forecast, name="delete_forecast"),
]
