from django.db import models


class Team(models.Model):

    title = models.CharField(max_length=150)


