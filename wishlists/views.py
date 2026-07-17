from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_200_OK
from .models import Wishlist
from rooms.models import Room
from .serializers import WishlistSerializer

# Create your views here.


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(
            user=request.user,
        )  # wishlist객체들을 가져올 때 객체의 user필드가 사용자와 동일한 객체들만 가져오는것
        serializer = WishlistSerializer(
            all_wishlists,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            user = request.user
            wishlist = serializer.save(
                user=user,
            )
            return Response(
                WishlistSerializer(wishlist).data,
            )
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(
        self, pk, user
    ):  # wishlist는 로그인한 사용자의 리스트만 반환해야하기에 유저정보를 받을 수 있는 자리를 마련한다.
        # HTTP 요청은 get_object()를 직접 호출하지 않는다.
        # get(), put(), delete() 같은 HTTP 요청 처리 메서드에서
        # 필요한 pk와 user 값을 전달받아 Wishlist 객체를 조회하는 보조 메서드이다.

        # get(), post(), put(), delete()는 HTTP 요청에 의해 DRF가 호출하는 요청 처리 메서드이고, get_object()는 그 내부에서 직접 호출하는 보조 메서드이다. get_object()의 매개변수는 호출하는 쪽에서 직접 전달해야 한다.
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk=pk, user=request.user)
        serializer = WishlistSerializer(
            wishlist,
            context={"request": request},
        )
        # 한 사용자가 wishlist 여러개를 만들어도 하나씩만 가져오는 중이기에 many=True필요없음
        return Response(serializer.data)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
            context={"request": request},
        )  # 수정용 인스턴스 생성하면서 Wishlist내부에서 사용되는 RoomListSerializer가 요구하는 context를 보냄
        if serializer.is_valid():
            wishlist = serializer.save()
            return Response(
                WishlistSerializer(wishlist, context={"request": request}).data
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)


class WishlistTogle(APIView):
    # put만 누를 수 있는 API, url에 입력된 아이디 넘버의 room객체를 wishlist객체와 연결시켰다끊었다 함(DB에 행으로 넜다뺐다)
    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(
                pk=pk,
                user=user,
            )
        except Wishlist.DoesNotExist:
            raise NotFound
        
    def get_room(self, pk):
        try:
            return Room.objects.get(
                pk=pk,
            )
        except Room.DoesNotExist:
            raise NotFound    

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists(): # 불러온 room 객체와 wishlist의 rooms객체들 중 일치하는게 있는지 확인하는것
            # Wishlist.rooms는 manytomany이기에 filter가 있으며 이는 검색 중 일치하는 값들만 반환 하기에 저장된 모든 객체를 가져오고난 후 판단하는 .all()과 다름
            # .exists()를 썼기에 boolean반환함
            wishlist.rooms.remove(room) # list 형태인 rooms에서 room객체 하나를 삭제한는것
            return Response(status=HTTP_200_OK)
        else:
            wishlist.rooms.add(room)
            # 좋아요 버튼처럼 기존에 있었으면 실행취소, 없었으면 추가하는 기능, wishlist-room DB에 새로운 행을 추가함
            return Response(status=HTTP_200_OK)
            
        
