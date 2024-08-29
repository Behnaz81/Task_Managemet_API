from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from users.permissions import IsManeger, IsTeamLeader, IsTeamMember
from drf_yasg.utils import swagger_auto_schema
from users.serializers import RegisterSerializer, LoginSerializer, CreateTeamSerializer, ReadTeamSerializer
from users.models import CustomUser, Team


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
        return Response({'details': 'successfully set to manager'}, status=status.HTTP_200_OK)
    

class SetTeamLeader(APIView):
    permission_classes = [IsAdminUser | IsManeger | IsTeamLeader]

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.role = 'teamleader'
        user.save()
        return Response({'details': 'successfully set to team leader'}, status=status.HTTP_200_OK)
    

class CreateTeam(APIView):
    permission_classes = [IsAdminUser | IsManeger]

    def post(self, request):
        serializer = CreateTeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['created_by'] = request.user
            serializer.save()
            return Response({'team': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class ListTeam(APIView):
    permission_classes = [IsAdminUser | IsManeger]

    def get(self, request):
        teams = Team.objects.all().filter(created_by=request.user)
        serializer = ReadTeamSerializer(instance=teams, many=True)
        return Response({'teams': serializer.data}, status=status.HTTP_200_OK)

    