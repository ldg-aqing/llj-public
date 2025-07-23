from django.urls import path
from . import views
urlpatterns = [
    path('<int:presentation_id>/', views.post_feedback, name='post_feedback'),
    path('list/<int:presentation_id>/', views.get_feedbacks, name='get_feedbacks'),
    path('show/<int:presentation_id>/', views.show_feedbacks, name='show_feedbacks'),
    path('report/organizer/<int:presentation_id>/', views.organizer_report, name='organizer_report'),
    path('report/audience/<int:presentation_id>/', views.audience_report, name='audience_report'),
]

