from django.contrib import admin
from . models import CodeSnippet, Notification, EmailTemplate

# Register your models here.

admin.site.register(CodeSnippet)
admin.site.register(Notification)
admin.site.register(EmailTemplate)