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

    if request.method == 'POST':
        received_form = ContestForm(request.POST)

        if received_form.is_valid():
            contest_creation_form = received_form.save(commit=False)
            contest_creation_form.created_by = request.user
            contest_creation_form.save()

            return redirect('contest-page', contest_creation_form.id)


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




@login_required(login_url='/accounts/google/login/')
def contest_page(request, id):
    now = timezone.now()
    user = request.user
    is_admin = None

    contest = get_object_or_404(Contest, id=id)
    problems = contest.problems.all()
    contest_form = ContestForm()
    
    unincluded_problems = Problem.objects.filter(is_public=True).exclude(
        id__in=contest.problems.all()
    )
    
    non_moderator_users = User.objects.filter(is_staff=False).exclude(
        id__in=contest.moderators.all()
    ).exclude(
        id=contest.created_by.id
    )

    if (user.is_staff or user == contest.created_by or user in contest.moderators.all()):
        is_admin = True

        context = {
            'contest': contest,
            'is_admin': is_admin,
            'problems': problems,
            'unincluded_problems': unincluded_problems,
            'non_moderator_users': non_moderator_users,
        }
        
        return render(request, 'contest/contest_page.html', context)

    is_admin = False

    if now < contest.start_time:
        return HttpResponse("The contest hasn't started yet!", status=403)

    if user not in contest.participants.all():
        return HttpResponse('You are not a participant of this contest')

    
    context = {
        'contest': contest,
        'is_admin': is_admin,
        'problems': problems,
    }

    return render(request, 'contest/contest_page.html', context)