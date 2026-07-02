from django.contrib import admin
from experiences.models import Experience, Perk

# Register your models here.


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "start_at",
        "end_at",
    )
    readonly_fields = ("updated_at",)


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "details",
        "description",
    )
    readonly_fields = ("updated_at",)
