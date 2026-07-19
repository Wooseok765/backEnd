from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# authenticate : username, password를 보내고 이게 일치하면 User 객체를 반환함
# login : 유저가 request를 보내면 django가 브라우저에 모든 필요한 정보를 반환해줌
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from .serializers import PrivateUserSerializer
from .models import User
# Create your views here.

class MyProfile(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        user = request.user #현재 로그인 사용자 정보(수정이 필요한 기존 객체)
        serializer = PrivateUserSerializer(user, data=request.data, partial=True,)
        # request.data : http request 본문에 담긴 수정용 데이터
        if serializer.is_valid():
            new_user = serializer.save()
            serializer = PrivateUserSerializer(new_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class Users(APIView): 
    def post(self, request): # 로그인이나 회원가입설정
        # Django에서 기본적인 중복검사는 pk와 username이다
        # 나머지도 중복 안되게 하려면 모델에서 unique=True 선언해야함
        # password만 체크하면 됨
        serializer = PrivateUserSerializer(data=request.data)
        password = request.data.get('password')
        if not password:
            raise ParseError("Please enter a password")
        
            
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(password) # hash화 된 비밀번호를 파이선 객체에 저장
            # new_user.password = password는 안됨. raw password를 그대로 저장하는것
            new_user.save() # 변경사항을 DB에 업데이트
            serializer = PrivateUserSerializer(new_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class PublicUsers(APIView): # 공개된 프로필 반환
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = PrivateUserSerializer(user) # 타인의 정보를 공개시키는 기능이기에 public으로 보여주기 합당한 정보들로 구성된 직렬화 클래스 필요
        return Response(serializer.data)
    
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user = request.user
        old_password = request.data.get('old_password') # 유저가 입력하는 기존 비밀번호, DB상의 비번과 일치여부 파악을 위해 입력시킴(hash상태)
        new_password = request.data.get('new_password') # raw password상태
        if not old_password or not new_password:
            raise ParseError
        
        if user.check_password(old_password): # 로그인한 사용자의 비밀번호와(hash상태) 유저가 직접 입력한 비밀번호(hash상태)가 일치하는지 비교하는 코드
            user.set_password(new_password) # 비밀번호 해쉬화 됨
            user.save() # DB에 비번 저장(업데이트)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
            
class LogIn(APIView):
        
    def post(self, request): # 로그인 정보를 서버에 제출하는것이기에 get이 아님
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username, password=password)
        # User DB에서 일치하는 객체를 확인 후 반환함(없을수도있음)
        if user:
            login(request, user) # 로그인시킴
            return Response({"OK" : "Welcome"})
        else:
            return Response({"Error": "Wrong ID or Password. Please check it again"}) # 이렇게 보내면 나중에 Error라는 이름으로 해당 내용에 접근할 수 있음. 그래서dictionary형태로 응답하는것
        
class LogOut(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({"ok":"you are logged out"})
        