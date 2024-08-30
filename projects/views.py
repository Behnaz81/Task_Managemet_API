from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsManeger
from projects.serializers import CreateProjectSerializer, AssignProjectSerializer
from projects.models import Project


class CreateProjectView(APIView):
    permission_classes = [IsManeger]

    def post(self, request):
        serializer = CreateProjectSerializer(data=request.data)
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
