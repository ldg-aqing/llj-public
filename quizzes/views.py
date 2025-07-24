from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from uploads.models import Upload
from .services import generate_question_from_text, save_quiz_from_ai_response
from presentations.models import Presentation
from quizzes.models import Quiz, QuizOption, QuizSession
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
@api_view(['GET'])
def quiz_statistics(request, presentation_id):
    quizzes = Quiz.objects.filter(presentation_id=presentation_id)
    result = []
    total_accuracy = 0
    count_with_answers = 0  # 只统计有作答的题目用于平均值

    for quiz in quizzes:
        sessions = QuizSession.objects.filter(quiz=quiz)
        total_answers = sessions.count()
        correct_answers = sessions.filter(is_correct=True).count()

        # 每个选项被选择次数
        option_stats = sessions.values('selected_option__id').annotate(count=Count('id'))
        option_count_map = {stat['selected_option__id']: stat['count'] for stat in option_stats}

        options_result = []
        options = quiz.options.all()
        for i, opt in enumerate(options):
            label = chr(65 + i)
            options_result.append({
                "label": label,
                "text": opt.option_text,
                "count": option_count_map.get(opt.id, 0)
            })

        accuracy = round(correct_answers / total_answers * 100, 2) if total_answers > 0 else None

        if accuracy is not None:
            total_accuracy += accuracy
            count_with_answers += 1

        result.append({
            "quiz_id": quiz.id,
            "question": quiz.question,
            "total_answers": total_answers,
            "correct_answers": correct_answers,
            "accuracy": accuracy,
            "options": options_result
        })

    average_accuracy = round(total_accuracy / count_with_answers, 2) if count_with_answers > 0 else None

    return Response({
        "presentation_id": presentation_id,
        "average_accuracy": average_accuracy,
        "quizzes": result
    })


@csrf_exempt
def check_submission(request, quiz_id, user_id):
    """
    查询用户是否对某题提交过答案
    GET请求，返回JSON:
    {
        "is_submitted": true/false,
        "selected_option_id": 选项id 或 null,
    }
    """
    if request.method != 'GET':
        return JsonResponse({'code': 1, 'msg': '只支持 GET 请求'}, status=405)

    try:
        session = QuizSession.objects.filter(quiz_id=quiz_id, user_id=user_id).first()
        if session:
            return JsonResponse({
                'is_submitted': True,
                'selected_option_id': session.selected_option_id if session.selected_option else None,
            })
        else:
            return JsonResponse({
                'is_submitted': False,
                'selected_option_id': None,
            })
    except Exception as e:
        return JsonResponse({'code': 1, 'msg': str(e)}, status=500)
@csrf_exempt
def get_selected_option(request, quiz_id, user_id):
    """
    获取用户对某题提交的选项ID
    GET请求，返回JSON:
    {
        "selected_option_id": 选项id 或 null,
    }
    """
    if request.method != 'GET':
        return JsonResponse({'code': 1, 'msg': '只支持 GET 请求'}, status=405)

    try:
        session = QuizSession.objects.filter(quiz_id=quiz_id, user_id=user_id).first()
        if session and session.selected_option:
            return JsonResponse({
                'selected_option_id': session.selected_option.id,
            })
        else:
            return JsonResponse({
                'selected_option_id': None,
            })
    except Exception as e:
        return JsonResponse({'code': 1, 'msg': str(e)}, status=500)
