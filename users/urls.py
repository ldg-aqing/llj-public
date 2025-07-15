from django.urls import path
from .views import register_view, login_view
from django.shortcuts import render

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),

    path('organizer/', lambda request: render(request, 'users/organizer.html'), name='organizer'),
    path('speaker/', lambda request: render(request, 'users/speaker.html'), name='speaker'),
    path('audience/', lambda request: render(request, 'users/audience.html'), name='audience'),
]
