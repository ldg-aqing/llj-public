from django.urls import path
from .views import hello_world

urlpatterns = [
    path('test/', hello_world),
]
