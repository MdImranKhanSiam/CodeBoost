from django.urls import path
from . import views

urlpatterns = [
    path('', views.contests, name='contests'),
    path('create_contest/', views.create_contest, name='create-contest'),
    path('contest_page/<str:id>/', views.contest_page, name='contest-page'),
    path('contest_registration/<str:id>/', views.contest_registration, name='contest-registration'),
]
