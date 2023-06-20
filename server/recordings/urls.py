from django.urls import path
from recordings.views import DetectionListView, DetectionSpeciesListView
from recordings import views

urlpatterns = [
    path("species/<id>/", DetectionSpeciesListView.as_view(), name="detection_species"),
    path("latest/", views.latest),
    path("", DetectionListView.as_view()),
]