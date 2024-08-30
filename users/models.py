from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('teammember', 'Team Member'),
        ('teamleader', 'Team Leader'),
        ('manager', 'Manager'),
    )

    role = models.CharField(max_length=20, default='teammember',choices=ROLE_CHOICES)


class Team(models.Model):

    title = models.CharField(max_length=150)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class TeamMembers(models.Model):

    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    member_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
