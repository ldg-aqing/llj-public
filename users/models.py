from django.db import models

# 用户角色枚举
class UserRole(models.TextChoices):
    ORGANIZER = 'ORGANIZER', '组织者'
    SPEAKER = 'SPEAKER', '演讲者'
    AUDIENCE = 'AUDIENCE', '听众'

# 用户信息表（非替代默认用户模型）
class Users(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # 建议使用前端加密 + 后端哈希
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=UserRole.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
