from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Discussion, Comment
from users.models import User
from quizzes.models import Quiz
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json

def get_comments(request, quiz_id):
    if request.method == 'GET':
        try:
            discussion = Discussion.objects.get(quiz_id=quiz_id)
            now = timezone.now()
            if not (discussion.open_time <= now <= discussion.close_time):
                return JsonResponse({'code': 1, 'msg': '讨论未开放'}, status=403)

            comments = Comment.objects.filter(discussion=discussion).order_by('-created_at')
            data = [
                {
                    'user': c.user.username,
                    'content': c.content,
                    'created_at': c.created_at.strftime("%Y-%m-%d %H:%M")
                } for c in comments
            ]
            return JsonResponse({'code': 0, 'data': data})
        except Discussion.DoesNotExist:
            return JsonResponse({'code': 1, 'msg': '该题目没有讨论区'}, status=404)

@csrf_exempt
def post_comment(request, quiz_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            content = data.get('content')

            user = User.objects.get(id=user_id)
            quiz = Quiz.objects.get(id=quiz_id)

            # 尝试获取已有讨论区，没有就创建
            discussion, created = Discussion.objects.get_or_create(
                quiz=quiz,
                defaults={
                    'open_time': timezone.now(),
                    'close_time': timezone.now() + timezone.timedelta(days=7),  # 举例7天后关闭
                }
            )

            now = timezone.now()
            if not (discussion.open_time <= now <= discussion.close_time):
                return JsonResponse({'code': 1, 'msg': '讨论已关闭'}, status=403)

            Comment.objects.create(
                discussion=discussion,
                user=user,
                content=content
            )

            return JsonResponse({'code': 0, 'msg': '评论成功'})

        except User.DoesNotExist:
            return JsonResponse({'code': 1, 'msg': '用户不存在'}, status=404)
        except Quiz.DoesNotExist:
            return JsonResponse({'code': 1, 'msg': '题目不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'code': 1, 'msg': str(e)}, status=500)
    else:
        return JsonResponse({'code': 1, 'msg': '请求方法错误'}, status=405)