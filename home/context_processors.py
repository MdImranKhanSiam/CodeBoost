from . forms import RegisterForm

def global_forms(request):
    user_form = RegisterForm()

    context = {
        'user_form' : user_form,
    }

    return context