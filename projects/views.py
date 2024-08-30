from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsManeger
from projects.serializers import CreateReadProjectSerializer, AssignProjectSerializer
from projects.models import Project


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
            validated_data = serializer.validated_data
            project = Project.objects.get(id=id)
            if  validated_data['team_id'].created_by == request.user and project.created_by == request.user:
                if not project.team_id:
                    project.team_id = validated_data['team_id']
                    project.save()
                    return Response({'details': 'project was assigned successfully', 'project': serializer.data}, status=status.HTTP_200_OK)
                return Response({'details': 'this project is already assigned to another team'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'details': "you don't have access to this method"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListProjectView(APIView):
    permission_classes = [IsManeger]

    def get(self, request):
        projects = Project.objects.filter(created_by=request.user)
        serializer = CreateReadProjectSerializer(instance=projects, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class DetailsProjectView(APIView):
    permission_classes = [IsManeger]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if project.created_by == request.user:
            serializer = CreateReadProjectSerializer(instance=project)
            return Response({'project': serializer.data}, status=status.HTTP_200_OK)
        return Response({'details': "you don't have access to this project"}, status=status.HTTP_401_UNAUTHORIZED)
