from django.urls import path
from recordings.views import DetectionListView, DetectionSpeciesListView

urlpatterns = [
    path("species/<id>/", DetectionSpeciesListView.as_view(), name="detection_species"),
    path("", DetectionListView.as_view()),
]