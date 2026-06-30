from django.contrib import admin
from rooms.models import Room, Amenity

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_filter = (
        "country",
        "city",
        "price",
        "address",
        "created_at",
        "updated_at",
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    
    list_filter = (
        "name",
        "created_at",
        "updated_at",
    )
    
    readonly_fields = (
        "created_at",
        "updated_at",
    )
