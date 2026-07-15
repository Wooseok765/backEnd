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

    reviews = ReviewSerializer(
        many=True,
        read_only=True,
    )
    # 각 방 사용자가 생성한 리뷰들을 reviews.serializer.py에 정의된 방식으로 표기하는 것
    # reverse accessor는 review.model에서 room 을 relational field로 선언할 때 room 객체에 자동으로 생성되었음
    # 그래서 하나의 room 객체가 가지는 모든 review 객체들을 reverse accessor인 reviews로 접근가능함
    # 속성 이름을 reverse accessor와 일치시켜야함(기본값:  review_set, reviews.model에서 선언 시 related_name="reviews"로 바꾼상태)
    # Django가 위 코드를 보고 room.reviews를 찾아서 적용시킨다(reverse accessor) 이때 room.reviews는 quretySet이기 때문에 many=True가 필요함
