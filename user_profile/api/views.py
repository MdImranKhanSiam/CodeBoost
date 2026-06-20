import cloudinary.uploader

from collections import Counter
from django.http import HttpResponseForbidden
from django_ratelimit.decorators import ratelimit
from django.shortcuts import get_object_or_404
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from django.contrib.auth.models import User
from user_profile.models import UserProfile
from problem.models import Submission
from . serializers import UserProfileSerializer

from home.cache import invalidate_user_data
from user_profile.api.cache import get_user_profile, set_user_profile, invalidate_user_profile
from user_profile.api.cache import get_user_progress_heatmap, set_user_progress_heatmap, invalidate_user_progress_heatmap


# Logic for getting the dates (2026-09-16) and number of problems solved on that day
# First get all the submissions from oldest to newest with distinct problems where verdict is Accepted
# Submission.objects.filter(user=user, verdict='Accepted').order_by('problem_id', 'submitted_at').distinct('problem_id')





@api_view(["GET"])
@ratelimit(key='user', rate='30/m', method='GET', block=True)
@permission_classes([IsAuthenticated])
def user_profile_data(request):
    target_user_id = request.GET.get('user_id')
    data = get_user_profile(target_user_id)

    if not data:
        target_user = get_object_or_404(User, id=target_user_id)
        target_user_profile = get_object_or_404(UserProfile, user=target_user)
        data = UserProfileSerializer(target_user_profile).data
        set_user_profile(target_user_id, data)

    return Response(data)


@api_view(["POST"])
@ratelimit(key='user', rate='30/m', method='POST', block=True)
@permission_classes([IsAuthenticated])
def user_profile_update(request):
    user_id = request.user.id
    user_profile = get_object_or_404(UserProfile, user=request.user)

    avatar_url = None

    if request.FILES.get('avatar_file'):
        user_avatar = request.FILES.get('avatar_file')
        response = cloudinary.uploader.upload(
            user_avatar,
            resource_type = "image"
        )

        avatar_url = response.get('secure_url')

    data = request.data.copy()

    if avatar_url:
        data['avatar'] = avatar_url

    data.pop('csrfmiddlewaretoken', None)
    data.pop('avatar_file', None)


    data_serializer = UserProfileSerializer(user_profile, data=data, partial=True)

    if data_serializer.is_valid():
        data_serializer.save()
        
        invalidate_user_data(user_id)
        invalidate_user_profile(user_id)

        return Response({"success": True, "data": data_serializer.data}, status=status.HTTP_200_OK)

    return Response({"success": False, "errors": data_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Instead of getting the query for the progress heatmap from submissions, use the field solved problems in the user profile model to add the submission IDs instead of the problem IDs.

@api_view(["GET"])
@ratelimit(key='user', rate='30/m', method='GET', block=True)
@permission_classes([IsAuthenticated])
def progress_heatmap(request):
    target_user_id = request.GET.get('user_id')
    data = get_user_progress_heatmap(target_user_id)

    if not data:
        target_user = get_object_or_404(User, id=target_user_id)
        first_ac = Submission.objects.filter(user=target_user, verdict='Accepted').order_by('problem_id', 'submitted_at').distinct('problem_id')

        # tz_name = request.GET.get('timezone', 'UTC')
        tz_name = 'UTC'

        try:
            tz = ZoneInfo(tz_name)
        except (ZoneInfoNotFoundError, KeyError):
            tz = ZoneInfo('UTC')

        daily_counts = Counter(
            submission.submitted_at.astimezone(tz).date().isoformat()
            for submission in first_ac
        )
        
        data = {}

        for date, count in daily_counts.items():
            year = date[:4]

            if year not in data:
                data[year] = {"data": []}

            data[year]["data"].append({
                "date": date,
                "count": count
            })

        set_user_progress_heatmap(target_user_id, data)
    
    return Response(data)


