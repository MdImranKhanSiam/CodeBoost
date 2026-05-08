from collections import defaultdict, Counter
from django.http import HttpResponseForbidden
from django_ratelimit.decorators import ratelimit
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from user_profile.models import UserProfile
from problem.models import Submission

# Logic for getting the dates (2026-09-16) and number of problems solved on that day
# First get all the submissions from oldest to newest with distinct problems where verdict is Accepted
# Submission.objects.filter(user=user, verdict='Accepted').order_by('problem_id', 'submitted_at').distinct('problem_id')





@api_view(["GET"])
@ratelimit(key='user', rate='30/m', method='GET', block=True)
@permission_classes([IsAuthenticated])
def user_profile_data(request):
    data = {}

    target_user_id = request.GET.get('user_id')
    target_user = get_object_or_404(User, id=target_user_id)
    target_user_profile = get_object_or_404(UserProfile, user=target_user)

    print(target_user_id)
    user_data = {}

    user_data['name'] = target_user_profile.display_name
    user_data['avatar'] = target_user_profile.avatar
    user_data['bio'] = target_user_profile.bio
    user_data['gender'] = target_user_profile.gender
    user_data['date_of_birth'] = target_user_profile.date_of_birth
    user_data['country'] = target_user_profile.country
    user_data['website'] = target_user_profile.website
    user_data['social'] = target_user_profile.social
    user_data['solved_problem_ids'] = list(target_user_profile.solved_problems.values_list('id', flat=True))
    user_data['solved_count'] = target_user_profile.solved_count
    
    data['user_data'] = user_data

    print(user_data)

    return Response(data)






# Instead of getting the query for the progress heatmap from submissions, use the field solved problems in the user profile model to add the submission IDs instead of the problem IDs.

@api_view(["GET"])
@ratelimit(key='user', rate='30/m', method='GET', block=True)
@permission_classes([IsAuthenticated])
def progress_heatmap(request):
    target_user_id = request.GET.get('user_id')
    target_user = get_object_or_404(User, id=target_user_id)

    first_ac = Submission.objects.filter(user=target_user, verdict='Accepted').order_by('problem_id', 'submitted_at').distinct('problem_id')

    
    daily_counts = Counter(
        submission.submitted_at.date().isoformat()
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

    print(data)

    return Response(data)


