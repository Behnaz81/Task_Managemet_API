from django.urls import path
from tasks.views import CreateTaskView

urlpatterns = [
    path('create-task/', CreateTaskView.as_view(), name="create-task"),
]