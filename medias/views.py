from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from .models import Photo
# Create your views here.

class PhotoDetail(APIView):
    permission_classes = [IsAuthenticated] # 클래스에 HTTP 요청으로 들어오는 메서드(get, post, put, patch, delete 등)를 실행하기 전에, 해당 요청 유저를 먼저 검사하는 설정
    # 다른 어플리케이션의 views.py에서 진행했던 if not request.user.is_authenticated: 단계를 대체함
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound(f"Photo({pk}) not found")
    
    def delete(self, request, pk):
        # 삭제를 시도하는 자가 업로드한자와 동일한지 검증하기위해 request가 필요
        # 사진 업로드한 사람이 아닌 사진과 연결된 room 또는 experience의 owner와 동일한지 비교해야함(사진의 외부키 활용)
        photo = self.get_object(pk)
        if (photo.rooms and photo.rooms.owner != request.user) or (photo.experiences and photo.experiences.host != request.user):
            # photo 객체가 rooms 또는 experiences 필드의 값을 가지고 있는 경우에만 시행(rooms의 field option이 null, blank=True이기 때문)
            # rooms또는 experiences을 등록한 주인과 삭제시도 하는 request의 user를 비교(외부키를 타고 접근함)
            raise PermissionDenied               
        photo.delete()
        return Response(HTTP_200_OK)