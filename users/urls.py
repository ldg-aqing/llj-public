from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('speaker/', views.speaker_view, name='speaker_view'),
    path('audience/', views.audience_view, name='audience_view'),
path('organizer/', views.organizer_view, name='organizer_view'),
]