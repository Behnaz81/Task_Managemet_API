from rest_framework import serializers
from tasks.models import Task


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'project')
