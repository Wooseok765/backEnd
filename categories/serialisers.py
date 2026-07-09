from rest_framework import serializers
from categories.models import Category



class CategorySerializer(serializers.Serializer):
    # 이 클래스는 arguement로 받은 object에서 일치하는 필드를 찾아 JSON으로 변환시킴
    # 실제 필드와 이름, 타입을 일치시켜야함
    # 다른 모델의 오브젝트를 주어도 필드명과 타입이 일치한다면 사용가능
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=50,
    )
    kind = serializers.ChoiceField(
        choices=Category.KindChoice.choices,
    )
    created_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.kind = validated_data.get("kind", instance.kind)
        instance.save()
        return instance