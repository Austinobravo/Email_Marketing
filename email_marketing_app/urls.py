from django.urls import path
from .views import custom_message, index

urlpatterns = [
    path('', custom_message, name='custom_message'),
    path('success/', index, name='index'),
]