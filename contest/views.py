from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from problem.models import Problem
from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from . models import Contest
from . forms import ContestForm



def contests(request):
    now = timezone.now()

    upcoming = list(Contest.objects.filter(start_time__gt=now).order_by("start_time"))
    running = list(Contest.objects.filter(start_time__lte=now, end_time__gte=now).order_by("end_time"))
    ended = list(Contest.objects.filter(end_time__lt=now).order_by("-end_time"))
    
    contests = running + upcoming + ended

    context = {
        'contests': contests,
    }

    return render(request, 'contest/contests.html', context)


@permission_required('contest.add_contest', raise_exception=True)
@login_required(login_url='/accounts/google/login/')
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



@ratelimit(key='user', rate='5/m', block=True)
@login_required(login_url='/accounts/google/login/')
def contest_registration(request, id):
    now = timezone.now()

    contest = get_object_or_404(Contest, id=id)

    if request.user in contest.participants.all():
        return HttpResponse('Already registered')

    if contest.registration_deadline <= now:
        return HttpResponse('The registration has closed')
    
    if request.method == "POST":
        if request.POST.get("agree"):
            contest.participants.add(request.user)

            return redirect('contests')

    context = {
        'contest': contest,    
    }

    return render(request, 'contest/contest_registration.html', context)




def contest_page(request, id):
    context = {

    }

    return render(request, 'contest/contest_page.html', context)