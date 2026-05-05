from django.urls import path
from . import views

urlpatterns = [
    path('<str:user_id>/', views.user_profile, name='user-profile'),
]
