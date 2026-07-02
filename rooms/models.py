from django.db import models
from common.models import CommonModel


# Create your models here.
class Amenity(CommonModel):
    """Amenity Definition"""

    name = models.CharField(
        max_length=50,
    )
    description = models.TextField(
        max_length=200,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"


class Room(CommonModel):
    """Room Definition"""

    class Room_kindChoice(models.TextChoices):
        DOUBLE = (
            "double",
            "Double room",
        )
        SINGLE = (
            "single",
            "Single room",
        )
        SHARED = (
            "shared",
            "Shared room",
        )

    name = models.CharField(max_length=140, default="")
    country = models.CharField(
        max_length=50,
        default="Ireland",
    )
    city = models.CharField(
        max_length=60,
        default="Dublin",
    )
    price = models.PositiveBigIntegerField()
    number_of_room = models.PositiveBigIntegerField()
    toilets = models.PositiveBigIntegerField()
    description = models.TextField(max_length=200)
    address = models.CharField(max_length=140)
    pet_friendly = models.BooleanField(default=True)
    room_kind = models.CharField(
        max_length=140,
        choices=Room_kindChoice.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenity = models.ManyToManyField(
        "Amenity",
        related_name="rooms",
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rooms"
    )

    def __str__(self):
        return self.name
