from django.urls import path
from .views import generate_ai_quiz, quiz_list, publish_quiz, close_quiz, quiz_statistics
from django.http import JsonResponse
from . import views
def test_view(request):
    return JsonResponse({"message": "quizzes API is working!"})

urlpatterns = [
    path('', test_view),  #  添加这一行，支持 /api/quizzes/
    path('generate/<int:presentation_id>/', generate_ai_quiz, name='generate_ai_quiz'),
    path('list/<int:presentation_id>/', quiz_list, name='quiz_list'),
    path('publish/<int:quiz_id>/', publish_quiz, name='publish_quiz'),
    path('close/<int:quiz_id>/', close_quiz, name='close_quiz'),
    path('stats/<int:presentation_id>/', quiz_statistics, name='quiz_statistics'),

    path('check_submission/<int:quiz_id>/<int:user_id>/', views.check_submission, name='check_submission'),
    path('get_selected_option/<int:quiz_id>/<int:user_id>/', views.get_selected_option, name='get_selected_option'),
]
