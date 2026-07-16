from rest_framework import serializers
from .models import Review
from users.serializers import TinyUserSerializer
class ReviewSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True) # review들을 표시할 때 user를 정보를 해당 serializer에서 정의한 대로 표기
    # read_only로 설정하여 user가 리뷰 작성자를 임의로 바꿔서 작성하는것을 방지
    # 해당 ReviewSerializer 클래스에 user 필드가 있어야 누가 작성했는지를 보여주는데 (조회할 때도 사용하기 때문) 입력할 때 마음대로 바꾸지 못하게 하는 설정
    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )