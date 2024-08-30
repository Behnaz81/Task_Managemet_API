from rest_framework.serializers import ModelSerializer
from projects.models import Project

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('title', 'description', 'team_id', 'created_by')
