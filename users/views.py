from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from users.permissions import IsManeger, IsTeamLeader, IsTeamMember
from drf_yasg.utils import swagger_auto_schema
from users.serializers import RegisterSerializer, LoginSerializer
from users.models import CustomUser


class RegisterView(APIView):

    @swagger_auto_schema(request_body=RegisterSerializer,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'user': serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer,)


    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'user': serializer.data, 'token': token.key}, status=status.HTTP_200_OK)
            return Response({'details':'Invalid data'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'details': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except (AttributeError, Token.DoesNotExist):
            return Response({'details': 'No token found'}, status=status.HTTP_400_BAD_REQUEST)
        

class SetManager(APIView):

    permission_classes = [IsAdminUser | IsManeger]

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.role = 'manager'
        user.save()
        return Response(status=status.HTTP_200_OK)
    
    
    