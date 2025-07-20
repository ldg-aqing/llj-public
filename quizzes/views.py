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


def quiz_list(request):
    if request.method == 'GET':
        data = []
        quizzes = Quiz.objects.all().order_by('-created_at')

        for quiz in quizzes:
            # 获取选项列表
            options = list(quiz.options.values_list('option_text', flat=True))

            # 获取正确答案文本（如果有设置）
            correct_option = quiz.correct_option.option_text if quiz.correct_option else None

            # 构造一个题目的字典
            quiz_data = {
                'id': quiz.id,
                'question': quiz.question,
                'options': options,
                'correct_answer': correct_option,
                'explanation': quiz.explanation,
                'status': quiz.status,
                'created_at': quiz.created_at,
                'presentation_id': quiz.presentation_id,
            }

            data.append(quiz_data)

        return JsonResponse(data, safe=False)
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