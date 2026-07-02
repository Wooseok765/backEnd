from django.db import models
from common.models import CommonModel

# Create your models here.


class Photo(CommonModel):
    file = models.ImageField()
    description = models.TextField()
    rooms = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    experiences = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self):
        return "photo file"


class Video(CommonModel):
    file = models.FileField()
    experiences = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "video file"
