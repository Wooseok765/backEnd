from django.shortcuts import render
from categories.models import Category
from django.http import JsonResponse # 파이선에서 작성한걸 JSON형식으로 보내주는 클래스
from django.core import serializers # object를 JSON으로 바꿔주는 클래스
from rest_framework.decorators import api_view
from rest_framework.response import Response
from categories.serialisers import CategorySerealizer
# Create your views here.
@api_view(["GET", "POST"]) #장고 REST 프레임 워크를 사용하는 함수라는 뜻
def categories(request):    
    if request.method =="GET":
        all_categories = Category.objects.all()
        serializers = CategorySerealizer(all_categories, many=True)
        return Response(serializers.data) # Django REST framework이 제공하는 형식으로 payload를 표현함
    elif request.method =="POST":
        return Response({"created":True})
    

@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerealizer(category)
    return Response(serializer.data)
