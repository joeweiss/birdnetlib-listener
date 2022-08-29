from django.contrib import admin
from recordings import models as app_models


class RecordingAdmin(admin.ModelAdmin):
    list_display = ["filepath", "analyze_status", "recording_started"]


admin.site.register(app_models.Recording, RecordingAdmin)


class SpeciesAdmin(admin.ModelAdmin):
    pass


admin.site.register(app_models.Species, SpeciesAdmin)


class AnalyzerAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(app_models.Analyzer, AnalyzerAdmin)


class DetectionAdmin(admin.ModelAdmin):
    list_display = [
        "species",
        "confidence",
        "detected_at",
        "analyzer",
        "extracted_file",
    ]
    list_filter = ["species", "detected_at"]
    raw_id_fields = ["recording", "analysis"]


admin.site.register(app_models.Detection, DetectionAdmin)


class NotificationConfigAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "notification_type",
        "detection_type",
        "is_active",
    ]
    list_filter = [
        "is_active",
    ]


admin.site.register(app_models.NotificationConfig, NotificationConfigAdmin)
