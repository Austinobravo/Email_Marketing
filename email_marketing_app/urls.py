from django.urls import path
from .views import custom_message, success, error

urlpatterns = [
    path('', custom_message, name='home'),
    path('success/', success, name='success'),
    path('error/', error, name='error'),
]