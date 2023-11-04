from django.urls import path
from recordings.views import DetectionSpeciesListView, index
from recordings.api_views import daily_bird_report

urlpatterns = [
    path("daily.json", daily_bird_report),
    path("species/<id>/", DetectionSpeciesListView.as_view(), name="detection_species"),
    path("", index),
]
