from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('problems/', views.problems, name='problems'),
    path('login/', views.login_user, name='login'),
    path('registration/', views.register_user, name='registration'),
    path('logout/', views.logout_user, name='logout'),
]
