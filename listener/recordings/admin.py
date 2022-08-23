from django.contrib import admin
from recordings import models as app_models


class RecordingAdmin(admin.ModelAdmin):
    pass


admin.site.register(app_models.Recording, RecordingAdmin)


class SpeciesAdmin(admin.ModelAdmin):
    pass


admin.site.register(app_models.Species, SpeciesAdmin)


class AnalyzerAdmin(admin.ModelAdmin):
    pass


admin.site.register(app_models.Analyzer, AnalyzerAdmin)


class DetectionAdmin(admin.ModelAdmin):
    pass


admin.site.register(app_models.Detection, DetectionAdmin)
