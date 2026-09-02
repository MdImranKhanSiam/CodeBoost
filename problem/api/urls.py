from django.urls import path
from . import views

urlpatterns = [
    path('languages/', views.languages),
    path('ai/explain/<str:problem_id>/', views.ai_explain),
    path('ai/review/<str:problem_id>/', views.ai_review),
]
