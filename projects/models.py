from django.db import models
from django.contrib.auth import get_user_model
from users.models import Team

User = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    team = models.ManyToManyField(Team)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)

    def __str__(self):
        return self.title
