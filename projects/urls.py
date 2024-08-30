from django.urls import path
from projects.views import CreateProjectView

urlpatterns = [
    path('create-project/', CreateProjectView.as_view(), name="creat-project"),
]
