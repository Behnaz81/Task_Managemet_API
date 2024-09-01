from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsManeger, IsTeamLeader
from users.models import TeamMembership
from projects.models import Project
from tasks.serializers import CreateTaskSerializer


class CreateTaskView(APIView):
    permission_classes = [IsTeamLeader | IsManeger]

    def post(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        
        if serializer.is_valid():
            user_teams = list(TeamMembership.objects.filter(user=request.user).values_list('team', flat=True))
            project = serializer.validated_data['project']
            project_teams = project.team.filter(id__in=user_teams)

            if not project_teams:
                return Response({"details": "you don't work on this project"}, status=status.HTTP_403_FORBIDDEN)
            
            serializer.save()
            return Response({"task": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
