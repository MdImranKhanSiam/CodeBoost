from rest_framework import serializers
from user_profile.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'display_name',
            'avatar',
            'bio',
            'gender',
            'date_of_birth',
            'country',
            'website',
            'social',
            'github',
            'preferred_language',
            'rating',
            'solved_problems',
            'solved_count'
        ]