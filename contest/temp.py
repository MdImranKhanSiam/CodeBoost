
@ratelimit(key='user', rate='6/m', method='POST', block=True)
@login_required(login_url='/accounts/google/login/')
def problem_detail(request, problem_id, contest_id=None):
    user = request.user
    problem = get_object_or_404(Problem, id=problem_id)
    testcases = problem.testcases.filter(is_hidden=False)
    contest = None

    if contest_id:
        contest = get_object_or_404(Contest, id=contest_id)

    is_admin = False

    if problem.is_public:
        if user.has_perm('problem.change_problem'):
            is_admin = True
    elif not problem.is_public:
        contest = problem.contests.first()

        if (user.is_staff or user == contest.created_by or user in contest.moderators.all()):
            is_admin = True

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

        if contest:
            now = timezone.now()

            if now >= contest.start_time and now <= contest.end_time and user in contest.participants.all():
                current_submission.contest = contest
                current_submission.save()

        code_submission.delay(current_submission.id)

        if contest:
            return redirect('contest-page', id=contest_id)

        return redirect('submission')
        
    context = {
        'is_admin': is_admin,
        'problem': problem,
        'testcases': testcases,
        'language_id': language_id,
        'language_name': language_name,
    }

    return render(request, 'problem/problem_detail.html', context)

