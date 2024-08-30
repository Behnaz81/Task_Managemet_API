from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()

class Task(models.Model):
    class Priority(models.IntegerChoices):
        VERY_HIGH = 1, "Very Important"
        HIGH = 2, "Important"
        MEDIUM = 3, "Medium"
        LOW = 4, "Low"
        VERY_LOW = 5, "Very Low"

    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_to')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_by')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    priority = models.IntegerField(choices=Priority)
    due_date = models.DateField()
    
