from django.db import models

from show.models import Presentation


# Create your models here.
# 测验题目表
class Quiz(models.Model):
    STATUS_CHOICES = [
        ('READY', '准备中'),
        ('ACTIVE', '进行中'),
        ('CLOSED', '已关闭'),
    ]

    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    question = models.TextField()
    options = models.JSONField()  # e.g. {"A": "选项1", "B": "选项2"}
    correct_answer = models.CharField(max_length=5)
    explanation = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='READY')
    time_limit = models.PositiveIntegerField(default=30)  # 单题限时（秒）

    def __str__(self):
        return self.question[:50]