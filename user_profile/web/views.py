from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit


@ratelimit(key='user', rate='30/m', method='GET', block=True)
@login_required(login_url='login')
def user_profile(request, user_id):

    context = {
        'user_id': user_id,
    }

    return render(request, 'user_profile/user_profile.html', context)