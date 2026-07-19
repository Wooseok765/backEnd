from django.urls import path
from .views import MyProfile, Users, PublicUsers, ChangePassword, LogIn, LogOut

urlpatterns = [
    path("", Users.as_view()),
    # path("<str:username>", PublicUsers.as_view()),# 이 url정보가 위로가면 개인프로필을 요구하는 users/me 요청에서 me를 유저아이디로 인식하기 때문에 개인프로필을 못보게됨
    path("log-in", LogIn.as_view()),
    path("log-out", LogOut.as_view()),
    path(
        "@<str:username>", PublicUsers.as_view()
    ),  # 하지만 유저가이디가 me인 사람도 있을 수 있으니 방지하기위해 @추가
    path("me", MyProfile.as_view()),
    path("change-password", ChangePassword.as_view()),
]
