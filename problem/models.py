from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Problem(models.Model):
    DIFFICULTY_LEVEL = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('challenging', 'Challenging'),
    ]

    title = models.CharField(max_length=255)
    # slug = models.SlugField(unique=True)
    statement = models.TextField()
    problem_input = models.TextField()
    problem_output = models.TextField()
    note = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=55, choices=DIFFICULTY_LEVEL, default='easy')
    time_limit = models.FloatField(default=1.0)
    memory_limit = models.FloatField(default=512)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['difficulty']),
            models.Index(fields=['created_at']),
        ]



# In production, store testcases in filesystem or object storage, not DB (better performance)
class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="testcases")
    input_data = models.TextField()
    expected_output = models.TextField()
    is_hidden = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Submission(models.Model):
    # VERDICT_CHOICES = [
    #     ('PENDING', 'Pending'),
    #     ('RUNNING', 'Running'),
    #     ('AC', 'Accepted'),
    #     ('WA', 'Wrong Answer'),
    #     ('TLE', 'Time Limit Exceeded'),
    #     ('MLE', 'Memory Limit Exceeded'),
    #     ('RE', 'Runtime Error'),
    #     ('CE', 'Compilation Error'),
    # ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    # Get all submissions of a user
    # user.submissions.all()

    # Get user submissions in a contest
    # contest.submissions.filter(user=user)

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="submissions")
    # Get submissions of a problem
    # problem.submissions.all()
    # problem.submissions.filter(verdict='AC')

    contest = models.ForeignKey("contest.Contest", on_delete=models.CASCADE, null=True, blank=True, related_name="submissions")
    # Get submissions in a contest
    # contest.submissions.all()

    code = models.TextField()
    language = models.CharField(max_length=50)
    total_testcases = models.IntegerField(default=0)
    passed_testcases = models.IntegerField(default=0)
    testcase_details = models.JSONField(default=list)
    # verdict = models.CharField(max_length=55, choices=VERDICT_CHOICES, default='PENDING')
    verdict = models.CharField(max_length=60, default='Pending')
    execution_time = models.FloatField(null=True, blank=True, default=0)
    memory_used = models.IntegerField(null=True, blank=True, default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)


    class Meta:
        indexes = [
            models.Index(fields=['user', '-submitted_at']),
            # Submission.objects.filter(user=user).order_by("-submitted_at")
            
            models.Index(fields=['problem', 'verdict']),
            # Submission.objects.filter(problem=problem, verdict="accepted")


            #Contest-based queries

            models.Index(fields=['contest', '-submitted_at']),
            # Submission.objects.filter(contest=contest).order_by('-submitted_at')

            models.Index(fields=['contest', 'user', 'problem', 'submitted_at'])
            # Submission.objects.filter(contest=contest, user=user, problem=problem).order_by('submitted_at')

            # models.Index(fields=['contest', 'user']),
            # Submission.objects.filter(contest=contest, user=request.user)

            # models.Index(fields=['contest', 'problem']),
            # Submission.objects.filter(contest=contest, problem=problem)

            # models.Index(fields=['contest', 'verdict']),
            # Submission.objects.filter(contest=contest, user=user, problem=problem)

            # models.Index(fields=['contest', 'problem', 'verdict']),
            # Submission.objects.filter(contest=contest, problem=problem, verdict='AC')

        ]


    def __str__(self):
        return f'{self.user.username} {self.language}'
