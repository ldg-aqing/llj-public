from django.db import models

from quiz.models import Quiz
from users.models import Users


# Create your models here.
# 答题记录表
class QuizAnswer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=5)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
    answer_time = models.PositiveIntegerField()  # 答题耗时（秒）
    quality_rating = models.PositiveSmallIntegerField(null=True, blank=True)  # 听众对题目质量的评分（1~5）
