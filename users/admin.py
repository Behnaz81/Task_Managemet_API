from django.contrib import admin
from users.models import CustomUser, Team, TeamMembership

admin.site.register(CustomUser)
admin.site.register(Team)
admin.site.register(TeamMembership)
