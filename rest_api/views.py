from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from contest.models import Contest
from contest.services import contest_rank

@api_view(["POST"])
def contest_leaderboard(request):
    post_data = request.data

    contest = get_object_or_404(Contest, id=post_data['contest_id'])
    problems = contest.problems.all().order_by('id')
    participants = contest.participants.all()

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

    print(standings_data)

    data['standings'] = standings_data

    return Response(data)