from django.contrib import admin
from bookings.models import Booking


# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "room",
        "check_in",
        "check_out",
        "experience",
        "experience_date",
        "guests",
    )
    list_filter = (
        "kind",
    )
