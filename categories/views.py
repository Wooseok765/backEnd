from categories.models import Category
from categories.serialisers import CategorySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()