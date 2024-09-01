from rest_framework.serializers import ModelSerializer
from projects.models import Project

class CreateReadProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('title', 'description')


class AssignProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('team',)


class DetailProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ("title", "description", "team", "created_by")
