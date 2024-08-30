from django.urls import path
from projects.views import CreateProjectView, AssignProjectView

urlpatterns = [
    path('create-project/', CreateProjectView.as_view(), name="creat-project"),
    path('assign-project/<int:id>/', AssignProjectView.as_view(), name="assign-project"),
]
