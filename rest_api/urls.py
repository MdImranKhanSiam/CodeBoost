from django.urls import path
from . import views

urlpatterns = [
    path('contest_leaderboard/', views.contest_leaderboard),
    
]
