from django.db import models
from users.models import User
from presentations.models import Presentation
from quizzes.models import Quiz

class Feedback(models.Model):
    FEEDBACK_TYPES = (
        ('SPEAKER', 'Speaker'),
        ('QUIZ', 'Quiz'),
        ('ENVIRONMENT', 'Environment'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    reason = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
