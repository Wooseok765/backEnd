from django.shortcuts import render
from categories.models import Category
from django.http import JsonResponse  # 파이선에서 작성한걸 JSON형식으로 보내주는 클래스
from django.core import serializers  # object를 JSON으로 바꿔주는 클래스
from rest_framework.decorators import api_view
from rest_framework.response import Response
from categories.serialisers import CategorySerializer
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView


# Create your views here.


@api_view(["GET", "POST"])  # 장고 REST 프레임 워크를 사용하는 함수라는 뜻
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        # Bring python objects

        serializers = CategorySerializer(
            all_categories,
            many=True,
        )  # prepare to be serialized

        return Response(serializers.data)
    elif request.method == "POST":
        serialized_data_from_user = CategorySerializer(
            data=request.data,
        )  # Prepare to be valided(making python object)

        if serialized_data_from_user.is_valid():
            model_object = serialized_data_from_user.save()
            return Response(
                CategorySerializer(model_object).data,
                # prepare to be serialized
            )
        else:
            return Response(serialized_data_from_user.errors)


@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        # same as CategorySerializer(category).data
    except Category.DoesNotExist:
        raise NotFound

    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
            # Allow to update partially even though a certain field has field option required
            # 없는 필드가 request.data로 들어올 경우 is_valid()에서 무시되고(에러안남) 기존 값이 불러짐
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
