from django.contrib import admin
from rooms.models import Room, Amenity

# Register your models here.

@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request_user_object, querysets):
    for price in querysets.all():
        price.price = 0
        price.save()
        

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)
    list_display = (
        "name",
        "owner",
        "rating",
        "category",
        "total_amenities",
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
    
    search_fields = (
        "name",
        "owner__username",
        "price",
    )
    
    def total_amenities(self, room):
        return room.amenity.count()
    
    total_amenities.shortdescription = "total amenities"


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
