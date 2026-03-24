from django.db import models
from django.contrib.auth.models import User


class Contest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    registration_deadline = models.DateTimeField(null=True, blank=True)

    problems = models.ManyToManyField("problem.Problem", related_name="contests")
    # problem.contests.all() #To find all contest this problem instance belong to
    # problem.contest_set.all() #If no related name is set

    # Assume problem_ids is a list of integers from POST data
    # e.g., request.POST.getlist('problems') = ['1','2','3']
    # problem_ids = request.POST.getlist('problems')
    
    # contest = get_object_or_404(Contest, id=contest_id)
    # Fetch Problem instances
    # problems = Problem.objects.filter(id__in=problem_ids)
    
    # Add problems to contest
    # contest.problems.add(*problems)  # * unpacks the list

    # .add(*problems) → adds multiple problems at once.

    # .set(problems) → replaces existing problems with the new list.

    # .remove(problem) → removes a problem.

    # All problems of this contest
    # problems = contest.problems.all()

    participants = models.ManyToManyField(User,related_name="joined_contests", blank=True)
    # user.joined_contests.all()

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_contests", null=True)
    # user.created_contests.all()

    moderators = models.ManyToManyField(User, related_name="moderator_of_contests", blank=True)
    # user.moderator_of_contests.all()
    
    created_at = models.DateTimeField(auto_now_add=True)
