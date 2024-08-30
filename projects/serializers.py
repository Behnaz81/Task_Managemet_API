from rest_framework.serializers import ModelSerializer
from projects.models import Project

class CreateProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('title', 'description')


class AssignProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('team_id',)

