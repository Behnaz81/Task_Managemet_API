from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Task Management API",
        default_version='v1',
        description="This API can help managers, team leaders and team members to create and do projects and tasks",
      ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
