from django.contrib import admin

from .models import District, EconomicForecast


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "area_level", "latest_capital_formation", "boundary_source")
    list_filter = ("area_level", "state")
    search_fields = ("name", "state")


@admin.register(EconomicForecast)
class EconomicForecastAdmin(admin.ModelAdmin):
    list_display = (
        "district",
        "area_level",
        "prediction_date",
        "predicted_yield",
        "nightlight_intensity",
        "vegetation_index_avg",
        "data_source",
    )
    list_filter = ("prediction_date", "district__state")
    search_fields = ("district__name", "district__state")
