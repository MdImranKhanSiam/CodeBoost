# from . forms import RegisterForm

# def global_forms(request):
#     user_form = RegisterForm()

#     context = {
#         'user_form' : user_form,
#     }

#     return context


from user_profile.models import UserProfile
from django.shortcuts import get_object_or_404
from . cache import get_user_data, set_user_data, invalidate_user_data

def user_data(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return {}

    user_id = request.user.id
    
    data = get_user_data(user_id)

    if not data:
        user_profile = get_object_or_404(UserProfile, user_id=user_id)

        data = {
            'user_id': user_id,
            'display_name': user_profile.display_name,
            'avatar': user_profile.avatar,
            'preferred_language': user_profile.preferred_language,
            'date_of_birth': user_profile.date_of_birth,
        }

        set_user_data(user_id, data)

    return data