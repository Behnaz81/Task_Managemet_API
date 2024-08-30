from django.urls import path
from projects.views import CreateProjectView, AssignProjectView, ListProjectView, DetailsProjectView, DeleteProjectView

urlpatterns = [
    path('create-project/', CreateProjectView.as_view(), name="creat-project"),
    path('assign-project/<int:id>/', AssignProjectView.as_view(), name="assign-project"),
    path('list-project/', ListProjectView.as_view(), name="list-projects"),
    path('detail-project/<int:project_id>/', DetailsProjectView.as_view(), name="detail-project"),
    path('delete-project/<int:project_id>/', DeleteProjectView.as_view(), name="delete-project"),
]
