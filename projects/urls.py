from django.urls import path
from projects.views import CreateProjectView, AssignProjectView, ListProjectView

urlpatterns = [
    path('create-project/', CreateProjectView.as_view(), name="creat-project"),
    path('assign-project/<int:id>/', AssignProjectView.as_view(), name="assign-project"),
    path('list-project/', ListProjectView.as_view(), name="list-projects"),
]
