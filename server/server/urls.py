"""listener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from recordings import viewsets

router = routers.DefaultRouter()
router.register(r"users", viewsets.UserViewSet, basename="users")
router.register(r"detections", viewsets.DetectionViewSet, basename="detections")
router.register(r"species", viewsets.SpeciesViewSet, basename="species")
router.register(
    r"species-images", viewsets.SpeciesImageViewSet, basename="species-images"
)


router.register(
    r"today-detections", viewsets.DailyDetectionViewSet, basename="today-detections"
)
router.register(
    r"now-detections", viewsets.NowDetectionViewSet, basename="now-detections"
)
router.register(
    r"daily-species", viewsets.DailySpeciesViewSet, basename="today-species"
)


urlpatterns = (
    # path("api/", include(router.urls)),
    [
        path("admin/", admin.site.urls),
        path("", include(("recordings.urls", "recordings"), namespace="recordings")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
)

urlpatterns = (
    [
        path("api/", include(router.urls)),
        path("admin/", admin.site.urls),
        path("", include(("recordings.urls", "recordings"), namespace="recordings")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
