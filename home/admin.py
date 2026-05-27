from django.contrib import admin
from . models import CodeSnippet, Notification, EmailTemplate, SubmitTicket, FeedbackAndSuggestions

# Register your models here.

admin.site.register(CodeSnippet)
admin.site.register(Notification)
admin.site.register(EmailTemplate)
admin.site.register(SubmitTicket)
admin.site.register(FeedbackAndSuggestions)