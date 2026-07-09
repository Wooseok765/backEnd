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
class Categories(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        serializers = CategorySerializer(
            all_categories,
            many=True,
        )
        return Response(serializers.data)

    def post(self, request):
        serialized_data_from_user = CategorySerializer(
            data=request.data,
        )
        if serialized_data_from_user.is_valid():
            model_object = serialized_data_from_user.save()
            return Response(
                CategorySerializer(model_object).data,
            )
        else:
            return Response(serialized_data_from_user.errors)


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound
        return category
    
    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)

