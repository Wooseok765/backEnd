from django.urls import path
from rooms import views

urlpatterns = [
    path(
        "",
        views.say_room,
    ),
    path(
        "<int:roomNumber>",
        views.show_one_room,
    ),
    path(
        "<str:myTemplate>",
        views.call_template,
    ),
]
