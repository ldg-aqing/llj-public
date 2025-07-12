from django.db import models

# 上传素材表（测试）
class UploadedMaterial(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='materials/')
    file_type = models.CharField(max_length=20)
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
