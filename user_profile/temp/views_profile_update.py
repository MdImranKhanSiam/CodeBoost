from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django_ratelimit.decorators import ratelimit

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer


@api_view(["POST"])
@ratelimit(key='user', rate='30/m', method='POST', block=True)
@permission_classes([IsAuthenticated])
def user_profile_update(request):
    """
    Update the profile of the authenticated user.
    Only allows users to update their OWN profile.
    """
    # Always update the requesting user's own profile (security: ignore user_id param)
    target_user_profile = get_object_or_404(UserProfile, user=request.user)

    # partial=True allows sending only the fields you want to change
    serializer = UserProfileSerializer(
        target_user_profile,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"success": True, "message": "Profile updated successfully.", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    return Response(
        {"success": False, "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )
