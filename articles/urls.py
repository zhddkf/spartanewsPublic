from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupAPIView, LogoutAPIView, DeleteAPIView
urlpatterns = [
    path("<str:keyword>/", SignupAPIView.as_view(), name="signup"),
]