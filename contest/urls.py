from django.urls import path
from . import views

urlpatterns = [
    path('', views.contests, name='contests'),
    path('create_contest/', views.create_contest, name='create-contest'),
    path('create_contest_problem/<str:contest_id>', views.create_contest_problem, name='create-contest-problem'),
    path('contest_page/<str:id>/', views.contest_page, name='contest-page'),
    path('contest_registration/<str:id>/', views.contest_registration, name='contest-registration'),
]
