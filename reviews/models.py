from django.db import models
from common.models import CommonModel


# Create your models here.
class Review(CommonModel):
    class RatingChoice(models.IntegerChoices):
        star1 = (1, "⭐")
        star2 = (2, "⭐⭐")
        star3 = (3, "⭐⭐⭐")
        star4 = (4, "⭐⭐⭐⭐")
        star5 = (5, "⭐⭐⭐⭐⭐")

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    payload = models.TextField()
    rating = models.PositiveBigIntegerField(
        choices=RatingChoice.choices,
    )

    def __str__(self):
        return f"ID: {self.user} / Rating: {self.rating}"
