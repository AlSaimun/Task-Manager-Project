from django.db import models
from django.contrib.auth.models import User
# Create your models here.

PRIORITY_CHOICES = (
    ('3', 'High'),
    ('2', 'Medium'),
    ('1', 'Low'),
)

class Task(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)
    description = models.TextField(max_length=255, null= True, blank = True)
    priority = models.CharField(max_length = 10, choices = PRIORITY_CHOICES)
    due_date = models.DateField()
    is_completed = models.BooleanField(default = False) 

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self) -> str:
        return self.title
    
    def get_priority(self):
        '''this function for showing priority in frontend'''
        if self.priority == '3':
            return "High"
        elif self.priority == '2':
            return "Medium"
        else:
            return "Low"

class Image(models.Model):
    task = models.ForeignKey(Task, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/tasks')
