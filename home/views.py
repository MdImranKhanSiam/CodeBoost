from django.shortcuts import render, redirect
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from . models import UserProfile, CodeSnippet
from . forms import RegisterForm

# Create your views here.

def home(request):
    code_snippet = CodeSnippet.objects.get(title='Welcome to competitive programming')
    
    context = {
        'code_snippet' : code_snippet,
    }

    return render(request, 'home/home.html', context)

def problems(request):
    
    context = {
        
    }

    return render(request, 'home/problems.html', context)


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home') 

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            current_user = form.save(commit=False)
            current_user.username = current_user.username.lower()
            current_user.email = current_user.email.lower()
            current_user.save()

            UserProfile.objects.create(
                user = current_user,
                display_name = current_user.username,
            )
            login(request, current_user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    referer = request.META.get('HTTP_REFERER')

    if referer:
        url_parts = list(urlparse(referer))

        # To keep previous parameter

        # query = parse_qs(url_parts[4])
        # query['register'] = 'progress'
        # url_parts[4] = urlencode(query, doseq=True)


        # Clear previous parameter
        url_parts[4] = urlencode({'register': 'progress'})

        return redirect(urlunparse(url_parts))
    
    return redirect('home')











from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")  # username or email
        password = request.POST.get("password")
        
        # First try to get user by username or email
        user = None
        try:
            user_obj = User.objects.get(username=identifier)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect("home")  # change to your home URL
        else:
            messages.error(request, "Invalid username/email or password")

    return render(request, "login.html")



def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        identifier = request.POST.get("identifier", "").lower()
        password = request.POST.get('password')

        user = User.objects.filter(
            Q(username__iexact=identifier) |
            Q(email__iexact=identifier)
        ).first()

        if user:
            authentic_user = authenticate(request, username=user.username, password=password)

            if authentic_user:
                login(request, authentic_user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid Username/Email or Password')
        else:
            messages.error(request, 'User does not exist')

    referer = request.META.get('HTTP_REFERER')

    if referer:
        url_parts = list(urlparse(referer))
        url_parts[4] = urlencode({'login': 'progress'})
        return redirect(urlunparse(url_parts))
    
    return redirect('home')
























@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')
