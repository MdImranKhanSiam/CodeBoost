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
    time_limit = models.IntegerField(default=1)
    memory_limit = models.IntegerField(default=512)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)
    total_testcases = models.IntegerField(default=0)
    passed_testcases = models.IntegerField(default=0)
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

            models.Index(fields=['user']),
            # Submission.objects.filter(user=request.user)

            models.Index(fields=['problem']),
            # Submission.objects.filter(problem=problem)
        ]
