from django.urls import path
from . import views

urlpatterns = [
    path('progress_heatmap/', views.progress_heatmap),
]
