from django.urls import path
from tasks.views import CreateTaskView, AssignTaskView, CheckAsDoneView, ListAssignedTasks, ListAssignedTeamTasks

urlpatterns = [
    path('create-task/', CreateTaskView.as_view(), name="create-task"),
    path('assign-task/<int:id>/', AssignTaskView.as_view(), name="assign-task"),
    path('check-done/<int:id>/', CheckAsDoneView.as_view(), name="check-done"),
    path('list-assigned-tasks/', ListAssignedTasks.as_view(), name="list-assigned-tasks"),
    path('list-assigned-team-tasks/', ListAssignedTeamTasks.as_view(), name="list-assigned-team-tasks"),
]