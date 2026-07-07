from rest_framework import serializers 

class CategorySerealizer(serializers.Serializer):
     # 이 클래스는 arguement로 받은 object에서 일치하는 필드를 찾아 JSON으로 변환시킴
     # 실제 필드와 이름, 타입을 일치시켜야함
     # 다른 모델의 오브젝트를 주어도 필드명과 타입이 일치한다면 사용가능
     pk = serializers.IntegerField()
     name = serializers.CharField(required = True)
     kind = serializers.CharField() 
     created_at = serializers.DateTimeField()