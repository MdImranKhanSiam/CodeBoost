from django.contrib import admin
from . models import CodeSnippet, UserProfile, Notification, EmailTemplate

# Register your models here.

admin.site.register(CodeSnippet)
admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(EmailTemplate)