from rest_framework.serializers import ModelSerializer
from users.models import CustomUser

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']
