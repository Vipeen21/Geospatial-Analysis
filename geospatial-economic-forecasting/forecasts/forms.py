from decimal import Decimal

from django import forms

from .district_choices import (
    DISTRICT_CHOICES,
    DISTRICT_COORDINATES,
    STATE_CHOICES,
    STATE_COORDINATES,
)


class ForecastForm(forms.Form):
    forecast_level = forms.ChoiceField(
        label="Forecast level",
        choices=[
            ("district", "District level"),
            ("state", "State level"),
        ],
    )
    state_name = forms.ChoiceField(
        label="State",
        choices=[("", "Select a state")] + STATE_CHOICES,
        required=False,
    )
    district_name = forms.ChoiceField(
        label="District",
        choices=[("", "Select a district")] + DISTRICT_CHOICES,
        required=False,
    )
    vegetation_index_avg = forms.FloatField(
        label="NDVI / vegetation index",
        min_value=0,
        max_value=1,
        help_text="Range: 0.00 to 1.00. Low values mean sparse vegetation; high values mean dense vegetation.",
        widget=forms.NumberInput(attrs={"step": "0.1"}),
    )
    nightlight_intensity = forms.FloatField(
        label="Nightlight intensity",
        min_value=0,
        max_value=100,
        help_text="Range: 0 to 100. Higher values mean brighter night lights.",
    )
    capital_formation_proxy = forms.DecimalField(
        label="Capital formation proxy",
        max_digits=20,
        decimal_places=2,
        min_value=Decimal("0"),
        max_value=Decimal("1000000"),
        help_text="Range: 0 to 1,000,000 Rs crore. Use the same unit consistently.",
        widget=forms.NumberInput(attrs={"step": "1000"}),
    )
    fetch_boundary = forms.BooleanField(
        label="Fetch district boundary from OpenStreetMap",
        required=False,
        initial=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        forecast_level = cleaned_data.get("forecast_level")
        if forecast_level == "state":
            state_name = cleaned_data.get("state_name")
            if not state_name:
                self.add_error("state_name", "Select a state.")
            else:
                cleaned_data["district_name"] = state_name
                cleaned_data["state_name"] = state_name
                latitude, longitude = STATE_COORDINATES[state_name]
                cleaned_data["fallback_latitude"] = latitude
                cleaned_data["fallback_longitude"] = longitude
            return cleaned_data

        district_value = cleaned_data.get("district_name")
        if not district_value:
            self.add_error("district_name", "Select a district.")
        elif "|" in district_value:
            district_name, state_name = district_value.split("|", 1)
            cleaned_data["district_name"] = district_name
            cleaned_data["state_name"] = state_name
            latitude, longitude = DISTRICT_COORDINATES[district_value]
            cleaned_data["fallback_latitude"] = latitude
            cleaned_data["fallback_longitude"] = longitude
        return cleaned_data
