from django.contrib import admin
from direct_messages.models import ChattingRoom, Message
# Register your models here.

@admin.register(ChattingRoom)
class ChattingRoomAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user_count",
        "created_at",
    )
    
    def user_count(self, obj):
        return obj.users.count()
    
    user_count.short_description = "Participants"
    

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "text",
        "updated_at",
    )