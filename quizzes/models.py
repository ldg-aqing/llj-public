from django.db import models
from presentations.models import Presentation
from users.models import User

class Quiz(models.Model):
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    question = models.TextField()
    created_by_ai = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class QuizOption(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='options')
    option_text = models.TextField()

    def __str__(self):
        return self.option_text

# 外部定义 correct_option 字段
Quiz.add_to_class('correct_option', models.ForeignKey(
    QuizOption, on_delete=models.SET_NULL, null=True, blank=True, related_name='correct_for'))

class QuizSession(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuizOption, on_delete=models.SET_NULL, null=True)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
