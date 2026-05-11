from django.db import models
from django.utils import timezone


class District(models.Model):
    AREA_LEVEL_CHOICES = [
        ("district", "District"),
        ("state", "State"),
    ]

    area_level = models.CharField(
        max_length=20,
        choices=AREA_LEVEL_CHOICES,
        default="district",
    )
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    boundary_wkt = models.TextField(
        blank=True,
        help_text="District boundary as WKT. Example: POLYGON((lon lat, ...)).",
    )
    boundary_geojson = models.TextField(blank=True)
    boundary_source = models.CharField(max_length=200, blank=True)
    centroid_latitude = models.FloatField(null=True, blank=True)
    centroid_longitude = models.FloatField(null=True, blank=True)
    latest_capital_formation = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Rs crore",
    )

    class Meta:
        indexes = [models.Index(fields=["name"])]
        ordering = ["state", "name"]

    def __str__(self):
        if self.area_level == "state":
            return f"{self.name} state"
        return f"{self.name}, {self.state}"


class EconomicForecast(models.Model):
    AREA_LEVEL_CHOICES = [
        ("district", "District"),
        ("state", "State"),
    ]

    area_level = models.CharField(
        max_length=20,
        choices=AREA_LEVEL_CHOICES,
        default="district",
    )
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name="forecasts",
    )
    prediction_date = models.DateField(default=timezone.localdate)
    predicted_yield = models.FloatField(help_text="In Metric Tons")
    nightlight_intensity = models.FloatField(
        default=0.0,
        help_text="Proxy for GDP/Economic Activity",
    )
    vegetation_index_avg = models.FloatField(default=0.0)
    capital_formation_proxy = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        help_text="Rs crore",
    )
    data_source = models.CharField(
        max_length=200,
        default="User supplied observed inputs",
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-prediction_date", "district__name"]
        indexes = [
            models.Index(fields=["prediction_date"]),
            models.Index(fields=["district", "prediction_date"]),
        ]

    def __str__(self):
        return f"{self.district} forecast for {self.prediction_date}"
