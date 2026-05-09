from django.urls import path
from . import views

urlpatterns = [
    path('progress_heatmap/', views.progress_heatmap),
    path('user_profile_data/', views.user_profile_data),
    path('user_profile_update/', views.user_profile_update),
]
