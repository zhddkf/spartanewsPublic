from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path("accounts/<str:username>/mypage/", views.Mypage.as_view(), name="mypage")
]