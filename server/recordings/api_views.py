from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.utils import timezone
from recordings.models import Detection
import flickr_api


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


@api_view()
def get_flickr_image(request, species_id):
    return Response({"detections": "yo"})
