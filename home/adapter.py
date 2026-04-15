from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.mail import send_mail
from . models import UserProfile, EmailTemplate

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
                sender='CodeBoost <noreply@gmail.com>'
                receiver=user.email

                send_mail(
                    subject,
                    message,
                    sender,
                    [receiver],
                    fail_silently=False,
                )

        return user
