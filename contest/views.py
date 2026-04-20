import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.db import transaction
from problem.models import Problem, TestCase, Submission
from problem.languages import LANGUAGES, LANGUAGE_SNIPPETS
from problem.background_task import code_submission
from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from . models import Contest
from . forms import ContestForm
from . services import contest_rank




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

    if request.method == 'POST':
        received_form = ContestForm(request.POST)

        if received_form.is_valid():
            contest_creation_form = received_form.save(commit=False)
            contest_creation_form.created_by = request.user
            contest_creation_form.save()

            return redirect('contest-page', contest_creation_form.id)


    context = {
        'contest_form' :contest_form,
    }

    return render(request, 'contest/create_contest.html', context)




@login_required(login_url='/accounts/google/login/')
def edit_contest(request, contest_id):
    user = request.user
    contest = get_object_or_404(Contest, id=contest_id)

    if (user.is_staff or user.has_perm('contest.change_contest') or user == contest.created_by or user in contest.moderators.all()):
        contest_form = ContestForm(instance=contest)

        if request.method == 'POST':
            received_form = ContestForm(request.POST, instance=contest)

            if received_form.is_valid():
                contest_update_form = received_form.save(commit=False)
                contest_update_form.save()

                return redirect('contest-page', contest_update_form.id)

        context = {
            'contest': contest,
            'contest_form': contest_form,
        }

        return render(request, 'contest/edit_contest.html', context)
    else:
        return HttpResponse('Permission Denied')



@ratelimit(key='user', rate='5/m', block=True)
@login_required(login_url='/accounts/google/login/')
def contest_registration(request, id):
    user = request.user
    now = timezone.now()

    contest = get_object_or_404(Contest, id=id)

    if user == contest.created_by or user in contest.moderators.all():
        return HttpResponse('Admins of the contest cannot register!')

    if user in contest.participants.all():
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
    problems = contest.problems.all().order_by('id')
    participants = contest.participants.all()

    standings = contest_rank(contest, problems, participants)

    problem_serial_id = {}
    serial = 'A'

    for problem in problems:
        problem.serial = serial
        problem_serial_id[problem.id] = serial
        serial = chr(ord(serial) + 1)


    if (user.is_staff or user == contest.created_by or user in contest.moderators.all()):
        is_admin = True

        unincluded_problems = Problem.objects.filter(is_public=True).exclude(
            id__in=contest.problems.all()
        )

        moderators = contest.moderators.all()
        
        non_moderator_users = User.objects.filter(is_staff=False).exclude(
            id__in=contest.moderators.all()
        ).exclude(
            id=contest.created_by.id
        )

        if request.method == "POST":
            if request.POST.get("users"):
                selected_users_json = request.POST.get("users")
                selected_users_ids = json.loads(selected_users_json)
                selected_users = User.objects.filter(id__in=selected_users_ids)
                contest.moderators.add(*selected_users)

            if request.POST.get("problems"):
                selected_problems_json = request.POST.get("problems")
                selected_problems_ids = json.loads(selected_problems_json)
                selected_problems = Problem.objects.filter(id__in=selected_problems_ids)
                contest.problems.add(*selected_problems)

            if request.POST.get('active_moderators'):
                active_moderators = json.loads(request.POST.get('active_moderators'))
                contest.moderators.set(active_moderators)

        
        context = {
            'contest': contest,
            'is_admin': is_admin,
            'problems': problems,
            'standings': standings,
            'unincluded_problems': unincluded_problems,
            'moderators': moderators,
            'non_moderator_users': non_moderator_users,
        }
        
        return render(request, 'contest/contest_page_second.html', context)

    is_admin = False

    if now < contest.start_time:
        return HttpResponse("The contest hasn't started yet!", status=403)

    if now >= contest.start_time and now <= contest.end_time and user not in contest.participants.all():
        return HttpResponse('You are not a participant of this contest')
    
    context = {
        'contest': contest,
        'is_admin': is_admin,
        'problems': problems,
        'standings': standings,
    }

    return render(request, 'contest/contest_page_second.html', context)




