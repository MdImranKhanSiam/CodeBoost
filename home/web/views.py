from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from home.models import CodeSnippet
from problem.models import Problem, Submission
from contest.models import Contest
from user_profile.models import UserProfile

from . cache import get_homepage, set_homepage, invalidate_homepage

def home(request):
    context = get_homepage()

    if not context:
        code_snippet = CodeSnippet.objects.get(title='Welcome to competitive programming')
        active_coders = UserProfile.objects.count()
        total_problems = Problem.objects.count()
        total_submission= Submission.objects.count()
        total_contests = Contest.objects.count()

        context = {
            'code_snippet' : {
                'title': code_snippet.title,
                'code': code_snippet.code
            },

            'active_coders': active_coders,
            'total_problems': total_problems,
            'total_submission': total_submission,
            'total_contests': total_contests,
        }

        set_homepage(context)

    return render(request, 'home/home.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')

