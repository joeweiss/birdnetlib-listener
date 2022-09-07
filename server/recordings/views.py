from django.views.generic import ListView
from recordings.models import Detection, Species
from django.shortcuts import get_object_or_404


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
