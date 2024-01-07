from django.db import models
from django.contrib.auth.models import User
# Create your models here.

PRIORITY_CHOICES = (
    ('high', 'High'),
    ('medium', 'Medium'),
    ('low', 'Low'),
)

class Task(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=255, null= True, black = True)
    photos = models.ImageField(upload_to='images/', null = True, blank= True)
    priority = models.CharField(max_length = 10, choices = PRIORITY_CHOICES)
    due_date = models.DateField()
    is_completed = models.BooleanField(default = False) 

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self) -> str:
        return self.title