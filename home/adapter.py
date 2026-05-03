# import threading
from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# from django.core.mail import EmailMessage
from . models import UserProfile, EmailTemplate
from . tasks import send_welcome_email



# def send_async_email(subject,message,sender,receiver):
#     print('Inside The Send Async Email')

#     def send_html_mail():
#         print('Inside The Send HTML Mail')

#         email = EmailMessage(
#             subject,
#             message,
#             sender,
#             [receiver]
#         )

#         email.content_subtype = "html"
#         email.send(fail_silently=True)

#     threading.Thread(target=send_html_mail).start()



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
                print('Welcome Email is active')

                subject=welcome_email.subject
                message=welcome_email.message.replace("{name}", profile.display_name)
                sender=settings.DEFAULT_FROM_EMAIL
                receiver=user.email

                # send_async_email(subject,message,sender,receiver)
                send_welcome_email.delay(subject,message,sender,receiver)


        return user
