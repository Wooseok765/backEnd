from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
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


class WishlistsDetail(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
