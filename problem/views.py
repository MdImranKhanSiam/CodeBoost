from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.db import transaction
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from django_ratelimit.decorators import ratelimit
from . models import Problem, TestCase, Submission
from . background_task import code_submission
from . languages import LANGUAGES, LANGUAGE_SNIPPETS


def problems(request):
    problems = Problem.objects.all()
    
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


@login_required(login_url='/accounts/google/login/')
@permission_required('problem.add_problem', raise_exception=True)
def create_problem(request):
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

        testcase_inputs = request.POST.getlist('testcase_input[]')
        testcase_outputs = request.POST.getlist('testcase_output[]')
        testcases_hidden = request.POST.getlist('testcase_hidden[]')

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

            testcases = []

            for i in range(len(testcase_inputs)):
                hidden = False

                if str(i) in testcases_hidden:
                    hidden = True

                testcase = TestCase(
                    problem=problem,
                    input_data=testcase_inputs[i],
                    expected_output=testcase_outputs[i],
                    is_hidden=hidden
                )

                testcases.append(testcase)

            TestCase.objects.bulk_create(testcases)

        if problem:
            return redirect('problem-detail', problem.id)
        

    context = {

    }

    return render(request, 'problem/create_problem.html', context)



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



