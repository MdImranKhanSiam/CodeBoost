from celery import shared_task
from . models import Submission
import requests

def normalize_line_endings(code):
    if code is None:
        return ""
    
    return code.replace('\r\n', '\n')



@shared_task
def code_submission(submission_id):
    submission = Submission.objects.get(id=submission_id)
    source_code = submission.code
    language_id = submission.language
    problem = submission.problem
    all_testcases = problem.testcases.all()
    total_testcases = 0
    passed_testcases = 0
    execution_time = 0
    memory_used = 0
    result = None

    url = f'http://127.0.0.1:2358/submissions/?base64_encoded=false&wait=true'

    headers = {
        "Content-Type": "application/json"
    }

    for testcase in all_testcases:
        total_testcases += 1
        
        payload = {
            "source_code": source_code,
            "language_id": language_id,
            "stdin": testcase.input_data
        }

        response = requests.post(url, json=payload, headers=headers)

        data = response.json()

        if data['status']['description'] == 'Accepted':
            current_output = data['stdout']
            expected_output = testcase.expected_output

            # print('\n')
            # print(f'Current Output: {repr(current_output)}')
            # print(f'Expected Output: {repr(expected_output)}')

            current_output = normalize_line_endings(current_output)
            expected_output = normalize_line_endings(expected_output)

            # print('After Normalizing')

            # print('\n')
            # print(f'Current Output: {repr(current_output)}')
            # print(f'Expected Output: {repr(expected_output)}')
            
            if current_output == expected_output:
                result = 'Accepted'
                passed_testcases += 1
            else:
                result = 'Wrong Answer'
        else:
            result = data['status']['description']

        if float(data['time']) > float(execution_time):
            execution_time = float(data['time'])

        if float(data['memory']) > float(memory_used):
            memory_used = float(data['memory'])

        # print(result)

    submission.total_testcases = total_testcases
    submission.passed_testcases = passed_testcases
    submission.execution_time = float(execution_time)
    submission.memory_used = int(memory_used)
    submission.verdict = result
    submission.save()














            