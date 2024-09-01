from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsManeger
from projects.serializers import CreateReadProjectSerializer, AssignProjectSerializer, DetailProjectSerializer
from projects.models import Project
from users.models import TeamMembership


class CreateProjectView(APIView):
    permission_classes = [IsManeger]

    def post(self, request):
        serializer = CreateReadProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['created_by'] = request.user
            serializer.save()
            return Response({'details': 'project was created successfully', 'project': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignProjectView(APIView):
    permission_classes = [IsManeger]

    def post(self, request, id):
        serializer = AssignProjectSerializer(data=request.data)

        if serializer.is_valid():
            teams_to_assign = serializer.validated_data['team']

            memberships = TeamMembership.objects.filter(user=request.user, role_within_team="manager")
            user_teams = list(memberships.values_list('team', flat=True))
            print(user_teams)

            try:
                project = Project.objects.get(id=id)

            except Project.DoesNotExist:
                return Response({'details': "The specified project does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            if not all(team.id in user_teams for team in teams_to_assign):
                return Response({'details': "You are not the manager of the selected teams."}, status=status.HTTP_403_FORBIDDEN)
                

            existing_teams = project.team.all()
            teams_to_assign = [team for team in teams_to_assign if team not in existing_teams]

            if not teams_to_assign:
                return Response({"details": "All teams are already participating in this project."}, status=status.HTTP_403_FORBIDDEN)
            
            project.team.add(*teams_to_assign)
            project.save()
            return Response({'details': 'project was assigned successfully', 'project': serializer.data}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        memberships = TeamMembership.objects.filter(user=request.user)
        teams = memberships.values_list('team', flat=True)
        projects = Project.objects.filter(team__in=teams).distinct()
        serializer = CreateReadProjectSerializer(instance=projects, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class DetailsProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        user_teams = TeamMembership.objects.filter(user=request.user).values_list('team', flat=True)
        if project.team.filter(id__in=user_teams).exists():
            serializer = DetailProjectSerializer(instance=project)
            return Response({'project': serializer.data}, status=status.HTTP_200_OK)
        return Response({'details': "you don't have access to this project"}, status=status.HTTP_401_UNAUTHORIZED)
    

class DeleteProjectView(APIView):
    permission_classes = [IsManeger]

    def delete(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if project.created_by == request.user:
            project.delete()
            return Response({'details': 'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response ({'details': "you don't have access to this project"}, status=status.HTTP_401_UNAUTHORIZED)
