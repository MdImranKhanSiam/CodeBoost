import threading
from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.mail import send_mail
from . models import UserProfile, EmailTemplate



def send_async_email(subject,message,sender,receiver):
    threading.Thread(
        target=send_mail,
        args=(subject, message, sender, [receiver]),
        kwargs={'fail_silently': True}
    ).start()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        data = sociallogin.account.extra_data

        name = data.get('name')
        avatar = data.get('picture')

        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'display_name': name,
                'avatar': avatar,
            }
        )

        if created:
            welcome_email = EmailTemplate.objects.get(email_type='welcome')

            if welcome_email.is_active:
                subject=welcome_email.subject
                message=welcome_email.message
                sender=settings.DEFAULT_FROM_EMAIL
                receiver=user.email

                send_async_email(subject,message,sender,receiver)

        return user
