from django.urls import path
from . import views

urlpatterns = [
    path('', views.contests, name='contests'),
    path('create_contest/', views.create_contest, name='create-contest'),
    path('create_private_contest/', views.create_private_contest, name='create-private-contest'),
    path('edit_contest/<str:contest_id>/', views.edit_contest, name='edit-contest'),
    path('create_contest_problem/<str:contest_id>', views.create_contest_problem, name='create-contest-problem'),
    path('edit_contest_problem/<str:problem_id>', views.edit_contest_problem, name='edit-contest-problem'),
    path('delete_contest_problem/<str:problem_id>', views.delete_contest_problem, name='delete-contest-problem'),
    path('contest_page/<str:id>/', views.contest_page, name='contest-page'),
    path('contest_problem_detail/<str:contest_id>/<str:problem_id>/', views.contest_problem_detail, name='contest-problem-detail'),
    # path('contest_submission_details/<str:contest_id>/<str:submission_id>/', views.contest_submission_details, name='contest-submission-details'),
    path('contest_submissions_api/<str:contest_id>/', views.contest_submissions_api, name='contest-submissions-api'),
    path('contest_registration/<str:id>/', views.contest_registration, name='contest-registration'),
    path('leaderboard/<str:contest_id>/', views.leaderboard, name='leaderboard'),
    path('private_contests/', views.private_contests, name='private-contests'),
]
