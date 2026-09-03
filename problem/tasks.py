import requests, os, time
from celery import shared_task
from . models import Submission
from . web.cache import invalidate_submission_api, invalidate_individual_current_submission_details, invalidate_user_problems_page, invalidate_submission_problem_api
from user_profile.api.cache import invalidate_user_progress_heatmap



def normalize_line_endings(code):
    if code is None:
        return ""
    
    # normalize all line ending styles to \n
    code = code.replace('\r\n', '\n').replace('\r', '\n')
    
    # strip trailing whitespace from each line
    lines = code.split('\n')
    lines = [line.rstrip() for line in lines]
    
    return '\n'.join(lines)



@shared_task(ignore_result=True, bind=True, max_retries=3, default_retry_delay=5, acks_late=True, reject_on_worker_lost=True,)
def code_submission(self, submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        source_code = submission.code
        language_id = submission.language
        problem = submission.problem
        all_testcases = list(problem.testcases.all())
        total_testcases = 0
        passed_testcases = 0
        execution_time = 0.0
        memory_used = 0.0
        final_verdict = 'Invalid'
        testcase_details = []

        url = f'http://{os.getenv("LINUX_JUDGE0_IP")}:2358/submissions/batch?base64_encoded=false'
        headers = {"Content-Type": "application/json"}

        prepared = []
        for testcase in all_testcases:
            given_input = normalize_line_endings(testcase.input_data)
            expected_output = normalize_line_endings(testcase.expected_output)
            prepared.append((testcase, given_input, expected_output))

        submissions_payload = {
            "submissions": [
                {
                    "source_code": source_code,
                    "language_id": language_id,
                    "stdin": given_input,
                    "cpu_time_limit": problem.time_limit,
                    "memory_limit": problem.memory_limit * 1000,
                }
                for (_, given_input, _) in prepared
            ]
        }

        try:
            batch_response = requests.post(
                url,
                json=submissions_payload,
                headers=headers,
            )
            tokens_data = batch_response.json()
            tokens = [item['token'] for item in tokens_data]
        except Exception:
            submission.verdict = 'Internal Error'
            submission.save()
            return

        # 2. poll until every submission is done, with a safety cap on attempts
        tokens_param = ','.join(tokens)
        results_by_token = {}
        max_polls = 600          # e.g. 60 * 0.5s = 30s max wait
        polls = 0

        while polls < max_polls:
            try:
                get_response = requests.get(
                    f'{base_url}/submissions/batch',
                    params={
                        "tokens": tokens_param,
                        "base64_encoded": "false",
                        "fields": "token,stdout,status,time,memory",
                    },
                    headers=headers,
                )
                results = get_response.json().get('submissions', [])
            except Exception:
                submission.verdict = 'Internal Error'
                submission.save()
                return

            still_pending = False
            for r in results:
                status_id = r.get('status', {}).get('id')
                if status_id in (1, 2):  # 1 = In Queue, 2 = Processing
                    still_pending = True
                results_by_token[r['token']] = r

            if not still_pending:
                break

            polls += 1
            time.sleep(0.5)
        else:
            submission.verdict = 'Internal Error'
            submission.save()
            return

        
        for (testcase, given_input, expected_output), token in zip(prepared, tokens):
            data = results_by_token.get(token, {})
            total_testcases += 1

            status = data.get('status', {}).get('description')
            exec_time = float(data.get('time') or 0)
            memory = float(data.get('memory') or 0)

            execution_time = max(execution_time, exec_time)
            memory_used = max(memory_used, memory)

            if status != 'Accepted':
                final_verdict = status or 'Invalid'
                testcase_details.append({
                    "id": testcase.id,
                    "input": given_input,
                    "expected_output": expected_output,
                    "status": final_verdict,
                    "time": exec_time,
                    "memory": memory,
                })
                break

            current_output = normalize_line_endings(data.get('stdout'))

            if current_output == expected_output:
                final_verdict = 'Accepted'
                passed_testcases += 1
            else:
                final_verdict = 'Wrong Answer'

            testcase_details.append({
                "id": testcase.id,
                "input": given_input,
                "expected_output": expected_output,
                "output": current_output,
                "status": final_verdict,
                "time": exec_time,
                "memory": memory,
            })

        if final_verdict == 'Accepted' and passed_testcases < total_testcases:
            final_verdict = 'Wrong Answer'

        submission.total_testcases = total_testcases
        submission.passed_testcases = passed_testcases
        submission.testcase_details = testcase_details
        submission.execution_time = execution_time
        submission.memory_used = memory_used
        submission.verdict = final_verdict

        user_id = submission.user.id

        if final_verdict == 'Accepted':
            users_profile = submission.user.userprofile
            users_profile.solved_problems.add(submission.problem)
            users_profile.solved_count = users_profile.solved_problems.count()
            users_profile.save()
            invalidate_user_progress_heatmap(user_id)

        submission.save()

    except Exception as exc:
        raise self.retry(exc=exc)

    time.sleep(1)
    invalidate_submission_api(user_id)
    invalidate_individual_current_submission_details(user_id, submission.id)
    invalidate_user_problems_page(user_id)
    invalidate_submission_problem_api(user_id, problem.id)





# celery -A CodeBoost worker --loglevel=info --pool=threads