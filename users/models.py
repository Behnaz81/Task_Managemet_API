from django.db import models
from django.contrib.auth.models import AbstractUser

class Team(models.Model):

    title = models.CharField(max_length=150)


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('teammember', 'Team Member'),
        ('teamleader', 'Team Leader'),
        ('manager', 'Manager'),
    )

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


    
