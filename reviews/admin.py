from django.contrib import admin
from reviews.models import Review

# Register your models here.
class newFilter(admin.SimpleListFilter):
    title = "Filter by keyword"
    parameter_name = "filter_URL"
    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]
        
    def queryset(self, request, queryset):
        word = self.value()
        if word:
            return queryset.filter(payload__contains = word)
        else:
            return queryset

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        newFilter,
        "rating",
    )