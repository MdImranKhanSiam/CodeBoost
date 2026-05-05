from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),

        ('female', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=200, null=True, blank=True)
    avatar = models.URLField(blank=True, null=True, default="https://res.cloudinary.com/dxd9uxsfv/image/upload/v1770963972/bjngg2xwjfd0vp69xv45.jpg")
    bio = models.TextField(max_length=1000, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=300, null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    social = models.URLField(blank=True, null=True)

    rating = models.IntegerField(default=1200, blank=True, null=True)
    solved_problems = models.ManyToManyField('problem.Problem', blank=True, null=True, related_name='solved_by')
    solved_count = models.IntegerField(default=0, blank=True, null=True)


    class Meta:
        indexes = [
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return self.user.username