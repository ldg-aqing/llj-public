from django.urls import path
from django.shortcuts import render

urlpatterns = [
    path('speaker/', lambda request: render(request, 'speaker.html'), name='speaker'),
]
