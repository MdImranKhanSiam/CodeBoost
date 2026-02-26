from django.contrib import admin
from . models import CodeSnippet, UserProfile

# Register your models here.

admin.site.register(CodeSnippet)
admin.site.register(UserProfile)