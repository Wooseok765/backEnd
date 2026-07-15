from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rooms.models import Amenity
from .models import Room
from users.serializers import TinyUserSerializer
from categories.serialisers import CategorySerializer
from reviews.serializer import ReviewSerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description")
        
        
class AmenitySerializerAll(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("__all__")


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
            "rating",
            "is_owner",
        )
        # "__all__"이 아니기 때문에 새로 만든 필드를 추가해주어야한다

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, room):
        return room.owner == self.context["request"].user

    def get_rating(self, room):
        return room.rating()


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(
        read_only=True,
    )
    amenity = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )

    class Meta:
        model = Room
        fields = "__all__"

    rating = serializers.SerializerMethodField()
    # 현재 클레스를 사용하는 모델에 없는 필드를 생성 함
    # potato의 value는 내부 메서드를 호출하여 가져오는 것(get_ 메서드의 반환값)
    # get_potato라는 메서드를 현재 serializer class가 직렬화 하고있는 오브젝트와 함께 호춣함
    # 해당 오브젝트는 get_ 메서드의 두 번째 arguemnt로 들어감
    # 모델이 가지고있는 않은(외부에서 참조하는) 값을 을 표시할 때 필요함

    # get_ 이 부분은 항상 고정임
    def get_rating(self, room):
        return room.rating()
        # room 객체의 model에서 정의된 rating()의 반환값을 직렬화메서드필드의 값으로 반환함
        # rating()은 각각의 room객체와 관련있는 review 객체들이 가지고있은
        # rating이라는 값의 평균값을 반환함

    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user
        # room 객체의 owner와 request의 user(로그인 중인 사용자)가 동일한지 비교
        # 해당 필드가 true일 때 유저에게 수정, 삭제 등의 기능을 보여주는 등 활용 가능

    