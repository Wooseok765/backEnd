from rest_framework.serializers import ModelSerializer
from .models import Wishlist
from rooms.serializer import RoomListSerializer

class WishlistSerializer(ModelSerializer):
    rooms = RoomListSerializer(many=True, read_only=True)
    # Wishlist 하나에는 여러 Room이 연결될 수 있으므로 many=True를 사용한다.
    # rooms는 조회 결과에 RoomListSerializer 형식으로 표시하지만, Wishlist 생성·수정 입력에서는 받지 않기 위해 read_only=True로 설정한다.
    # RoomListSerializer의 is_owner 필드는 self.context["request"]를 사용한다. WishlistSerializer 안에 중첩되어 사용될 때도 request가 필요하므로, Wishlist view에서 WishlistSerializer를 생성할 때 context={"request": request}를 전달해야 한다.
    class Meta : 
        model = Wishlist
        fields = (
            "name",
            "rooms", # wishlist객체가 가지고있는 relational field인데 여기에 작성하면 입력하는 유저가 직접 작성한다는 의미
            # serializer는 DB에서 객체를 가져올 때(get), 수정/삭제/업로드할 때 모두 사용함
        )
    