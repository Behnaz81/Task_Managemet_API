from django.contrib import admin
from users.models import CustomUser, Team, TeamMembers

admin.site.register(CustomUser)
admin.site.register(Team)
admin.site.register(TeamMembers)
