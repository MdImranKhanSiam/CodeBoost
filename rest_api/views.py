from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_ratelimit.decorators import ratelimit

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from contest.models import Contest
from contest.services import contest_rank



@api_view(["GET"])
@ratelimit(key='user', rate='12/m', block=True)
@permission_classes([IsAuthenticated])
def contest_leaderboard(request):
    now = timezone.now()
    contest_id = request.GET.get('contest_id')

    contest = get_object_or_404(Contest, id=contest_id)

    if now < contest.start_time:
        return HttpResponse("The contest hasn't started yet!", status=403)
    
    problems = contest.problems.all().order_by('id')
    participants = contest.participants.all()

    problems_data = []

    serial = 'A'

    for problem in problems:
        current3 = {}

        current3['id'] = problem.id
        current3['serial'] = serial
        current3['title'] = problem.title
        
        serial = chr(ord(serial) + 1)

        problems_data.append(current3)

    standings, overallStatus = contest_rank(contest, problems, participants)

    data = {}

    standings_data = []

    for standing in standings:
        current = {}

        current['participant_id'] = standing['participant'].id
        current['participant_name'] = standing['participant'].userprofile.display_name
        current['participant_avatar'] = standing['participant'].userprofile.avatar
        current['total_solved'] = standing['total_solved']
        current['total_penalty'] = standing['total_penalty']
        current['total_penalty_in_minutes'] = standing['total_penalty_in_minutes']

        solved_problems_and_penalties = []

        for item in standing['solved_problems_and_penalties']:
            current1 = {}

            if item.get('solved_timestamp'):
                current1['problem_id'] = item['problem'].id
                current1['penalty'] = item['penalty']
                current1['attempts'] = item['attempts']
                current1['solved_timestamp'] = item['solved_timestamp']
            else:
                current1['problem_id'] = item['problem'].id
                current1['attempts'] = item['attempts']

            solved_problems_and_penalties.append(current1)
        
        current['solved_problems_and_penalties'] = solved_problems_and_penalties

        standings_data.append(current)

    # print(standings_data)

    data['standings'] = standings_data
    data['problems'] = problems_data

    return Response(data)