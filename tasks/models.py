from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)


    class Meta:
        unique_together = ('title', 'project')

    def __str__(self):
        return f"{self.title} - Due to {self.due_date}"
