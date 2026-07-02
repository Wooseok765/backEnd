from django.db import models
from common.models import CommonModel


# Create your models here.
class Experience(CommonModel):
    name = models.CharField(max_length=140)
    country = models.CharField(
        max_length=50,
        default="Ireland",
    )
    city = models.CharField(
        max_length=60,
        default="Dublin",
    )
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=140)
    start_at = models.TimeField()
    end_at = models.TimeField()
    description = models.TextField()
    perk = models.ManyToManyField(
        "Perk",
        null=True,
        blank=True,
        related_name="experiences",
    )

    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="experiences",
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    name = models.CharField(max_length=200)
    details = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
