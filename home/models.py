from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.

class CodeSnippet(models.Model):
    title = models.CharField(max_length=200)
    code = models.TextField()  # This can store very long strings
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class EmailTemplate(models.Model):
    EMAIL_TYPES = [
        ('welcome', 'Welcome Email'),
        ('contest_starting', 'Contest Starting Email'),
        ('contest_ended', 'Contest Ended Email'),
    ]

    email_type = models.CharField(max_length=50, choices=EMAIL_TYPES, unique=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_email_type_display()



    


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('submission', 'Submission'),
        ('contest', 'Contest'),
        ('system', 'System'),
        ('message', 'Message'),
    ]

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user_notifications = Notification.objects.filter(user=request.user)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    # user = request.user
    # user.notifications.all()           # all notifications
    # user.notifications.filter(is_read=False)  # unread notifications

    content = models.TextField()
    type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, default='system')
    link = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    # user.notifications.order_by('-created_at')[:10]  # latest 10 notifications

    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]





class SubmitTicket(models.Model):
    TICKET_STATUS = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_tickets')
    # Get all submitted tickets of a user
    # user.submitted_tickets.all()

    title = models.CharField(max_length=255)
    details = models.TextField()
    photos = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=30, choices=TICKET_STATUS, default='pending')
    admin_reply = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.user.email}"
    




class FeedbackAndSuggestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_feedbacks')
    # Get all submitted feedbacks of a user
    # user.submitted_feedbacks.all()

    details = models.TextField()
    photos = models.JSONField(default=list, blank=True)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    admin_reply = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback #{self.id} - {self.user.email}"