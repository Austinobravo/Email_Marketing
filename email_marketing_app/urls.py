from django.urls import path
from .views import custom_message, success, error, visitor_count

urlpatterns = [
    path('', custom_message, name='home'),
    path('success/', success, name='success'),
    path('error/', error, name='error'),
     path('visitor-count/', visitor_count, name='visitor_count'),
]