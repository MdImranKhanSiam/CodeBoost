from django.contrib import admin
from . models import Problem, Tags, TestCase, Submission

# Register your models here.

admin.site.register(Problem)
admin.site.register(Tags)
admin.site.register(TestCase)
admin.site.register(Submission)
