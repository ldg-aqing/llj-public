from django.db import models


class User(models.Model):
    ROLE_CHOICES = (
        ('ORGANIZER', 'Organizer'),
        ('SPEAKER', 'Speaker'),
        ('AUDIENCE', 'Audience'),
    )
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
