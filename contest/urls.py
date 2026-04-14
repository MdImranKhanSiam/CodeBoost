from django.urls import path
from . import views

urlpatterns = [
    path('', views.contests, name='contests'),
    path('create_contest/', views.create_contest, name='create-contest'),
    path('create_contest_problem/<str:contest_id>', views.create_contest_problem, name='create-contest-problem'),
    path('edit_contest_problem/<str:problem_id>', views.edit_contest_problem, name='edit-contest-problem'),
    path('delete_contest_problem/<str:problem_id>', views.delete_contest_problem, name='delete-contest-problem'),
    path('contest_page/<str:id>/', views.contest_page, name='contest-page'),
    path('contest_registration/<str:id>/', views.contest_registration, name='contest-registration'),
]
