from django.shortcuts import render
from django.contrib.auth.models import User
from . models import Contest
from problem.models import Problem
from . forms import ContestForm

def contests(request):
    contests = Contest.objects.all()
    
    context = {
        'contests': contests,
    }

    return render(request, 'contest/contests.html', context)


def create_contest(request):
    contest_form = ContestForm()
    problems = Problem.objects.all()
    all_users = User.objects.all()

    context = {
        'contest_form' :contest_form,
        'problems': problems,
        'users': all_users,
    }

    return render(request, 'contest/create_contest.html', context)