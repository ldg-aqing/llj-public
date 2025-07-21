from django.urls import path
from . import views

urlpatterns = [
    path('quiz/<int:quiz_id>/comments/', views.get_comments, name='get_comments'),
    path('quiz/<int:quiz_id>/comments/post/', views.post_comment, name='post_comment'),
]
