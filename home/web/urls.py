from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('terms_of_service/', views.terms_of_service, name='terms-of-service'),
    path('privacy_policy/', views.privacy_policy, name='privacy-policy'),
    
]
