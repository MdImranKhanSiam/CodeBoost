import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.db import transaction
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from django_ratelimit.decorators import ratelimit
from . models import Problem, TestCase, Submission
from . background_task import code_submission
from . languages import LANGUAGES, LANGUAGE_SNIPPETS



def problems(request):
    problems = Problem.objects.filter(is_public=True)
    
    context = {
        'problems': problems,
    }

    return render(request, 'problem/problems.html', context)





@ratelimit(key='user', rate='6/m', method='POST', block=True)
@login_required(login_url='/accounts/google/login/')
def problem_detail(request, id):
    username = request.user.userprofile.display_name
    problem = Problem.objects.get(id=id)
    testcases = problem.testcases.filter(is_hidden=False)

    language_id = '71'
    language_name = LANGUAGES[language_id]

    if request.method == 'POST':
        language_id = request.POST.get('language_id')
        source_code = request.POST.get('source_code')

        current_submission = Submission.objects.create(
            user=request.user,
            problem=problem,
            code=source_code,
            language=language_id
        )

        code_submission.delay(current_submission.id)

        return redirect('submission')
        
    context = {
        'problem': problem,
        'testcases': testcases,
        'language_id': language_id,
        'language_name': language_name,
    }

    return render(request, 'problem/problem_detail.html', context)



@login_required(login_url='/accounts/google/login/')
def language_snippet(request):
    language_id = request.GET.get('language_id')
    user_name = request.user.userprofile.display_name
    snippet = LANGUAGE_SNIPPETS[language_id].format(name=user_name)

    return JsonResponse({
        'snippet': snippet,
    })



@permission_required('problem.add_problem', raise_exception=True)
@login_required(login_url='/accounts/google/login/')
def create_problem(request):
    problem_type = 'public'
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

        testcases = json.loads(request.POST.get('testcases'))

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
                created_by=request.user
            )

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
            return redirect('problem-detail', problem.id)
        

    context = {
        'problem_type': problem_type,
    }

    return render(request, 'problem/create_problem.html', context)



@permission_required('problem.change_problem', raise_exception=True)
@login_required(login_url='/accounts/google/login/')
def edit_problem(request, problem_id):
    problem_type = 'public'
    problem = None
    current_problem = Problem.objects.get(id=problem_id)
    current_testcases = current_problem.testcases.all()

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



@login_required(login_url='/accounts/google/login/')
def submission(request):
    context = {

    }

    return render(request, 'problem/submission.html', context)





@login_required(login_url='/accounts/google/login/')
def submissions_api(request):
    submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    
    data = []

    for sub in submissions:
        data.append({
            "submission_id": sub.id,
            "problem_title": sub.problem.title,
            "problem_id": sub.problem.id,
            "status": sub.verdict,
            "language": LANGUAGES[sub.language],
            "submitted_at": sub.submitted_at.strftime("%Y-%m-%d %H:%M:%S"),
            "execution_time": sub.execution_time,
            "memory_used": sub.memory_used,
            "total_testcases": sub.total_testcases,
            "passed_testcases": sub.passed_testcases
        })
        
    return JsonResponse({"submissions": data})



@login_required(login_url='/accounts/google/login/')
def submission_details(request, id):
    submission = get_object_or_404(Submission, id=id, user=request.user)

    context = {
        'problem_id': submission.problem.id,
        'problem_name': submission.problem.title,
        'source_code': submission.code,
        'language': LANGUAGES[submission.language],
        'execution_time': submission.execution_time,
        'memory_used': submission.memory_used,
        'verdict': submission.verdict,
        'testcase_details': submission.testcase_details,
        'passed_testcases': submission.passed_testcases,
        'total_testcases': submission.total_testcases,
    }

    return render(request, 'problem/submission_details.html', context)



