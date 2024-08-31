from django.urls import path
from users.views import RegisterView, LoginView, Logout, SetManager, SetTeamLeader, CreateTeam, DeleteTeam, ListTeam, AddMember

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('set-manager/<int:user_id>/', SetManager.as_view(), name="set-manager"),
    path('set-teamleader/<int:user_id>/', SetTeamLeader.as_view(), name="set-teamleader"),
    path('create-team/', CreateTeam.as_view(), name="create-team"),
    path('list-teams/', ListTeam.as_view(), name="list-teams"),
    path('add-members/', AddMember.as_view(), name="add-members"),
    path('delete-team/<int:id>/', DeleteTeam.as_view(), name="delete-team"),
]
