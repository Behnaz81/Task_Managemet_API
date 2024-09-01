from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - Due to {self.due_date}"
