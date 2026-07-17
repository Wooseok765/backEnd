from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rooms.models import Amenity
from .models import Room
from users.serializers import TinyUserSerializer
from categories.serialisers import CategorySerializer
from reviews.serializer import ReviewSerializer
from medias.serializers import PhotoSerializer


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
            "photos",
            "is_owner",
        )
        # "__all__"이 아니기 때문에 새로 만든 필드를 추가해주어야한다

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True,read_only=True)
    # serializer method fields(모델에 실제 필드가 없거나, 그대로 보여주면 원하는 형태가 아닐 때, serializer에서 값을 직접 계산해서 출력하기 위해 사용, 읽기전용이다, 필드값을 구현할 전용함수필요)

    def get_is_owner(self, room):
        return room.owner == self.context["request"].user
    # view.py에서부터 전달받은 객체를(http request에서 추출한) 사용하는것
    # 예) 현재 사용자가 로그인했는지 여부
    # self.context["request"].user : 현재 로그인 한 사용자 정보

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
    photos = PhotoSerializer(many=True,read_only=True)
    # read_only는 room 객체 생성 시 photos의 값을 받아도 무시, 외부에서 생성된 사진을 받아서 표시만 한다는 뜻
    # photo 객체는 단독으로 생성해야한다는 의미
    # photos라는 필드는 현재 Room 모델의 필드값이 아님, 외부에서 받아서 표시하는것(reverse accessor 사용)

    class Meta:
        model = Room
        fields = "__all__"

    rating = serializers.SerializerMethodField()
    # 현재 클레스를 사용하는 모델에(rooms) 없는 필드를 가져옴
    # rating의 value는 내부 메서드를 호출하여 가져오는 것(get_ 메서드의 반환값)
    # get_rating이라는 메서드를 현재 serializer class가 직렬화 하고있는 오브젝트와 함께 호춣함
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

    