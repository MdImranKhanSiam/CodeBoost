from django.urls import path
from . import views

urlpatterns = [
    path('', views.contests, name='contests'),
    path('create_contest/', views.create_contest, name='create-contest'),
]
