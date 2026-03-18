from django.urls import path
from . import views

urlpatterns = [
    path('', views.problems, name='problems'),
    path('create_problem/', views.create_problem, name='create-problem'),
    path('problem_detail/<str:id>/', views.problem_detail, name='problem-detail'),
    path('submission/', views.submission, name='submission'),
    path('api/submission/', views.submissions_api, name='submission-api'),
]
