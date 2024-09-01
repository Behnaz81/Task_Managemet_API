from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.permissions import (IsManeger, 
                               IsTeamLeader)
from users.models import TeamMembership
from projects.models import Project
from tasks.serializers import (CreateReadTaskSerializer, 
                               AssignTaskSerializer, 
                               DetailTaskSerializer)
from tasks.models import Task


class CreateTaskView(APIView):
    permission_classes = [IsTeamLeader | IsManeger]

    def post(self, request):
        serializer = CreateReadTaskSerializer(data=request.data)

        if serializer.is_valid():
            user_teams = list(TeamMembership.objects.filter(user=request.user).values_list('team', flat=True))
            project = serializer.validated_data['project']
            project_teams = project.team.filter(id__in=user_teams)

            if not project_teams:
                return Response({"details": "you don't work on this project"}, 
                                status=status.HTTP_403_FORBIDDEN)
            
            serializer.save()
            return Response({"task": serializer.data}, 
                            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    

class AssignTaskView(APIView):
    permission_classes = [IsTeamLeader | IsManeger]

    def post(self, request, id):

        serializer = AssignTaskSerializer(data=request.data)

        try:
            task = Task.objects.get(id=id)

        except Task.DoesNotExist:
            return Response({"details":"this task doesn't exist"}, 
                            status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            user_teams = list(TeamMembership.objects.filter(user=request.user).values_list('team', flat=True))
            project_teams_except_user_teams = task.project.team.filter(id__in=user_teams)

            if task.user is not None:
                return Response({"details": "this task is already assigned"}, 
                                status=status.HTTP_403_FORBIDDEN)
            
            if task.is_done:
                return Response({"details": "This task is already done"}, 
                                status=status.HTTP_403_FORBIDDEN)

            if not project_teams_except_user_teams:
                return Response({"details": "you don't work on this project"}, 
                                status=status.HTTP_403_FORBIDDEN)
            
            new_user_teams = list(TeamMembership.objects.filter(user=user).values_list('team', flat=True))
            project_teams_except_new_user_teams = task.project.team.filter(id__in=new_user_teams)

            if not project_teams_except_new_user_teams:
                return Response({'details': "this user doesn't participate in this project"}, 
                                status=status.HTTP_403_FORBIDDEN)
            
            if not any(team in new_user_teams for team in user_teams):
                return Response({"details": "This user is from a different team"}, 
                                status=status.HTTP_403_FORBIDDEN)

            task.user = user
            task.save()
            return Response({'task': serializer.data}, 
                            status=status.HTTP_200_OK)
        
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
        

class CheckAsDoneView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        try:
            task = Task.objects.get(id=id)

        except Task.DoesNotExist:
            return Response({"details": "This task doesn't exist"}, 
                            status=status.HTTP_404_NOT_FOUND)

        if task.user == request.user:
            task.is_done = True
            task.save()
            return Response(status=status.HTTP_200_OK)
        
        return Response({"details": "This task wasn't assign to you"}, 
                        status=status.HTTP_403_FORBIDDEN)
    

class ListAssignedTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        tasks = Task.objects.filter(user=request.user)

        tasks_not_done = tasks.filter(is_done=False)
        tasks_done = tasks.filter(is_done=True)

        tasks_not_done_serializer = CreateReadTaskSerializer(instance=tasks_not_done, many=True)
        tasks_done_serializer = CreateReadTaskSerializer(instance=tasks_done, many=True)

        return Response({"done": tasks_done_serializer.data, 
                         "not done": tasks_not_done_serializer.data}, 
                         status=status.HTTP_200_OK)


class ListAssignedTeamTasksView(APIView):
    permission_classes = [IsManeger | IsTeamLeader]

    def get(self, request):

        user_teams = TeamMembership.objects.filter(user=request.user, role_within_team__in=["manager", "teamleader"]).values_list('team', flat=True)

        user_projects = Project.objects.filter(team__in=user_teams).distinct()

        tasks = Task.objects.filter(project__in=user_projects)

        serializer = DetailTaskSerializer(instance=tasks, many=True)

        return Response({"tasks": serializer.data}, 
                        status=status.HTTP_200_OK)


class DeleteTaskView(APIView):
    permission_classes = [IsManeger | IsTeamLeader]

    def delete(self, request, id):

        try:
            task_to_delete = Task.objects.get(id=id)

        except Task.DoesNotExist:
            return Response({"details": "This task doesn't exist"}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        user_teams = TeamMembership.objects.filter(user=request.user, role_within_team__in=["manager", "teamleader"]).values_list('team', flat=True)

        user_projects = Project.objects.filter(team__in=user_teams).distinct()

        if task_to_delete.project in user_projects:
            task_to_delete.delete()
            return Response({"details": "task was successfully deleted"}, 
                            status=status.HTTP_204_NO_CONTENT)
        
        return Response({"details": "you don't have access to this task"}, 
                        status=status.HTTP_403_FORBIDDEN)
