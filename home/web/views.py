import json, cloudinary.uploader
from django.http import HttpResponse, JsonResponse
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.models import User
from django.db.models import Q
from home.models import CodeSnippet, SubmitTicket, FeedbackAndSuggestions
from problem.models import Problem, Submission
from contest.models import Contest
from user_profile.models import UserProfile
from home.tasks import check_rate_limit
from home.forms import RegisterForm


from . cache import get_homepage, set_homepage, invalidate_homepage




@ratelimit(key='user_or_ip', rate='100/m', method='GET', block=True)
def home(request):
    context = get_homepage()

    if not context:
        code_snippet = CodeSnippet.objects.get(title='Welcome to competitive programming')
        active_coders = UserProfile.objects.count()
        total_problems = Problem.objects.count()
        total_submissions = Submission.objects.count()
        total_contests = Contest.objects.count()

        context = {
            'code_snippet' : {
                'title': code_snippet.title,
                'code': code_snippet.code
            },

            'active_coders': active_coders,
            'total_problems': total_problems,
            'total_submissions': total_submissions,
            'total_contests': total_contests,
        }

        set_homepage(context)

    return render(request, 'home/home.html', context)




@ratelimit(key='user_or_ip', rate='100/m', method='GET', block=True)
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
            login(request, current_user, backend='django.contrib.auth.backends.ModelBackend')
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




@ratelimit(key='user_or_ip', rate='100/m', method='GET', block=True)
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



@ratelimit(key='user_or_ip', rate='100/m', method='GET', block=True)
def terms_of_service(request):
    
    return render(request, 'home/terms_of_service.html')






@ratelimit(key='user_or_ip', rate='100/m', method='GET', block=True)
def privacy_policy(request):
    
    return render(request, 'home/privacy_policy.html')









@ratelimit(key='user', rate='30/m', method='GET', block=True)
@login_required(login_url='/accounts/google/login/')
def submit_ticket(request):
    submitted = False
    ticket_id = None

    if request.method == 'POST':
        title = request.POST.get('title')
        details = request.POST.get('details')
        photos = request.FILES.getlist('photos')[:5]

        photo_urls = []

        for photo in photos:
            response = cloudinary.uploader.upload(
                photo,
                resource_type = "image"
            )

            url = response.get('secure_url')
            photo_urls.append(url)

        ticket = SubmitTicket.objects.create(
            user=request.user,
            title=title,
            details=details,
            photos=photo_urls
        )

        if ticket:
            submitted = True
            ticket_id = ticket.id


    context = {
        'submitted': submitted,
        'ticket_id': ticket_id,
    }

    return render(request, 'home/submit_ticket.html', context)






@ratelimit(key='user', rate='30/m', method='GET', block=True)
@login_required(login_url='/accounts/google/login/')
def feedback_and_suggestions(request):
    submitted = False

    if request.method == 'POST':
        rating = request.POST.get('rating')

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                rating = None
        except (TypeError, ValueError):
            rating = None

        details = request.POST.get('details')
        photos = request.FILES.getlist('photos')[:5]

        photo_urls = []

        for photo in photos:
            response = cloudinary.uploader.upload(
                photo,
                resource_type = "image"
            )

            url = response.get('secure_url')
            photo_urls.append(url)

        feedback = FeedbackAndSuggestions.objects.create(
            user=request.user,
            rating=rating,
            details=details,
            photos=photo_urls
        )

        if feedback:
            submitted = True


    context = {
        'submitted': submitted,
    }

    return render(request, 'home/feedback_and_suggestions.html', context)




@ratelimit(key='user', rate='20/m', method='GET', block=True)
@login_required(login_url='/accounts/google/login/')
def check_limit(request):
    if not request.user.has_perm("axes.add_accessattempt"):
        return HttpResponse('Not Found')

    if request.method == "POST":
        api = str(request.POST.get("api"))
        limit = int(request.POST.get("limit"))
        delay = int(request.POST.get("delay"))
    
        check_rate_limit.apply_async(
                args=[api,limit],
                countdown=delay
            )
    
        return redirect('home')

    return render(request, 'home/check_limit.html')



@ratelimit(key='user', rate='30/m', method='GET', block=True)
@login_required(login_url='/accounts/google/login/')
def logout_user(request):
    logout(request)
    return redirect('home')




@ratelimit(key='user_or_ip', rate='100/m', method='GET', block=True)
def extension1_privacy(request):

    return render(request, 'home/extension1-privacy.html')

