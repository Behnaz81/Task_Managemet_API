from django.urls import path
from users.views import RegisterView, LoginView, Logout

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
]
