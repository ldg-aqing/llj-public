from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime
from .models import Feedback
from users.models import User
from django.shortcuts import render, get_object_or_404
from presentations.models import Presentation
from quizzes.models import Quiz  # 如果不关联 quiz 可不导入
import json

# 获取反馈列表
def get_feedbacks(request, presentation_id):
    try:
        feedbacks = Feedback.objects.filter(presentation_id=presentation_id).order_by('-submitted_at')
        data = []
        for f in feedbacks:
            data.append({
                'id': f.id,
                'user': f.user.username,
                'category': f.get_category_display(),  # 中文名显示
                'reason': f.reason,
                'time': localtime(f.submitted_at).strftime('%Y-%m-%d %H:%M')
            })
        return JsonResponse({'code': 0, 'feedbacks': data})
    except Exception as e:
        return JsonResponse({'code': 1, 'msg': str(e)})

# 提交反馈
@csrf_exempt
def post_feedback(request, presentation_id):
    if request.method != 'POST':
        return JsonResponse({'code': 1, 'msg': '仅支持 POST 请求'})

    try:
        data = json.loads(request.body)
        category = data.get('category')
        reason = data.get('reason')

        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'code': 1, 'msg': '用户未登录'})

        user = User.objects.get(id=user_id)
        presentation = Presentation.objects.get(id=presentation_id)

        feedback = Feedback.objects.create(
            user=user,
            presentation=presentation,
            category=category,
            reason=reason
        )
        return JsonResponse({'code': 0, 'msg': '反馈提交成功', 'feedback_id': feedback.id})
    except Exception as e:
        return JsonResponse({'code': 1, 'msg': str(e)})

def show_feedbacks(request, presentation_id):
    FEEDBACK_TYPE_DISPLAY = {
        'SPEAKER': '演讲者',
        'QUIZ': '测验',
        'ENVIRONMENT': '环境'
    }
    feedbacks = Feedback.objects.filter(presentation_id=presentation_id).order_by('-submitted_at')
    for fb in feedbacks:
        fb.category_display_zh = FEEDBACK_TYPE_DISPLAY.get(fb.category, fb.category)
    return render(request, 'presentations/after/speaker_afterp.html', {
        'feedbacks': feedbacks
    })



# 组织者视图
def organizer_report(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    feedbacks = Feedback.objects.filter(presentation_id=presentation_id).order_by('-submitted_at')
    # 可以加各种统计/分析，仅组织者能看
    return render(request, 'presentations/after/organizer_afterp.html', {
        'presentation': presentation,
        'feedbacks': feedbacks,
    })

# 观众视图
def audience_report(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    feedbacks = Feedback.objects.filter(presentation_id=presentation_id).order_by('-submitted_at')
    # 可以只显示部分内容
    return render(request, 'presentations/after/audience_afterp.html', {
        'presentation': presentation,
        'feedbacks': feedbacks,
    })