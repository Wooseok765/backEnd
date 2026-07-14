from rest_framework.serializers import ModelSerializer
from rooms.models import Amenity
from .models import Room
from users.serializers import TinyUserSerializer
from categories.serialisers import CategorySerializer

class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description")
        
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        depth = 1
        
class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )
        
class RoomDetailSerializer(ModelSerializer):
    
    owner = TinyUserSerializer(read_only=True)
    amenity = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Room
        fields = "__all__" 
        
  
        
  