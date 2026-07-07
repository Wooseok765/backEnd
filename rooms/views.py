from django.shortcuts import render
from django.http import HttpResponse
from rooms.models import Room


# Create your views here.
def say_room(request):
    return HttpResponse("Room root URL")


def show_one_room(request, roomNumber):
    try:
        room = Room.objects.get(pk=roomNumber)
        return render(
            request,
            "see_one_room.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:  # DoesNotExist is an exception classes. It occurs when no matching data exists in the model(Room this case)
        return render(
            request,
            "see_one_room.html",
            {
                "not_found": True,
            },
        )


def call_template(request, myTemplate):
    rooms = Room.objects.all()
    return render(
        request,
        "sample.html",
        {
            "roomName": rooms,
            "text": "hello, suckers",
        },
    )
