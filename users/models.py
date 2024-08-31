from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class Team(models.Model):

    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title
    

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('teammember', 'Team Member'),
        ('teamleader', 'Team Leader'),
        ('manager', 'Manager'),
    )

    role = models.CharField(max_length=20, default='teammember', choices=ROLE_CHOICES)
    team = models.ManyToManyField(Team)
