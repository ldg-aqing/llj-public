from django.db import models
from users.models import User

class Presentation(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('LIVE', 'Live'),
        ('FINISHED', 'Finished'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    speaker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='speeches')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_presentations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PresentationAttendee(models.Model):
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('presentation', 'attendee')
