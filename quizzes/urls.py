from django.urls import path
from .views import generate_ai_quiz
from django.http import JsonResponse

def test_view(request):
    return JsonResponse({"message": "quizzes API is working!"})

urlpatterns = [
    path('', test_view),  # ✅ 添加这一行，支持 /api/quizzes/
    path('generate/<int:presentation_id>/', generate_ai_quiz, name='generate_ai_quiz'),
]
