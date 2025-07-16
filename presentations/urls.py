# presentations/urls.py
from django.urls import path
from .views import speaker_home
from .views import start_presentation
from . import views

urlpatterns = [
    path('speaker/', speaker_home, name='speaker_home'),
    path('before/<int:presentation_id>/', views.start_presentation, name='speaker_before_presentation'),
]
