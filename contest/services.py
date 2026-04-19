from problem.models import Submission


# score = [
#     {"solved": 3, "penalty": 245},
#     ...
# ]

# sorted(score, key=lambda x: (-x["solved"], x["penalty"]))



# rank = [
#     'participant_id': {
#         'solved': solved,
#         'penalty': penalty,
#         'solved_problems_ids': [3,56,6]
#     },
#     'participant_id': {
#         'solved': solved,
#         'penalty': penalty
#     },
#     'participant_id': {
#         'solved': solved,
#         'penalty': penalty
#     }
#     .
#     .
#     .
# ]




def contest_rank(contest, problems, participants):
    rank = []

    for participant in participants:
        solved_problems_and_penalty = []

        for problem in problems:
            submissions = Submission.objects.filter(contest=contest, user=participant, problem=problem).order_by('submitted_at')

            print(f'Participant Name: {participant.userprofile.display_name}\nId: {participant.id}')

            for submission in submissions:
                print(submission.id)
                print(submission.contest)
                print(submission.problem)

        break
