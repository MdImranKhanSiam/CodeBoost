from django.urls import path
from . import views

urlpatterns = [
    path('<str:user_id>/', views.user_profile, name='user-profile'),
    path('authored_problems/<str:user_id>/', views.authored_problems, name='authored-problems'),
]
