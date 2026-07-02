from django.contrib import admin
from wishlists.models import Wishlist
# Register your models here.

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
    )
