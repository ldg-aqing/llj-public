from django.db import models

from show.models import Presentation
from users.models import Users


# Create your models here.
# 听众参与关系表
class PresentationAttendee(models.Model):
    STATUS_CHOICES = [
        ('PENDING', '待审核'),
        ('APPROVED', '已通过'),
        ('REJECTED', '已拒绝'),
    ]
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Users, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='APPROVED')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('presentation', 'attendee')