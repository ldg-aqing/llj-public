from django.db import models

# 上传素材表（测试）
class UploadedMaterial(models.Model):
    title = models.CharField(max_length=500)
    file = models.FileField(upload_to='materials/')
    file_type = models.CharField(max_length=20)
    upload_time = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True)  # 用于存储提取出的文本

    def __str__(self):
        return self.title
