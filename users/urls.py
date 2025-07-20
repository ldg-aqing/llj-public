from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.handle_form, name='login'),
]