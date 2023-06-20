from django.views.generic import ListView
from recordings.models import Detection, Species
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from django.db.models import Q


class DetectionListView(ListView):
    queryset = Detection.objects.order_by("-detected_at")[0:30]
    context_object_name = "detections"


class DetectionSpeciesListView(ListView):

    template_name = "recordings/detection_by_species_list.html"
    context_object_name = "detections"

    def get_queryset(self):
        self.species = get_object_or_404(Species, id=self.kwargs["id"])
        return Detection.objects.filter(species=self.species).order_by("-detected_at")[
            0:30
        ]

    def get_context_data(self, **kwargs):
        context = super(DetectionSpeciesListView, self).get_context_data(**kwargs)
        context["species"] = self.species
        return context


def latest(request):
    latest_detection = Detection.objects.all().order_by("-detected_at").first()
    today = timezone.now()
    species_today_count = (
        Detection.objects.all()
        .filter(detected_at__date=today)
        .values('species')
        .distinct()
        .count()
    )
    last_10_minutes = timezone.now() - timedelta(hours=0, minutes=20)
    latest_species = (
        Detection.objects
        .filter(Q(detected_at__gte=last_10_minutes))
        .values('species__common_name')
        .distinct()
        .values_list("species__common_name", flat=True)
    )
    recent_birds = [i for i in latest_species]
    return JsonResponse({
        "name": latest_detection.species.common_name,
        "daily_count": species_today_count,
        "recent_birds": recent_birds
    })
