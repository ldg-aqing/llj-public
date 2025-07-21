from django.urls import path
from . import views

urlpatterns = [
    path('presentation/<int:presentation_id>/', views.get_feedbacks, name='get_feedbacks'),
    path('presentation/<int:presentation_id>/post/', views.post_feedback, name='post_feedback'),
]