@ratelimit(key='user', rate='6/m', method='POST', block=True)
@login_required(login_url='/accounts/google/login/')
def contest_problem_detail(request, contest_id, problem_id):
    now = timezone.now()
    user = request.user
    contest = get_object_or_404(Contest, id=contest_id)
    problem = Problem.objects.get(id=problem_id)
    
    is_admin = False

    if (user == contest.created_by or user in contest.moderators.all()):
        if problem.is_public:
            if user.has_perm('problem.change_problem'):
                is_admin = True    
        elif not problem.is_public:
            is_admin = True

    if not is_admin:
        if now < contest.start_time:
            return HttpResponse("The contest hasn't started yet!", status=403)

        if now >= contest.start_time and now <= contest.end_time and user not in contest.participants.all():
            return HttpResponse('You are not a participant of this contest', status=403)


    testcases = problem.testcases.filter(is_hidden=False)

    language_id = '71'
    language_name = LANGUAGES[language_id]

    if request.method == 'POST':
        now = timezone.now()

        language_id = request.POST.get('language_id')
        source_code = request.POST.get('source_code')

        current_submission = Submission.objects.create(
            user=request.user,
            problem=problem,
            code=source_code,
            language=language_id
        )

        if not is_admin and now >= contest.start_time and now <= contest.end_time and user in contest.participants.all():
            current_submission.contest = contest
            current_submission.save()

        code_submission.delay(current_submission.id)

        if is_admin:
            return redirect('submission')
        else:
            return redirect('contest-page', id=contest_id)
        
    context = {
        'is_admin': is_admin,
        'problem': problem,
        'contest_id': contest.id,
        'testcases': testcases,
        'language_id': language_id,
        'language_name': language_name,
    }

    return render(request, 'problem/problem_detail.html', context)




@login_required(login_url='/accounts/google/login/')
def contest_submissions_api(request, contest_id):
    user=request.user
    contest = get_object_or_404(Contest, id=contest_id)
    submissions = Submission.objects.filter(user=user, contest=contest).order_by('-submitted_at')
    
    data = []

    for sub in submissions:
        data.append({
            "submission_id": sub.id,
            "problem_title": sub.problem.title,
            "problem_id": sub.problem.id,
            "contest_id": sub.contest.id,
            "status": sub.verdict,
            "language": LANGUAGES[sub.language],
            "submitted_at": sub.submitted_at.strftime("%Y-%m-%d %H:%M:%S"),
            "execution_time": sub.execution_time,
            "memory_used": sub.memory_used,
            "total_testcases": sub.total_testcases,
            "passed_testcases": sub.passed_testcases
        })
        
    return JsonResponse({"submissions": data})


# Work Left
@login_required(login_url='/accounts/google/login/')
def contest_submission_details(request, contest_id, submission_id):
    user=request.user
    contest = get_object_or_404(Contest, id=contest_id)
    submission = get_object_or_404(Submission, id=submission_id, user=user, contest=contest)

    context = {
        'problem_id': submission.problem.id,
        'problem_name': submission.problem.title,
        'contest_id': contest.id,
        'source_code': submission.code,
        'language': LANGUAGES[submission.language],
        'execution_time': submission.execution_time,
        'memory_used': submission.memory_used,
        'verdict': submission.verdict,
        # 'testcase_details': submission.testcase_details,
        'passed_testcases': submission.passed_testcases,
        'total_testcases': submission.total_testcases,
    }

    return render(request, 'problem/submission_details.html', context)



