from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    class GenderChoice(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoice(models.TextChoices):
        KR = ("kr", "KOREAN")
        EN = ("eng", "ENGLISH")

    class CurrencyChoice(models.TextChoices):
        WON = ("won", "Won(KOREA)")
        DOLLAR = ("dollar", "Dollar(USA)")

    first_name = models.CharField(
        max_length=150,
        blank=True,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        editable=False,
    )
    name = models.CharField(
        max_length=140,
        default="",
    )
    is_host = models.BooleanField(default=False)
    profile_photo = models.URLField(blank=True)
    gender = models.CharField(
        default="null",
        max_length=140,
        choices=GenderChoice.choices,
    )
    language = models.CharField(
        default="null",
        max_length=10,
        choices=LanguageChoice.choices,
    )
    currency = models.CharField(
        default=CurrencyChoice.WON,
        max_length=10,
        choices=CurrencyChoice.choices,
    )
