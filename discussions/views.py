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
    if request.method != 'POST':
        return JsonResponse({'code': 1, 'msg': '仅支持 POST 请求'}, status=405)

    try:
        data = json.loads(request.body)
        content = data.get('content')

        # 统一从 session 里取 user_id，保证登录状态
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'code': 1, 'msg': '请先登录'}, status=401)

        if not content or not content.strip():
            return JsonResponse({'code': 1, 'msg': '评论内容不能为空'}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'code': 1, 'msg': '用户不存在'}, status=404)

        quiz = Quiz.objects.get(id=quiz_id)

        discussion, created = Discussion.objects.get_or_create(
            quiz=quiz,
            defaults={
                'open_time': timezone.now(),
                'close_time': timezone.now() + timezone.timedelta(days=7),
            }
        )

        now = timezone.now()
        if not (discussion.open_time <= now <= discussion.close_time):
            return JsonResponse({'code': 1, 'msg': '讨论已关闭'}, status=403)

        Comment.objects.create(
            discussion=discussion,
            user=user,
            content=content.strip()
        )

        return JsonResponse({'code': 0, 'msg': '评论成功'})

    except Quiz.DoesNotExist:
        return JsonResponse({'code': 1, 'msg': '题目不存在'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'code': 1, 'msg': '请求体解析错误'}, status=400)
    except Exception as e:
        return JsonResponse({'code': 1, 'msg': '服务器错误'}, status=500)
