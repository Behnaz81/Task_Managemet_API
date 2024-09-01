from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from users.permissions import IsManeger, IsTeamLeader, IsTeamMember
from drf_yasg.utils import swagger_auto_schema
from users.serializers import RegisterSerializer, LoginSerializer, TeamSerializer, CreateTeamMembershipSerializer, DeleteTeamMembershipSerializer, ReadTeamMembershipSerializer
from users.models import Team, TeamMembership

User = get_user_model()


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'user': serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    permission_classes = [AllowAny]

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
        user = get_object_or_404(User, id=user_id)

        if not request.user.is_superuser and request.user.role != 'manager':
            return Response({'details': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        user.role = 'manager'
        user.save()
        return Response({'details': 'successfully set to manager'}, status=status.HTTP_200_OK)
    

class SetTeamLeader(APIView):
    permission_classes = [IsAdminUser | IsManeger | IsTeamLeader]

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        if not request.user.is_superuser and request.user.role not in ['manager', 'teamleader']:
            return Response({'details': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        user.role = 'teamleader'
        user.save()
        return Response({'details': 'successfully set to team leader'}, status=status.HTTP_200_OK)
    

class CreateTeam(APIView):
    permission_classes = [IsAdminUser | IsManeger]

    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            team = serializer.save()
            team_member = TeamMembership.objects.create(team=team, user=request.user)
            return Response({'details':'team created successfully', 'team': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ListTeam(APIView):

    def get(self, request):
        memberships = TeamMembership.objects.filter(user=request.user)
        teams = [membership.team for membership in memberships]
        serializer = TeamSerializer(instance=teams, many=True)
        return Response({'details':'data retrieved successfully', 'teams': serializer.data}, status=status.HTTP_200_OK)


class AddMember(APIView):
    permission_classes = [IsAdminUser | IsManeger]

    def post(self, request):
        serializer = CreateTeamMembershipSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            team = validated_data['team']
            user_to_add = validated_data['user']
            
            try:
                TeamMembership.objects.get(team=team, user=request.user)
            except TeamMembership.DoesNotExist:
                return Response({'details': "You don't have access to this method"}, status=status.HTTP_401_UNAUTHORIZED)
            
            if user_to_add.role == 'manager':
                return Response({'details': "You can't add managers to teams"}, status=status.HTTP_400_BAD_REQUEST)

            if TeamMembership.objects.filter(user=user_to_add).exists():
                return Response({'details': 'This user already has a team'}, status=status.HTTP_400_BAD_REQUEST)
            
            if user_to_add.role == 'teamleader':
                if TeamMembership.objects.filter(team=team, user__role='teamleader').exists():
                    return Response({'details': 'The team already has a team leader'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteTeam(APIView):
    permission_classes = [IsAdminUser | IsManeger]

    def delete(self, request, id):
        team = get_object_or_404(Team, id=id)
        try:
            team_membership = TeamMembership.objects.get(team=team, user=request.user)
        except TeamMembership.DoesNotExist:
            return Response({'details': "You are not a member of this team"}, status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 'manager':
            team.delete()
            return Response({'details': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({'details': "You don't have access to this method"}, status=status.HTTP_401_UNAUTHORIZED)
    

class DeleteMember(APIView):
    permission_classes = [IsManeger | IsTeamLeader]

    def delete(self, request):
        serializer = DeleteTeamMembershipSerializer(data=request.data)
        if serializer.is_valid():
            team = serializer.validated_data['team']
            user = serializer.validated_data['user']

            try:
                TeamMembership.objects.get(team=team, user=request.user)
            except TeamMembership.DoesNotExist:
                return Response({'details': "You don't have access to this method"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                membership = TeamMembership.objects.get(team=team, user=user)
                membership.delete()
                return Response({'details': 'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            except TeamMembership.DoesNotExist:
                return Response({'details': "This member isn't in this team"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ListMember(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, team_id):
        memberships = TeamMembership.objects.filter(team=team_id)
        manager = memberships.filter(role_within_team="manager")
        teamleader = memberships.filter(role_within_team="teamleader")
        
        if memberships.filter(user=request.user).exists():
            memberships = memberships.exclude(role_within_team="manager").exclude(role_within_team="teamleader")
            
            manager_serializer = ReadTeamMembershipSerializer(instance=manager, many=True)
            teamleader_serializer = ReadTeamMembershipSerializer(instance=teamleader, many=True)
            members_serializer = ReadTeamMembershipSerializer(instance=memberships, many=True)
            
            return Response({"manager": manager_serializer.data, 
                             "teamleader": teamleader_serializer.data, 
                             "members": members_serializer.data}, 
                             status=status.HTTP_200_OK)
        
        return Response({"details": "You don't have access to this method"}, 
                        status=status.HTTP_403_FORBIDDEN)
        
            