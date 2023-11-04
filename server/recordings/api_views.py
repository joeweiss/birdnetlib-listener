from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.utils import timezone
from recordings.models import Detection
import requests
from django.conf import settings
from pprint import pprint

from django.views.decorators.cache import cache_page


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})


@api_view()
def daily_bird_report(request):
    today_detections = Detection.objects.all().filter(detected_at__date=timezone.now())
    print(today_detections)
    return Response({"detections": f"what, world!{today_detections}"})


@cache_page(settings.WEATHER_CACHE_SECONDS)
@api_view()
def get_weather_conditions(request):
    lat = settings.LATITUDE
    lon = settings.LONGITUDE
    key = settings.OPENWEATHERAPI_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=imperial"
    response = requests.get(url)
    if response.status_code == 200:
        return Response(response.json())

    return Response({})


@cache_page(settings.WEATHER_CACHE_SECONDS)
@api_view()
def get_weather_forecast(request):
    lat = settings.LATITUDE
    lon = settings.LONGITUDE
    key = settings.OPENWEATHERAPI_KEY
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}&units=imperial&cnt=7"
    response = requests.get(url)
    if response.status_code == 200:
        return Response(response.json())

    return Response({})
