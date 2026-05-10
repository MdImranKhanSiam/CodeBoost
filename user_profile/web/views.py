from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from user_profile.models import UserProfile
from problem.languages import LANGUAGES

# @login_required(login_url='login')
# def user_profile(request, user_id):
#     current_user = request.user
#     target_user = User.objects.get(id=user_id)
#     target_user_profile = UserProfile.objects.get(user=target_user)

#     current_users_profile = False

#     if current_user == target_user:
#         current_users_profile = True


#     context = {
#         'target_user': target_user,
#         'current_users_profile': current_users_profile,
#     }

#     return render(request, 'user_profile/user_profile.html', context)


@login_required(login_url='login')
def user_profile(request, user_id):

    context = {
        'user_id': user_id,
    }

    return render(request, 'user_profile/user_profile.html', context)