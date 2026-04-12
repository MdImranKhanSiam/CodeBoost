from django.urls import path
from . import views

urlpatterns = [
    path('', views.problems, name='problems'),
    path('create_problem/', views.create_problem, name='create-problem'),
    path('edit_problem/<str:problem_id>', views.edit_problem, name='edit-problem'),
    path('problem_detail/<str:id>/', views.problem_detail, name='problem-detail'),
    path('submission/', views.submission, name='submission'),
    path('api/submission/', views.submissions_api, name='submission-api'),
    path('submission_details/<str:id>/', views.submission_details, name='submission-details'),
    path('language_snippet/', views.language_snippet, name='language-snippet'),

]
