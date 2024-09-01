from django.urls import path
from tasks.views import CreateTaskView, AssignTaskView

urlpatterns = [
    path('create-task/', CreateTaskView.as_view(), name="create-task"),
    path('assign-task/<int:id>/', AssignTaskView.as_view(), name="assign-task"),
]