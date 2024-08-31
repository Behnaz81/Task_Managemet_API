from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


ROLE_CHOICES = (
        ('teammember', 'Team Member'),
        ('teamleader', 'Team Leader'),
        ('manager', 'Manager'),
    )


class Team(models.Model):

    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title
    

class CustomUser(AbstractUser):

    role = models.CharField(max_length=20, default='teammember', choices=ROLE_CHOICES)
    team = models.ManyToManyField(Team, through='TeamMembership') 


class TeamMembership(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    joined_at = models.DateField(auto_now_add=True) 
    role_within_team = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'team') 

    
    def save(self, *args, **kwargs):
        if not self.role_within_team:
            self.role_within_team = self.user.role
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} in {self.team.title} as {self.role_within_team}"
    