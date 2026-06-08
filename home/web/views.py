import json, cloudinary.uploader
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.models import User
from home.models import CodeSnippet, SubmitTicket, FeedbackAndSuggestions
from problem.models import Problem, Submission
from contest.models import Contest
from user_profile.models import UserProfile
from home.tasks import check_rate_limit


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

    api = str(request.GET.get("api"))
    limit = int(request.GET.get("limit"))
    delay = int(request.GET.get("delay"))
    
    check_rate_limit.apply_async(
            args=[api,limit],
            countdown=delay
        )
    
    return redirect('home')




@ratelimit(key='user', rate='30/m', method='GET', block=True)
@login_required(login_url='/accounts/google/login/')
def logout_user(request):
    logout(request)
    return redirect('home')