@login_required(login_url='/accounts/google/login/')
def create_contest_problem(request, contest_id):
    user = request.user
    contest = get_object_or_404(Contest, id=contest_id)

    if (user.is_staff or user == contest.created_by or user in contest.moderators.all()):
        problem_type = 'contest'
        problem = None

        if request.method == 'POST':
            title = request.POST.get('title')
            statement = request.POST.get('statement')
            problem_input = request.POST.get('problem_input')
            problem_output = request.POST.get('problem_output')
            note = request.POST.get('note')
            difficulty = request.POST.get('difficulty')
            time_limit = request.POST.get('time_limit')
            memory_limit = request.POST.get('memory_limit')

            # All actions are discarded if the creation of either the problem or the testcase object fails.
            with transaction.atomic():
                problem = Problem.objects.create(
                    title=title,
                    statement=statement,
                    problem_input=problem_input,
                    problem_output=problem_output,
                    note=note,
                    difficulty=difficulty,
                    time_limit=time_limit,
                    memory_limit=memory_limit,
                    created_by=request.user,
                    is_public=False
                )

                testcases = json.loads(request.POST.get('testcases'))

                testcase_objects = []

                for testcase in testcases:
                    testcase_object = TestCase(
                        problem=problem,
                        input_data=testcase['testcase_input'],
                        expected_output=testcase['testcase_output'],
                        is_hidden=testcase['hidden_testcase']
                    )

                    testcase_objects.append(testcase_object)

                TestCase.objects.bulk_create(testcase_objects)

            if problem:
                contest.problems.add(problem)
                return redirect('contest-page', contest.id)
        

        context = {
            'problem_type': problem_type,
            'contest': contest,
        }

        return render(request, 'problem/create_problem.html', context)
    else:
        return HttpResponse('Permission denied')
    




@login_required(login_url='/accounts/google/login/')
def edit_contest_problem(request, problem_id):
    user = request.user
    current_problem = Problem.objects.get(id=problem_id)

    if current_problem.is_public:
        return HttpResponse('Permission Denied')

    current_testcases = current_problem.testcases.all()
    contest = current_problem.contests.first()

    if (user.is_staff or user == contest.created_by or user in contest.moderators.all()):
        problem_type = 'contest'
        
        if request.method == 'POST':
            title = request.POST.get('title')
            statement = request.POST.get('statement')
            problem_input = request.POST.get('problem_input')
            problem_output = request.POST.get('problem_output')
            note = request.POST.get('note')
            difficulty = request.POST.get('difficulty')
            time_limit = request.POST.get('time_limit')
            memory_limit = request.POST.get('memory_limit')

            testcases = json.loads(request.POST.get('testcases'))

            # All actions are discarded if the creation of either the problem or the testcase object fails.
            with transaction.atomic():
                current_problem.title=title
                current_problem.statement=statement
                current_problem.problem_input=problem_input
                current_problem.problem_output=problem_output
                current_problem.note=note
                current_problem.difficulty=difficulty
                current_problem.time_limit=time_limit
                current_problem.memory_limit=memory_limit
                current_problem.save()

                current_problem.testcases.all().delete()

                testcase_objects = []

                for testcase in testcases:
                    testcase_object = TestCase(
                        problem=current_problem,
                        input_data=testcase['testcase_input'],
                        expected_output=testcase['testcase_output'],
                        is_hidden=testcase['hidden_testcase']
                    )

                    testcase_objects.append(testcase_object)

                TestCase.objects.bulk_create(testcase_objects)

            if current_problem:
                return redirect('problem-detail', current_problem.id)
            

        context = {
            'problem_type': problem_type,
            'current_problem': current_problem,
            'current_testcases': current_testcases,
        }

        return render(request, 'problem/edit_problem.html', context)
    else:
        return HttpResponse('Permission denied')
    


@login_required(login_url='/accounts/google/login/')
def delete_contest_problem(request, problem_id):
    user = request.user
    problem = get_object_or_404(Problem, id=problem_id)
    if problem.is_public:
        return HttpResponse('Permission Denied')
    
    contest = problem.contests.first()

    if (user.is_staff or user == contest.created_by or user in contest.moderators.all()):
        if request.method == 'POST':
            problem.delete()

            return redirect('contest-page', contest.id)
    
        context = {
            'item' : problem.title,
        }

        return render(request, 'home/delete.html', context)
    else:
        return HttpResponse('Permission denied')