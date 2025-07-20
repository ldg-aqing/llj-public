from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from uploads.models import Upload
from .services import generate_question_from_text, save_quiz_from_ai_response
from presentations.models import Presentation
from quizzes.models import Quiz, QuizOption
from django.http import JsonResponse
@api_view(['POST'])
def generate_ai_quiz(request, presentation_id):
    try:
        presentation = Presentation.objects.get(id=presentation_id)
        upload = Upload.objects.filter(presentation_id=presentation_id).last()
        if not upload:
            return Response({"status": "error", "message": "未找到该演讲对应的上传内容"}, status=404)

        text = upload.content
        ai_output = generate_question_from_text(text)
        quizzes = save_quiz_from_ai_response(presentation, ai_output)

        return Response({
            "status": "success",
            "presentation_id": presentation.id,
            "text": text,
            "output": ai_output,
            "quizzes": [
                {
                    "id": quiz.id,
                    "question": quiz.question,
                    "options": [
                        {"id": option.id, "text": option.option_text}
                        for option in quiz.options.all()
                    ]
                }
                for quiz in quizzes
            ]
        })


    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)


def quiz_list(request, presentation_id):
    try:
        quizzes = Quiz.objects.filter(presentation_id=presentation_id).order_by('id')
        result = []

        for q in quizzes:
            options = QuizOption.objects.filter(quiz=q)
            result.append({
                "id": q.id,
                "title": f"题目 #{q.id}",
                "status": q.status if hasattr(q, 'status') else "active",
                "content": q.question,
                "options": [f"{chr(65+i)}. {opt.option_text}" for i, opt in enumerate(options)],
                "answer": f"{get_correct_option_label(q)}. {q.correct_option.option_text}" if q.correct_option else None,
                "explanation": q.explanation or ""
            })

        return JsonResponse(result, safe=False)

    except Presentation.DoesNotExist:
        return JsonResponse({"status": "error", "message": "找不到对应的演讲"}, status=404)
@api_view(['POST'])
def publish_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.status = 'active'
        quiz.save()
        return Response({'message': f'Quiz {quiz_id} 已发布'}, status=status.HTTP_200_OK)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz 不存在'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def close_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.status = 'completed'
        quiz.save()
        return JsonResponse({'message': f'Quiz {quiz_id} 已收卷'})
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz 不存在'}, status=404)

def get_correct_option_label(quiz):
        if not quiz.correct_option:
            return None
        options = list(quiz.options.all())
        try:
            index = options.index(quiz.correct_option)
            return chr(65 + index)  # A, B, C, D
        except ValueError:
            return None
