from django.db import models
from users.models import User
from quizzes.models import Quiz

class Discussion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()

class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
