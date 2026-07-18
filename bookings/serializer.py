from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Booking


class CreatRoomBookingSerializer(ModelSerializer):
    check_in = serializers.DateField()  # validate_check_in()의 반환값을 가진다
    check_out = serializers.DateField()

    # 모델에있는 동명의 값은 null=True이기 때문에 required인 serializer field로 덮어씌우려는것, 어차피 생성용이라 상관없음
    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        # .is_valid()가 실행될 때 작동됨
        # 특정 필드를 검증하는(여기선 check_in을 검증) 커스텀 method를 만드는것, validate_까지가 reserved keyword
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't check out before check in")
        return value

    def validate(self, data):  # serializer로 넘어온 모든 데이터(유저가 입력한)를 검증
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "check_in can't be later than check_out"
            )  # 입력데이터가 규칙에 맞지않다는 경고를 띄움(400)

        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError("The room has already booked")
        # 새로 부킹하려는 기간내에 일부라도 겹치는 날짜를 가진 booking 객체가 있을경우(특정 id의 room객체에 대해서) true를 반환함

        return data


class PublicBookingSerializer(ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )
