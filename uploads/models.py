from django.db import models
from users.models import User
from presentations.models import Presentation

class Upload(models.Model):
    FILE_TYPES = (
        ('PDF', 'PDF'),
        ('PPTX', 'PPTX'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    content = models.TextField(default='未提取')
    uploaded_at = models.DateTimeField(auto_now_add=True)


