from django.urls import path
from tasks.views import (CreateTaskView, 
                         AssignTaskView, 
                         CheckAsDoneView, 
                         ListAssignedTasksView, 
                         ListAssignedTeamTasksView, 
                         DeleteTaskView)

urlpatterns = [
    path('create-task/', CreateTaskView.as_view(), name="create-task"),
    path('assign-task/<int:id>/', AssignTaskView.as_view(), name="assign-task"),
    path('check-done/<int:id>/', CheckAsDoneView.as_view(), name="check-done"),
    path('list-assigned-tasks/', ListAssignedTasksView.as_view(), name="list-assigned-tasks"),
    path('list-assigned-team-tasks/', ListAssignedTeamTasksView.as_view(), name="list-assigned-team-tasks"),
    path('delete-task/<int:id>/', DeleteTaskView.as_view(), name="delete-task"),
]