from django.urls import path
from tasks.views import CreateTaskView, AssignTaskView, CheckAsDoneView

urlpatterns = [
    path('create-task/', CreateTaskView.as_view(), name="create-task"),
    path('assign-task/<int:id>/', AssignTaskView.as_view(), name="assign-task"),
    path('check-done/<int:id>/', CheckAsDoneView.as_view(), name="check-done"),
]