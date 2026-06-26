from django.db import models

# Create your models here.
class House(models.Model): # inherites superclass
    """Model Definition for Houses"""
    
    # Django에서 DB테이블 만들려면 Model을 상속해야함\
    # 그래야 단순 파이썬클래스가 아닌 DB모델로 인식
    # models라는 module에서 Model이라는 class를 상속함
    
    name = models.CharField(max_length=140)
    # Defining type of the value
    # charField : text having limit of the length
    
    price_per_night = models.PositiveBigIntegerField()
    # 양수 숫자 타입을 말함
    
    description = models.TextField()
    # longer than charField
    
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(default=True)