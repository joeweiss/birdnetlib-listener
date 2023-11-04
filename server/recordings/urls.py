from django.urls import path
from recordings.views import DetectionSpeciesListView, index
from recordings.api_views import (
    daily_bird_report,
    get_weather_conditions,
    get_weather_forecast,
)

urlpatterns = [
    path("daily.json", daily_bird_report),
    path("api/weather/current/", get_weather_conditions),
    path("api/weather/forecast/", get_weather_forecast),
    path("species/<id>/", DetectionSpeciesListView.as_view(), name="detection_species"),
    path("", index),
]
