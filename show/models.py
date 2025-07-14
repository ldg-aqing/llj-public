from django.db import models

from users.models import Users


# Create your models here.
# 演讲信息表
class Presentation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', '未开始'),
        ('LIVE', '演讲中'),
        ('FINISHED', '已结束'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    code = models.CharField(max_length=20, unique=True)
    speaker = models.ForeignKey(Users, related_name='speaking_presentations', on_delete=models.SET_NULL, null=True)
    organizer = models.ForeignKey(Users, related_name='organized_presentations', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.code})"