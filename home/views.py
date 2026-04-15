from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from . models import CodeSnippet

def home(request):
    code_snippet = CodeSnippet.objects.get(title='Welcome to competitive programming')
    
    context = {
        'code_snippet' : code_snippet,
    }

    return render(request, 'home/home.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')

