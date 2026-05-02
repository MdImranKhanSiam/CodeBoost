from celery import shared_task
from . models import Submission
import requests

def normalize_line_endings(code):
    if code is None:
        return ""
    
    return code.replace('\r\n', '\n')



@shared_task(ignore_result=True)
def code_submission(submission_id):
    submission = Submission.objects.get(id=submission_id)
    source_code = submission.code
    language_id = submission.language
    problem = submission.problem
    all_testcases = problem.testcases.all()
    total_testcases = 0
    passed_testcases = 0
    execution_time = 0.0
    memory_used = 0.0
    final_verdict = 'Invalid'
    testcase_details = []

    url = f'http://192.168.95.128:2358/submissions/?base64_encoded=false&wait=true'

    headers = {
        "Content-Type": "application/json"
    }

    for testcase in all_testcases:
        given_input = testcase.input_data
        given_input = normalize_line_endings(given_input)

        expected_output = testcase.expected_output
        expected_output = normalize_line_endings(expected_output)

        payload = {
            "source_code": source_code,
            "language_id": language_id,
            "stdin": given_input,
            "cpu_time_limit": problem.time_limit,
            "memory_limit": problem.memory_limit * 1000,
        }

        # print(payload)

        try:
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
        except Exception:
            final_verdict = 'Internal Error'
            break

        # print(data)

        total_testcases += 1

        status = data.get('status', {}).get('description')

        time = float(data.get('time') or 0)
        memory = float(data.get('memory') or 0)

        execution_time = max(execution_time, time)
        memory_used = max(memory_used, memory)


        if status != 'Accepted':
            final_verdict = status or 'Invalid'

            testcase_details.append(
                {
                    "id": testcase.id,
                    "input": given_input,
                    "expected_output": expected_output,
                    "status": final_verdict,
                    "time": time,
                    "memory": memory,
                }
            )

            break

        current_output = data['stdout']
        current_output = normalize_line_endings(current_output)
        
            
        if current_output == expected_output:
            final_verdict = 'Accepted'
            passed_testcases += 1
        else:
            final_verdict = 'Wrong Answer'

        testcase_details.append(
            {
                "id": testcase.id,
                "input": given_input,
                "expected_output": expected_output,
                "output": current_output,
                "status": final_verdict,
                "time": time,
                "memory": memory,
            }
        )
            
        

    if final_verdict == 'Accepted':
        if passed_testcases < total_testcases:
            final_verdict = 'Wrong Answer'

    submission.total_testcases = total_testcases
    submission.passed_testcases = passed_testcases
    submission.testcase_details = testcase_details
    submission.execution_time = execution_time
    submission.memory_used = memory_used
    submission.verdict = final_verdict

    if final_verdict == 'Accepted':
        users_profile = submission.user.userprofile
        users_profile.solved_problems.add(submission.problem)
        users_profile.solved_count=users_profile.solved_problems.count()
        users_profile.save()

    submission.save()       





# celery -A CodeBoost worker --loglevel=info --pool=threads