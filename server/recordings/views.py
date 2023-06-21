from django.views.generic import ListView
from recordings.models import Detection, Species
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime

# from datetime import timedelta
from django.utils.timezone import timedelta
from django.db.models import Q
from django.db.models import Count


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


def remove_duplicates(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]


def latest(request):
    today = timezone.now()
    species_today_count = (
        Detection.objects.all()
        .filter(detected_at__date=today)
        .values('species')
        .distinct()
        .count()
    )

    # Last minute
    last_minute_dt = timezone.now() - timedelta(hours=0, minutes=2)
    _species = (
        Detection.objects.filter(detected_at__gte=last_minute_dt)
        .filter(detected_at__lte=timezone.now())
        .order_by("-detected_at")
        .values("species__common_name")
        .values_list("species__common_name", flat=True)
    )
    last_minute = remove_duplicates([i for i in _species])

    # Last hour
    last_hour_dt = timezone.now() - timedelta(hours=1, minutes=0)
    _species = (
        Detection.objects.filter(detected_at__gte=last_hour_dt)
        .filter(detected_at__lte=timezone.now())
        .order_by("-detected_at")
        .values("species__common_name")
        .values_list("species__common_name", flat=True)
    )
    last_hour = remove_duplicates([i for i in _species])

    # most_common today
    today = timezone.now()
    _species = (
        Detection.objects.filter(detected_at__date=today)
        .values("species__common_name")
        .annotate(count=Count("species__common_name"))
        .order_by("-count")
    )

    max_count = max([i["count"] for i in _species])
    most_common = [
        i["species__common_name"] for i in _species if i["count"] == max_count
    ]

    min_count = min([i["count"] for i in _species])
    least_common = [
        i["species__common_name"] for i in _species if i["count"] == min_count
    ]

    return JsonResponse(
        {
            "daily_count": species_today_count,
            "last_minute": last_minute,
            "last_hour": last_hour,
            "most_common": most_common,
            "least_common": least_common,
        }
    )
