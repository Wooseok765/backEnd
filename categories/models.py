from django.db import models
from common.models import CommonModel


# Create your models here.
class Category(CommonModel):

    class KindChoice(models.TextChoices):
        ROOMS = ("room", "Room")
        EXPERIENCES = ("experience", "Experience")

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=50,
        choices=KindChoice.choices,
    )
    def __str__(self):
        return f"{self.kind.title()}: {self.name}"
    
    class Meta:
        verbose_name_plural = "Categories"
