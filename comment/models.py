from django.db import models

from quiz.models import Quiz
from show.models import Presentation
from users.models import Users


# Create your models here.
# 演讲即时反馈表
class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('TOO_FAST', '讲得太快'),
        ('TOO_SLOW', '讲得太慢'),
        ('BORING', '演讲乏味'),
        ('BAD_QUIZ', '题目不好'),
    ]
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    related_quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# 讨论区评论表
class DiscussionMessage(models.Model):
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)