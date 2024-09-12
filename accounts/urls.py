from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupAPIView, LogoutAPIView, DeleteAPIView, ChangePasswordAPIView

app_name = 'accounts'

urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("delete/", DeleteAPIView.as_view(), name="user_delete"),
    path("change-password/", ChangePasswordAPIView.as_view(), name='change_password'),
    path("<str:username>/subscribes/", views.SubscribeView.as_view(), name="subscribes"),
    path("<str:username>/mypage/", views.Mypage.as_view(), name="mypage"),

]