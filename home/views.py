from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from . models import CodeSnippet
from . cache import get_homepage, set_homepage, invalidate_homepage

def home(request):
    context = get_homepage()

    if not context:
        code_snippet = CodeSnippet.objects.get(title='Welcome to competitive programming')
    
        context = {
            'code_snippet' : {
                'title': code_snippet.title,
                'code': code_snippet.code
            },
        }

        set_homepage(context)

    return render(request, 'home/home.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')

