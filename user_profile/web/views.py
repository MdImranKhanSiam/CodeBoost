from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from problem.models import Problem
from . cache import get_authored_problems_page, set_authored_problems_page, invalidate_authored_problems_page


@ratelimit(key='user', rate='30/m', method='GET', block=True)
@login_required(login_url='login')
def user_profile(request, user_id):

    context = {
        'user_id': user_id,
    }

    return render(request, 'user_profile/user_profile.html', context)






@ratelimit(key='user', rate='30/m', method='GET', block=True)
@login_required(login_url='/accounts/google/login/')
def authored_problems(request, user_id):
    # In future, a button will be added for users to make authored problems public or private

    user = request.user
    context = get_authored_problems_page(user.id)

    if not context:
        problems = Problem.objects.filter(created_by=user)
        # solved_ids = set()
        # solved_count = None

        # solved_ids = set(user.userprofile.solved_problems.values_list('id', flat=True))
        # solved_count = user.userprofile.solved_count

        context = {
            'problems': problems,
            # 'solved_ids': solved_ids,
            # 'solved_count': solved_count,
        }

        set_authored_problems_page(user.id, context)

    return render(request, 'user_profile/authored_problems.html', context)

