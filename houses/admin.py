from django.contrib import admin
from .models import House
# Register your models here.

@admin.register(House)
# House라는 모델을 admin module의 register 클래스에 등록
class HouseAdmin(admin.ModelAdmin):
    pass
# ModleAdmin은 admin 패널기능을 제공하는 클래스
# HouseAdmin class가 House 모델을 컨트롤 한다는 의미