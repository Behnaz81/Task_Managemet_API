from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsManeger
from projects.serializers import CreateProjectSerializer


class CreateProjectView(APIView):
    permission_classes = [IsManeger]

    def post(self, request):
        serializer = CreateProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['created_by'] = request.user
            serializer.save()
            return Response({'details': 'project was created successfully', 'project': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
