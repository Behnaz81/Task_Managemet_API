from django.db import models
from django.contrib.auth import get_user_model
from users.models import Team

User = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    team_id = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
