from collections import defaultdict, Counter
from django.http import HttpResponseForbidden
from django_ratelimit.decorators import ratelimit
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from problem.models import Submission

# Logic for getting the dates (2026-09-16) and number of problems solved on that day
# First get all the submissions from oldest to newest with distinct problems where verdict is Accepted
# Submission.objects.filter(user=user, verdict='Accepted').order_by('problem_id', 'submitted_at').distinct('problem_id')



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


