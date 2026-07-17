from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Booking

class CreatRoomBookingSerializer(ModelSerializer):
    check_in = serializers.DateField() # validate_check_in()의 반환값을 가진다
    check_out = serializers.DateField()
    # 모델에있는 동명의 값은 null=True이기 때문에 required인 serializer field로 덮어씌우려는것, 어차피 생성용이라 상관없음
    
    class Meta :
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )
        
    def validate_check_in(self, value):
        # value는 validate data. 만약 들어온 value를 다시 반환한다면 validated된 data라는것(여기서 value는 post하며 유저가 입력한 check_in의 값)
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

class PublicBookingSerializer(ModelSerializer):
    
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )
