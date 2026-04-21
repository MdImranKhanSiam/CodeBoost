from problem.models import Submission

def contest_rank(contest, problems, participants):
    rank = []
    overallStatus = {}

    for problem in problems:
        overallStatus[problem.id] = {
            'solved': 0,
            'attempted': 0
        }

    for participant in participants:
        solved_problems_and_penalties = []

        for problem in problems:
            solved = False
            penalty_per_wrong_answer = 20*60*1000
            penalty = 0
            attempts = 0
            solved_timestamp = 0

            submissions = Submission.objects.filter(contest=contest, user=participant, problem=problem).order_by('submitted_at')

            for submission in submissions:
                attempts += 1

                if submission.verdict == 'Accepted':
                    solved = True
                    submission_delay = submission.submitted_at - contest.start_time
                    
                    solved_timestamp = f"{int(submission_delay.total_seconds() // 3600):02d}:{int(submission_delay.total_seconds() // 60 % 60):02d}"

                    submission_delay = int(submission_delay.total_seconds() * 1000)
                    penalty += submission_delay
                    
                    break
                else:
                    penalty += penalty_per_wrong_answer

            if solved:
                solved_problems_and_penalties.append(
                    {
                        'problem': problem,
                        'penalty': penalty,
                        'attempts': attempts,
                        'solved_timestamp': solved_timestamp
                    }
                )

                overallStatus[problem.id]['solved'] += 1
            else:
                solved_problems_and_penalties.append(
                    {
                        'problem': problem,
                        'attempts': attempts
                    }
                )
            
            if attempts > 0:
                overallStatus[problem.id]['attempted'] += 1

        total_penalty = sum(item.get('penalty', 0) for item in solved_problems_and_penalties)
        total_penalty_in_minutes = int(total_penalty/60000)
        total_solved = sum(1 for item in solved_problems_and_penalties if item.get('solved_timestamp', 0))

        rank.append(
            {
                'participant': participant,
                'total_solved': total_solved,
                'total_penalty': total_penalty,
                'total_penalty_in_minutes': total_penalty_in_minutes,
                'solved_problems_and_penalties': solved_problems_and_penalties
            }
        )

    rank = sorted(rank, key=lambda x: (-x["total_solved"], x["total_penalty"]))

    return rank, overallStatus