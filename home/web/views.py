import json
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
@login_required(login_url='login')
def submit_ticket(request):
    if request.method == 'GET':
        return render(request, 'home/submit_ticket.html')
 
    if request.method == 'POST':
        return _handle_ticket_post(request)
 
    return JsonResponse({'message': 'Method not allowed'}, status=405)
 
 
def _handle_ticket_post(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'message': 'Invalid request body.'}, status=400)
 
    title   = data.get('title', '').strip()
    details = data.get('details', '').strip()
    photos  = data.get('photos', [])
 
    # Validation
    if not title:
        return JsonResponse({'message': 'Title is required.'}, status=400)
    if not details:
        return JsonResponse({'message': 'Details are required.'}, status=400)
    if len(title) > 255:
        return JsonResponse({'message': 'Title must be 255 characters or fewer.'}, status=400)
    if len(details) > 5000:
        return JsonResponse({'message': 'Details must be 5000 characters or fewer.'}, status=400)
    if not isinstance(photos, list):
        photos = []
 
    try:
        ticket = SubmitTicket.objects.create(
            user=request.user,
            title=title,
            details=details,
            photos=photos[:5],   # limit to 5 photos
            status='pending',
        )
    except Exception:
        return JsonResponse({'message': 'Failed to save ticket. Please try again.'}, status=500)
 
    return JsonResponse({
        'message': 'Ticket submitted successfully.',
        'ticket_id': ticket.id,
    }, status=201)
 
 
# ─── Feedback & Suggestions ──────────────────────────────────────
 
@login_required(login_url='login')
@ratelimit(key='user', rate='30/m', method='GET', block=True)
def feedback_and_suggestions(request):
    if request.method == 'GET':
        return render(request, 'home/feedback_and_suggestions.html')
 
    if request.method == 'POST':
        return _handle_feedback_post(request)
 
    return JsonResponse({'message': 'Method not allowed'}, status=405)
 
 
def _handle_feedback_post(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'message': 'Invalid request body.'}, status=400)
 
    details = data.get('details', '').strip()
    rating  = data.get('rating', None)
    photos  = data.get('photos', [])
 
    # Validation
    if not details:
        return JsonResponse({'message': 'Feedback details are required.'}, status=400)
    if len(details) > 3000:
        return JsonResponse({'message': 'Feedback must be 3000 characters or fewer.'}, status=400)
 
    # Rating: must be 1–5 or None
    if rating is not None:
        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                rating = None
        except (ValueError, TypeError):
            rating = None
 
    if not isinstance(photos, list):
        photos = []
 
    try:
        feedback = FeedbackAndSuggestions.objects.create(
            user=request.user,
            details=details,
            rating=rating,
            photos=photos[:3],
        )
    except Exception:
        return JsonResponse({'message': 'Failed to save feedback. Please try again.'}, status=500)
 
    return JsonResponse({
        'message': 'Feedback submitted. Thank you!',
        'feedback_id': feedback.id,
    }, status=201)
 



@ratelimit(key='user', rate='30/m', method='GET', block=True)
@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')




