from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView 
from .views import SignupAPIView 

app_name = 'accounts'
urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name='signup'),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("accounts/<str:username>/mypage/", views.Mypage.as_view(), name="mypage")
]