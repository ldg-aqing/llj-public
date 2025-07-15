from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('organizer', '组织者'),
        ('speaker', '演讲者'),
        ('listener', '听众'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='listener')

    def __str__(self):
        return f"{self.username}（{self.get_role_display()}）"