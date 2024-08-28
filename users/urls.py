from django.urls import path
from users.views import RegisterView, LoginView, Logout, SetManager, SetTeamLeader

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('set-manager/<int:user_id>/', SetManager.as_view(), name="set-manager"),
    path('set-teamleader/<int:user_id>/', SetTeamLeader.as_view(), name="set-teamleader"),
]
