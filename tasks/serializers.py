from rest_framework import serializers
from django.contrib.auth import get_user_model
from tasks.models import Task

User = get_user_model()


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'project')


class AssignTaskSerializer(serializers.Serializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
