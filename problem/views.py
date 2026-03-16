from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.db import transaction
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from . models import Problem, TestCase


def problems(request):
    problems = Problem.objects.all()
    
    context = {
        'problems': problems,
    }

    return render(request, 'problem/problems.html', context)


@login_required(login_url='/accounts/google/login/')
def problem_detail(request, id):
    problem = Problem.objects.get(id=id)
    testcases = problem.testcases.filter(is_hidden=False)

    language_id = None #Use users preferred language
    source_code = f'Welcome {request.user.userprofile.display_name}\nWrite your code here'
    stdin = None
    stdout = None

    if request.method == 'POST':
        language_id = request.POST.get('language_id')
        source_code = request.POST.get('source_code')
        stdin = request.POST.get('stdin')
        stdout = request.POST.get('stdout')

        print('Got it')
        print(language_id)
        print(source_code)
        print(stdin)
        print(stdout)

        # referer = request.META.get('HTTP_REFERER')

        # if referer:
        #     url_parts = list(urlparse(referer))
        #     url_parts[4] = urlencode({'submission': 'progress'})
        #     return redirect(urlunparse(url_parts))
        

    context = {
        'problem': problem,
        'testcases': testcases,
        'language_id': language_id,
        'source_code': source_code,
        'stdin': stdin,
        'stdout': stdout
    }

    return render(request, 'problem/problem_detail.html', context)




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



def submission(request):
    return HttpResponse('Submission')
