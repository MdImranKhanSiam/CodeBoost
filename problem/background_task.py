from celery import shared_task
from . models import Submission
import requests


@shared_task
def code_submission(submission_id):
    submission = Submission.objects.get(id=submission_id)
    source_code = submission.code
    language_id = submission.language
    problem = submission.problem
    all_testcases = problem.testcases.all()
    total_testcases = 0
    passed_testcases = 0
    result = None

    url = f'https://ce.judge0.com/submissions/?base64_encoded=false&wait=true'

    headers = {
        "Content-Type": "application/json"
    }

    for testcase in all_testcases:
        total_testcases += 1
        print(testcase.input_data)
        print(testcase.expected_output)

        payload = {
            "source_code": source_code,
            "language_id": language_id,
            "stdin": testcase.input_data
        }

        response = requests.post(url, json=payload, headers=headers)

        data = response.json()

        if data['status']['description'] == 'Accepted':
            current_output = data['stdout'].strip()
            expected_output = testcase.expected_output.strip()

            print(f'Current Output: {current_output}')

            print(f'stdout: {current_output}')
            print(f'expected: {expected_output}')
            
            if current_output == testcase.expected_output:
                result = 'AC'
                passed_testcases += 1
            else:
                result = 'WA'
        else:
            result = data['status']['description']

        print(result)

    submission.total_testcases = total_testcases
    submission.passed_testcases = passed_testcases
    submission.verdict = result
    submission.save()














            