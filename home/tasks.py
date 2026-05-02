from celery import shared_task
from django.core.mail import EmailMessage


@shared_task(ignore_result=True)
def send_welcome_email(subject,message,sender,receiver):
    email = EmailMessage(
        subject,
        message,
        sender,
        [receiver]
    )

    email.content_subtype = "html"
    email.send(fail_silently=True)